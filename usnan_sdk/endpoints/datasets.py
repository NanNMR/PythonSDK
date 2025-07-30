"""Datasets endpoint implementation"""
import concurrent.futures
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
        next_batch_future = None
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        def fetch_batch(config):
            """Helper function to fetch a batch of data"""
            return self._get('/nan/public/datasets/search', params=config.build())

        try:
            while True:
                # Get current batch (either first request or from prefetched future)
                if next_batch_future is None:
                    response = fetch_batch(config_copy)
                else:
                    response = next_batch_future.result()
                
                # Prepare next batch config before yielding current results
                next_config = config_copy.clone()
                next_config.offset += next_config.records
                
                # Double the amount of records fetched at a time each time they are exhausted, but don't
                #  fetch more than 1000 at a time.
                if next_config.records < 1000:
                    new_records = int(next_config.records * 2)
                    next_config.records = new_records
                    if new_records > 1000:
                        next_config.records = 1000

                # Start prefetching next batch if not on last page
                if not response.get('last_page'):
                    next_batch_future = executor.submit(fetch_batch, next_config)
                else:
                    next_batch_future = None

                # Yield current batch results
                for item in response.get('experiments', []):
                    yield Dataset.from_dict(self.client, item)
                
                if response.get('last_page'):
                    return
                
                config_copy = next_config
        finally:
            executor.shutdown(wait=False)
    
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
