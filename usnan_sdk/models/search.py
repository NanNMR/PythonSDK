import dataclasses
import json
from collections import defaultdict
from typing import Any, Dict, List, Literal, Optional

MatchMode = Literal['equals','notEquals', 'startsWith', 'endsWith', 'contains', 'similarTo', 'notContains', 'isNull', 'isNotNull', 'greaterThan', 'lessThan', 'includes', 'notIncludes']
OperatorMode = Literal['OR', 'AND']
SortOrder = Literal['ASC', 'DESC']

@dataclasses.dataclass
class FilterMetadata:
    """Represents a single filter condition"""

    def __init__(self, *,
                 value: Any,
                 match_mode: MatchMode = 'equals',
                 operator: OperatorMode = 'AND'):
        self.value = value
        self.match_mode = match_mode
        self.operator = operator

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {'value': self.value, 'matchMode': self.match_mode, 'operator': self.operator}


class SearchConfig:
    """Builder class for creating TableFilterMetadata objects"""

    records: int = 25
    offset: int = 0
    sort_order: SortOrder = 'ASC'
    sort_field: Optional[str] = None

    def __init__(self,
                 records: int = 25,
                 offset: int = 0,
                 sort_order: SortOrder = 'ASC',
                 sort_field: Optional[str] = None):
        self.filters: Dict[str, List[FilterMetadata]] = defaultdict(list)
        self.records = records
        self.offset = offset
        self.sort_order = sort_order
        self.sort_field = sort_field

    def add_filter(self, field: str, value: Any, match_mode: MatchMode = 'equals', operator: OperatorMode = 'AND') -> 'SearchConfig':
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
        filter_meta = FilterMetadata(value=value, match_mode=match_mode, operator=operator)
        existing_field_filters = self.filters[field]
        for field in existing_field_filters:
            if field.operator != operator:
                raise ValueError('Cannot have homogeneous operators for the same field.')
        existing_field_filters.append(filter_meta)
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build the final TableFilterMetadata object

        Returns:
            Dictionary representing TableFilterMetadata
        """

        filters_dict = {key: [_.to_dict() for _ in value] for key, value in self.filters.items()}

        return {'filters': json.dumps(filters_dict),
                'offset': self.offset,
                'sort_order': self.sort_order,
                'sort_field': self.sort_field,
                'records': self.records}
