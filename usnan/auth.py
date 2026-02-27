"""Keycloak OAuth authentication for USNAN SDK"""

from __future__ import annotations

import base64
import hashlib
import http.server
import json
import logging
import os
import secrets
import stat
import threading
import time
import webbrowser
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs

import requests
from platformdirs import user_data_dir

logger = logging.getLogger(__name__)

KEYCLOAK_URL = "https://keycloak.nmrhub.org"
KEYCLOAK_REALM = "nmrhub"
CLIENT_ID = "usnan-programmatic"

_BASE = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect"
TOKEN_URL = f"{_BASE}/token"
AUTHORIZATION_URL = f"{_BASE}/auth"
DEVICE_AUTH_URL = f"{_BASE}/auth/device"
REVOCATION_URL = f"{_BASE}/revoke"

_TOKEN_FILE = Path(user_data_dir("usnan", ensure_exists=True)) / "tokens.json"


def _save_refresh_token(refresh_token: str) -> None:
    """Persist the refresh token to disk with restrictive permissions."""
    _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    _TOKEN_FILE.write_text(json.dumps({"refresh_token": refresh_token}))
    os.chmod(_TOKEN_FILE, stat.S_IRUSR | stat.S_IWUSR)


def _load_refresh_token() -> str | None:
    """Load a previously saved refresh token, or return None."""
    try:
        data = json.loads(_TOKEN_FILE.read_text())
        return data.get("refresh_token")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


def _delete_saved_token() -> None:
    """Remove the saved token file."""
    try:
        _TOKEN_FILE.unlink()
    except FileNotFoundError:
        pass


