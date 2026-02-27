Authentication
==============

The USNAN SDK can be used without authentication to access publicly released datasets. To access
additional datasets (e.g., your own unreleased data), you can authenticate with your NMR Hub account.

Authentication uses OAuth2 via Keycloak. Once authenticated, your session is saved locally so you
don't need to log in again until your session expires.

Browser Login
-------------

The simplest way to authenticate is the browser-based flow. This opens your default web browser
to complete the login:

.. code-block:: python

   import usnan

   client = usnan.USNANClient()
   client.login()

If you already have an active NMR Hub session in your browser, authentication will complete
automatically. Otherwise, you'll be prompted to log in via the standard NMR Hub login page.

Device Login
------------

For headless or remote environments (e.g., SSH sessions, servers, containers), use the device
authorization flow:

.. code-block:: python

   client = usnan.USNANClient()
   client.login(method='device')

This prints a URL and code to your terminal. Open the URL on any device (including your phone),
enter the code, and log in. The SDK will detect the authorization automatically.

Direct Token
------------

For automation and CI/CD pipelines, you can pass a pre-obtained access token directly:

.. code-block:: python

   client = usnan.USNANClient()
   client.login(method='token', token='eyJ...')

Note that direct tokens cannot be automatically refreshed. When the token expires, you'll need
to provide a new one.

Session Persistence
-------------------

By default, the SDK saves your refresh token to disk after a successful login. On subsequent
runs, ``USNANClient()`` will automatically restore your session without requiring you to call
``login()`` again:

.. code-block:: python

   # First run — login required
   client = usnan.USNANClient()
   client.login()

   # Later runs — session is restored automatically
   client = usnan.USNANClient()
   # No login() needed, already authenticated

The token is stored with restrictive file permissions (owner-only read/write) in your
platform's standard data directory:

* Linux: ``~/.local/share/usnan/tokens.json``
* macOS: ``~/Library/Application Support/usnan/tokens.json``
* Windows: ``%LOCALAPPDATA%\usnan\tokens.json``

To disable persistence (e.g., in shared environments):

.. code-block:: python

   client = usnan.USNANClient(persist=False)
   client.login()  # Token is not saved to disk

Logging Out
-----------

To revoke your session and remove any saved tokens:

.. code-block:: python

   client.logout()

This revokes the refresh token with Keycloak and deletes the local token file.

Error Handling
--------------

If you attempt to access a resource that requires authentication, the SDK raises a
``PermissionError``:

.. code-block:: python

   try:
       results = list(client.datasets.search(config))
   except PermissionError:
       print("Authentication required — call client.login()")
