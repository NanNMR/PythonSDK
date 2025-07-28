"""Datasets endpoint implementation"""

from typing import List, Optional, Dict, Any
from .base import BaseEndpoint
from ..models.dataset import Dataset


class DatasetsEndpoint(BaseEndpoint):
    """Endpoint for managing datasets"""
    
    def list(self, 
             limit: Optional[int] = None,
             offset: Optional[int] = None,
             sort_by: Optional[str] = None,
             sort_order: Optional[str] = None,
             filters: Optional[Dict[str, Any]] = None) -> List[Dataset]:
        """
        List datasets with optional filtering, sorting, and pagination
        
        Args:
            limit: Maximum number of results to return
            offset: Number of results to skip
            sort_by: Field to sort by
            sort_order: Sort order ('asc' or 'desc')
            filters: Dictionary of filters to apply
            
        Returns:
            List of Dataset objects
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        if sort_by:
            params['sort_by'] = sort_by
        if sort_order:
            params['sort_order'] = sort_order
        if filters:
            params.update(filters)
        
        response = self._get('/nan/data-browser/experiment', params=params)
        return [Dataset.from_dict(self, item) for item in response.get('data', [])]
    
    def get(self, dataset_id: str) -> Dataset:
        """
        Get a specific dataset by ID

        Args:
            dataset_id: The dataset ID

        Returns:
            Dataset object
        """
        #dataset_id
        response = self._get(f'/nan/data-browser/experiment',)
        return Dataset.from_dict(response)


class FilterMetadata:
    """Represents a single filter condition"""
    
    def __init__(self, value: Any = None, match_mode: str = None, operator: str = None):
        self.value = value
        self.match_mode = match_mode
        self.operator = operator
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = {}
        if self.value is not None:
            result['value'] = self.value
        if self.match_mode is not None:
            result['matchMode'] = self.match_mode
        if self.operator is not None:
            result['operator'] = self.operator
        return result


class SearchBuilder:
    """Builder class for creating TableFilterMetadata objects"""
    
    def __init__(self):
        self.filters: Dict[str, Any] = {}
    
    def add_filter(self, field: str, value: Any = None, match_mode: str = None, operator: str = None) -> 'SearchBuilder':
        """
        Add a single filter for a field
        
        Args:
            field: The field name to filter on
            value: The value to filter by
            match_mode: The match mode (e.g., 'contains', 'equals', 'startsWith')
            operator: The operator (e.g., 'and', 'or')
            
        Returns:
            Self for method chaining
        """
        filter_meta = FilterMetadata(value, match_mode, operator)
        self.filters[field] = filter_meta.to_dict()
        return self
    
    def add_multiple_filters(self, field: str, filters: List[FilterMetadata]) -> 'SearchBuilder':
        """
        Add multiple filters for a single field
        
        Args:
            field: The field name to filter on
            filters: List of FilterMetadata objects
            
        Returns:
            Self for method chaining
        """
        self.filters[field] = [f.to_dict() for f in filters]
        return self
    
    def build(self) -> Dict[str, Any]:
        """
        Build the final TableFilterMetadata object
        
        Returns:
            Dictionary representing TableFilterMetadata
        """
        return self.filters.copy()
    
    def clear(self) -> 'SearchBuilder':
        """
        Clear all filters
        
        Returns:
            Self for method chaining
        """
        self.filters.clear()
        return self


def create_search() -> SearchBuilder:
    """
    Create a new SearchBuilder instance
    
    Returns:
        New SearchBuilder instance
    """
    return SearchBuilder()


def create_filter(value: Any = None, match_mode: str = None, operator: str = None) -> FilterMetadata:
    """
    Create a FilterMetadata object
    
    Args:
        value: The value to filter by
        match_mode: The match mode (e.g., 'contains', 'equals', 'startsWith')
        operator: The operator (e.g., 'and', 'or')
        
    Returns:
        FilterMetadata object
    """
    return FilterMetadata(value, match_mode, operator)