class KeycloakAuth:
    """Handles OAuth2 authentication against the NMR Hub Keycloak server."""

    def __init__(self, persist: bool = True):
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self._token_expiry: float = 0
        self._persist = persist

    @property
    def authenticated(self) -> bool:
        return self.access_token is not None

    def login_browser(self, port: int = 0, timeout: int = 120) -> None:
        """Authorization Code + PKCE flow — opens a browser for login.

        Args:
            port: Local port for the callback server (0 = OS-assigned).
            timeout: Seconds to wait for the user to complete login.
        """
        code_verifier = secrets.token_urlsafe(96)[:128]
        code_challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
            .rstrip(b"=")
            .decode()
        )
        state = secrets.token_urlsafe(32)

        # Mutable container for the callback result
        result = {"code": None, "error": None}

        class _CallbackHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                qs = parse_qs(urlparse(self.path).query)
                if qs.get("state", [None])[0] != state:
                    result["error"] = "State mismatch"
                elif "error" in qs:
                    result["error"] = qs["error"][0]
                else:
                    result["code"] = qs.get("code", [None])[0]

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                if result["error"]:
                    self.wfile.write(b"<h1>Authentication failed</h1><p>You can close this tab.</p>")
                else:
                    self.wfile.write(b"<h1>Authentication successful</h1><p>You can close this tab.</p>")

            def log_message(self, format, *args):
                pass  # silence request logging

        server = http.server.HTTPServer(("127.0.0.1", port), _CallbackHandler)
        assigned_port = server.server_address[1]
        redirect_uri = f"http://localhost:{assigned_port}/callback"

        auth_url = (
            AUTHORIZATION_URL
            + "?"
            + urlencode(
                {
                    "response_type": "code",
                    "client_id": CLIENT_ID,
                    "redirect_uri": redirect_uri,
                    "scope": "openid email profile",
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                    "state": state,
                }
            )
        )

        # Handle the single callback request in a thread so we can enforce a timeout
        server_thread = threading.Thread(target=server.handle_request, daemon=True)
        server_thread.start()

        webbrowser.open(auth_url)
        server_thread.join(timeout=timeout)
        server.server_close()

        if result["error"]:
            raise RuntimeError(f"Authentication failed: {result['error']}")
        if result["code"] is None:
            raise TimeoutError("Authentication timed out — no callback received.")

        # Exchange authorization code for tokens
        resp = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": result["code"],
                "redirect_uri": redirect_uri,
                "client_id": CLIENT_ID,
                "code_verifier": code_verifier,
            },
        )
        resp.raise_for_status()
        self._store_tokens(resp.json())

    def login_device(self) -> None:
        """Device Authorization Grant flow — for headless/remote environments.

        Displays a URL and code for the user to visit and authorize.
        """
        resp = requests.post(
            DEVICE_AUTH_URL,
            data={"client_id": CLIENT_ID, "scope": "openid email profile"},
        )
        resp.raise_for_status()
        data = resp.json()

        if "verification_uri_complete" in data:
            print(f"Visit this URL to authenticate:\n  {data['verification_uri_complete']}")
        else:
            print(f"Visit {data['verification_uri']} and enter code: {data['user_code']}")

        device_code = data["device_code"]
        interval = data.get("interval", 5)
        expires_at = time.time() + data.get("expires_in", 600)

        while time.time() < expires_at:
            time.sleep(interval)
            token_resp = requests.post(
                TOKEN_URL,
                data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "device_code": device_code,
                    "client_id": CLIENT_ID,
                },
            )
            token_data = token_resp.json()

            if "access_token" in token_data:
                self._store_tokens(token_data)
                return

            error = token_data.get("error")
            if error == "authorization_pending":
                continue
            elif error == "slow_down":
                interval += 5
                continue
            else:
                raise RuntimeError(f"Device authentication failed: {token_data.get('error_description', error)}")

        raise TimeoutError("Device authentication timed out — user did not authorize in time.")

    def login_token(self, token: str) -> None:
        """Accept a pre-obtained access token directly.

        Args:
            token: A valid Keycloak access token string.
        """
        self.access_token = token
        self.refresh_token = None
        self._token_expiry = 0  # unknown — no auto-refresh possible

    def restore(self) -> bool:
        """Attempt to restore a session from a saved refresh token.

        Returns:
            True if a valid session was restored, False otherwise.
        """
        saved_token = _load_refresh_token()
        if not saved_token:
            return False

        self.refresh_token = saved_token
        try:
            self.refresh()
            return True
        except (requests.HTTPError, RuntimeError):
            # Refresh token expired or revoked — clean up
            self.refresh_token = None
            _delete_saved_token()
            return False

    def refresh(self) -> None:
        """Refresh the access token using the stored refresh token."""
        if not self.refresh_token:
            raise RuntimeError("No refresh token available — cannot refresh.")

        resp = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": CLIENT_ID,
            },
        )
        resp.raise_for_status()
        self._store_tokens(resp.json())

    def get_token(self) -> str:
        """Return the current access token, refreshing if close to expiry.

        Returns:
            The access token string.
        """
        if not self.access_token:
            raise RuntimeError("Not authenticated — call login() first.")

        # Refresh if within 30 seconds of expiry and we have a refresh token
        if self.refresh_token and self._token_expiry and time.time() > self._token_expiry - 30:
            logger.info("Access token near expiry, refreshing...")
            self.refresh()

        return self.access_token

    def logout(self) -> None:
        """Revoke the refresh token and clear stored credentials."""
        if self.refresh_token:
            try:
                requests.post(
                    REVOCATION_URL,
                    data={
                        "client_id": CLIENT_ID,
                        "token": self.refresh_token,
                        "token_type_hint": "refresh_token",
                    },
                )
            except requests.RequestException:
                logger.warning("Failed to revoke refresh token at Keycloak.")

        self.access_token = None
        self.refresh_token = None
        self._token_expiry = 0

        if self._persist:
            _delete_saved_token()

    def _store_tokens(self, token_data: dict) -> None:
        self.access_token = token_data["access_token"]
        self.refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")
        self._token_expiry = time.time() + expires_in if expires_in else 0

        if self._persist and self.refresh_token:
            _save_refresh_token(self.refresh_token)
