"""Datasets endpoint implementation"""
from typing import Generator

from .base import BaseEndpoint
from ..models.dataset import Dataset
from ..models.search import SearchConfig


class DatasetsEndpoint(BaseEndpoint):
    """Endpoint for managing datasets"""

    def search(self, search_config: SearchConfig) -> Generator[Dataset, None, None]:
        """
        Search datasets according to parameters in the search_config object.
        
        Args:
            search_config: Search configuration object
            
        Returns:
            Generator of Dataset objects
        """

        config_copy: SearchConfig = search_config.clone()

        while True:
            response = self._get('/nan/public/datasets/search', params=config_copy.build())
            for item in response.get('experiments', []):
                yield Dataset.from_dict(self.client, item)
            if response.get('last_page'):
                return
            config_copy.offset += config_copy.records

            # Double the amount of records fetched at a time each time they are exhausted, but don't
            #  fetch more than 1000 at a time.
            if config_copy.records < 1000:
                new_records = int(config_copy.records * 2)
                config_copy.records = new_records
                if new_records > 1000:
                    config_copy.new_records = 1000
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a specific dataset by ID

        Args:
            dataset_id: The dataset ID

        Returns:
            Dataset object
        """
        experiment = self._get(f'/nan/public/datasets/{dataset_id}')
        return Dataset.from_dict(self.client, experiment)
