import dataclasses
import json
from collections import defaultdict
from typing import Any, Dict, List, Literal, Optional, overload

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

    def __str__(self) -> str:
        """Return a string summary of the search configuration"""
        parts = []
        
        # Add filter summary
        if self.filters:
            filter_parts = []
            for field, filter_list in self.filters.items():
                field_conditions = []
                for filter_meta in filter_list:
                    if filter_meta.match_mode in ('isNull', 'isNotNull'):
                        condition = f"{field} {filter_meta.match_mode}"
                    else:
                        condition = f"{field} {filter_meta.match_mode} '{filter_meta.value}'"
                    field_conditions.append(condition)
                
                # Join conditions for this field with the operator
                if len(field_conditions) > 1:
                    operator = filter_list[0].operator  # All filters for a field have same operator
                    field_summary = f"({f' {operator} '.join(field_conditions)})"
                else:
                    field_summary = field_conditions[0]
                filter_parts.append(field_summary)
            
            parts.append(f"Filters: {' AND '.join(filter_parts)}")
        else:
            parts.append("Filters: None")
        
        # Add pagination info
        parts.append(f"Records: {self.records}, Offset: {self.offset}")
        
        # Add sorting info
        if self.sort_field:
            parts.append(f"Sort: {self.sort_field} {self.sort_order}")
        else:
            parts.append("Sort: None")
        
        return f"SearchConfig({', '.join(parts)})"

    @overload
    def add_filter(self, field: str, *, match_mode: Literal['isNull', 'isNotNull'], operator: OperatorMode = 'AND') -> 'SearchConfig':
        ...

    @overload
    def add_filter(self, field: str, *, value: Any, match_mode: MatchMode = 'equals', operator: OperatorMode = 'AND') -> 'SearchConfig':
        ...

    def add_filter(self, field: str, *, value: Any = None, match_mode: MatchMode = 'equals', operator: OperatorMode = 'AND') -> 'SearchConfig':
        """
        Add a single filter for a field

        Args:
            field: The field name to filter on
            value: The value to filter by (optional for 'isNull' and 'isNotNull' match modes)
            match_mode: The match mode (e.g., 'contains', 'equals', 'startsWith')
            operator: The operator (e.g., 'and', 'or')

        Returns:
            Self for method chaining
        """
        # For isNull and isNotNull, value should be None
        if match_mode in ('isNull', 'isNotNull') and value is not None:
            value = None
        
        filter_meta = FilterMetadata(value=value, match_mode=match_mode, operator=operator)
        existing_field_filters = self.filters[field]
        for field in existing_field_filters:
            if field.operator != operator:
                raise ValueError(f'Cannot have homogeneous operators for the same field. Field: "{field}. Previous operator: "{field.operator}". Current field operator: "{operator}"')
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

    def clone(self) -> 'SearchConfig':
        """
        Clones this object so that it can be used to keep track of results as they are fetched (or for other purposes).

        Returns:
             A search config object with the same exact attributes.
        """

        new_config = SearchConfig(records=self.records, offset=self.offset, sort_order=self.sort_order, sort_field=self.sort_field)
        new_config.filters = self.filters.copy()
        return new_config
