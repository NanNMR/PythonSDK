"""Spectrometers endpoint implementation"""

from typing import List, Dict
from .base import BaseEndpoint
from usnan_sdk.models.spectrometers import Spectrometer


class SpectrometerEndpoint(BaseEndpoint):
    """Endpoint for managing spectrometers"""

    _spectrometers: List[Spectrometer]
    _spectrometers_map: Dict[str, Spectrometer]

    def __init__(self, client):
        super().__init__(client)
        self._spectrometers: List[Spectrometer] = []
        self._spectrometers_map: Dict[str, Spectrometer] = {}

    def list(self) -> List[Spectrometer]:
        """
        List all spectrometers
        
        Returns:
            List of Spectrometer objects
        """
        if self._spectrometers:
            return self._spectrometers
        else:
            response = self._get('/nan/public/instruments')
            facilities = [Spectrometer.from_dict(self.client, item) for item in response]
            self._spectrometers_map = {_.identifier: _ for _ in facilities}
            self._spectrometers = facilities
            return facilities

    def get(self, spectrometer_id: str) -> Spectrometer:
        """
        Get a specific spectrometer by ID
        
        Args:
            spectrometer_id: The spectrometer ID
            
        Returns:
            Spectrometer object
        """
        if not self._spectrometers_map:
            self.list()
        if spectrometer_id not in self._spectrometers_map:
            raise KeyError(f'Unknown spectrometer identifier: {spectrometer_id}')
        return self._spectrometers_map[spectrometer_id]
