"""Main client for USNAN API"""

import requests
from .endpoints import DatasetsEndpoint, FacilitiesEndpoint, SpectrometerEndpoint, ProbesEndpoint


class USNANClient:
    """Main client for interacting with the USNAN API"""
    
    def __init__(self, base_url: str="https://dev.api.nmrhub.org", timeout: int = 30):
        """
        Initialize the USNAN client
        
        Args:
            base_url: Base URL for the USNAN API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        
        # Initialize session
        self.session = requests.Session()
        
        # Initialize endpoints
        self.datasets = DatasetsEndpoint(self)
        self.facilities = FacilitiesEndpoint(self)
        self.spectrometers = SpectrometerEndpoint(self)
        self.probes = ProbesEndpoint(self)
    
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
        
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
