"""Datasets endpoint implementation"""
from typing import List

from .base import BaseEndpoint
from ..models.dataset import Dataset
from ..models.search import SearchConfig


class DatasetsEndpoint(BaseEndpoint):
    """Endpoint for managing datasets"""
    
    def search(self, search_config: SearchConfig) -> List[Dataset]:
        """
        List datasets with optional filtering, sorting, and pagination
        
        Args:
            search_config: Search configuration object
            
        Returns:
            List of Dataset objects
        """
        
        response = self._get('/nan/data-browser/experiment', params=search_config.build())
        return [Dataset.from_dict(self.client, item) for item in response.get('data', [])]
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a specific dataset by ID

        Args:
            dataset_id: The dataset ID

        Returns:
            Dataset object
        """
        search_object = SearchConfig().add_filter('id', value=dataset_id, match_mode='equals')
        response = self._get(f'/nan/data-browser/experiment', params=search_object.build())

        if len(response.get('experiments', [])) == 0:
            raise KeyError('Invalid dataset ID (or the specified dataset is not public.')

        return Dataset.from_dict(self.client, response['experiments'][0])
