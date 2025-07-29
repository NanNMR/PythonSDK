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
            response = self._get('/nan/data-browser/experiment', params=config_copy.build())
            for item in response.get('experiments', []):
                yield Dataset.from_dict(self.client, item)
            if response.get('last_page'):
                raise StopIteration
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
        search_object = SearchConfig().add_filter('id', value=dataset_id, match_mode='equals')
        response = self._get(f'/nan/data-browser/experiment', params=search_object.build())

        experiments = response.get('experiments', [])
        if len(experiments) == 0:
            raise KeyError('Invalid dataset ID (or the specified dataset is not public.')
        if len(experiments) > 1:
            raise KeyError('Error when fetching dataset: more than one dataset found where one was expected.')

        return Dataset.from_dict(self.client, experiments[0])
