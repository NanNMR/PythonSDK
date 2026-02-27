"""Main client for USNAN API"""

from __future__ import annotations

import logging
import time

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from .auth import KeycloakAuth
from .endpoints import DatasetsEndpoint, FacilitiesEndpoint, SpectrometerEndpoint, ProbesEndpoint

# Set up logger for this module
logger = logging.getLogger(__name__)


class USNANClient:
    """Main client for interacting with the USNAN API
    
    Attributes:
        facilities: Access to facilities endpoint for querying facility information
        spectrometers: Access to spectrometers endpoint for querying spectrometer data
        datasets: Access to datasets endpoint for querying dataset information
        probes: Access to probes endpoint for querying probe data
    """

    def __init__(self, base_url: str="https://api.nmrhub.org", timeout: int = 30, num_retries: int = 3,
                 persist: bool = True):
        """
        Initialize the USNAN client

        Args:
            base_url: Base URL for the USNAN API
            timeout: Request timeout in seconds
            num_retries: Number of retries for failed requests (only for 500 errors or connectivity issues)
            persist: Save authentication tokens to disk for reuse across sessions
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.num_retries = num_retries
        self._cache_clear_time = time.time()
        self._auth: KeycloakAuth | None = None
        self._persist = persist

        # Initialize session
        self.session = requests.Session()

        # Initialize endpoints
        self.datasets = DatasetsEndpoint(self)
        self.facilities = FacilitiesEndpoint(self)
        self.spectrometers = SpectrometerEndpoint(self)
        self.probes = ProbesEndpoint(self)

        # Attempt to restore a previous session from saved tokens
        if persist:
            auth = KeycloakAuth(persist=True)
            if auth.restore():
                self._auth = auth
                self.session.headers["Authorization"] = f"Bearer {auth.get_token()}"
                logger.info("Restored authenticated session from saved token.")
    
    def login(self, method: str = "browser", *, token: str | None = None, **kwargs) -> None:
        """Authenticate with the NMR Hub API via Keycloak.

        Args:
            method: Authentication method — ``'browser'`` (default), ``'device'``, or ``'token'``.
            token: Access token string (required when *method* is ``'token'``).
            **kwargs: Extra keyword arguments forwarded to the underlying auth method
                (e.g. ``port`` or ``timeout`` for the browser flow).
        """
        auth = KeycloakAuth(persist=self._persist)

        if method == "browser":
            auth.login_browser(**kwargs)
        elif method == "device":
            auth.login_device()
        elif method == "token":
            if token is None:
                raise ValueError("A token must be provided when using method='token'.")
            auth.login_token(token)
        else:
            raise ValueError(f"Unknown login method: {method!r}. Use 'browser', 'device', or 'token'.")

        self._auth = auth
        self.session.headers["Authorization"] = f"Bearer {auth.get_token()}"
        logger.info("Authenticated successfully.")
        print("Authenticated successfully.")

    def logout(self) -> None:
        """Log out and clear authentication state."""
        if self._auth:
            self._auth.logout()
        self.session.headers.pop("Authorization", None)
        self._auth = None

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request to the API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)

        # Refresh the bearer token if we're authenticated
        if self._auth:
            self.session.headers["Authorization"] = f"Bearer {self._auth.get_token()}"

        last_exception = None

        for attempt in range(self.num_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (ConnectionError, Timeout) as e:
                # Network connectivity issues - retry
                last_exception = e
                if attempt < self.num_retries:
                    logger.info(f"Request to {url} failed due to connectivity issue, retrying in {2 ** attempt} seconds (attempt {attempt + 1}/{self.num_retries + 1})")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            except requests.HTTPError as e:
                # Only retry on 500 status codes
                if e.response.status_code == 500:
                    last_exception = e
                    if attempt < self.num_retries:
                        logger.info(f"Request to {url} failed with HTTP 500, retrying in {2 ** attempt} seconds (attempt {attempt + 1}/{self.num_retries + 1})")
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                if e.response.status_code == 401:
                    raise PermissionError("Authentication required or session expired. Please call client.login() to authenticate.")
                if e.response.status_code == 400:
                    raise RuntimeError(f"NMRhub server indicated your request was invalid: {e.response.json()['message']}")
                if e.response.status_code == 404:
                    raise KeyError(f"NMRhub server indicated no results: {e.response.json()['message']}")
                raise
            except RequestException:
                # Other request exceptions - don't retry
                raise
        
        # If we get here, all retries failed
        raise last_exception

    def clear_cache(self) -> None:
        self._cache_clear_time = time.time()

    @property
    def cache_clear_time(self):
        return self._cache_clear_time
