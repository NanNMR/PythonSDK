from dataclasses import dataclass
from typing import Optional, Dict, Any, List

import usnan_sdk


@dataclass
class Dimension:
    """Represents a dimension in a dataset"""
    dimension: int
    nucleus: str
    is_direct: bool
    spectral_width: Optional[float] = None
    maximum_evolution_time: Optional[float] = None
    num_points: Optional[int] = None

    def __str__(self) -> str:
        """Return a string representation of the dimension"""
        parts = [f"Dimension {self.dimension}: {self.nucleus}"]

        if self.is_direct:
            parts.append("(direct)")
        else:
            parts.append("(indirect)")

        specs = []
        if self.spectral_width:
            specs.append(f"SW: {self.spectral_width} Hz")
        if self.num_points:
            specs.append(f"Points: {self.num_points}")
        if self.maximum_evolution_time:
            specs.append(f"Max evolution: {self.maximum_evolution_time} s")

        if specs:
            parts.append(f"[{', '.join(specs)}]")

        return " ".join(parts)

    def __repr__(self) -> str:
        """Return a concise representation of the dimension"""
        return f"Dimension({self.dimension}, '{self.nucleus}', direct={self.is_direct})"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Dimension':
        return cls(
            dimension=data['dimension'],
            nucleus=data['nucleus'],
            is_direct=data['is_direct'],
            spectral_width=data.get('spectral_width'),
            maximum_evolution_time=data.get('maximum_evolution_time'),
            num_points=data.get('num_points')
        )


@dataclass
class DatasetVersion:
    """Represents a version of an experiment"""
    id: int
    version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatasetVersion':
        return cls(
            id=data['id'],
            version=data.get('version')
        )


@dataclass
class Dataset:
    """Represents a dataset in the system"""

    id: int
    _initialized: bool = False
    _client: 'usnan_sdk.USNANClient' = None
    dataset_name: Optional[str] = None
    identifier: Optional[str] = None
    tags: Optional[List[str]] = None
    title: Optional[str] = None
    version: Optional[str] = None
    public_time: Optional[str] = None
    published_ts: Optional[str] = None
    state: Optional[str] = None
    person_id: Optional[int] = None
    pulse_sequence: Optional[str] = None
    experiment_start_time: Optional[str] = None
    sample_id: Optional[str] = None
    solvent: Optional[str] = None
    temperature_k: Optional[float] = None
    is_non_uniform: Optional[bool] = None
    is_locked: Optional[bool] = None
    sample_sparsity: Optional[str] = None
    num_dimension: Optional[int] = None
    num_dimension_collected: Optional[int] = None
    experiment_end_time: Optional[str] = None
    workstation_user: Optional[str] = None
    experiment_name: Optional[str] = None
    session_id: Optional[int] = None
    pi_id: Optional[int] = None
    mas_rate: Optional[float] = None
    z0_drift_correction: Optional[bool] = None
    mixing_sequence: Optional[str] = None
    mixing_time: Optional[float] = None
    decoupling_sequence: Optional[str] = None
    is_multi_receiver: Optional[bool] = None
    time_shared: Optional[bool] = None
    classification: Optional[str] = None
    notes: Optional[str] = None
    preferred: Optional[bool] = None
    spectrometer: 'usnan_sdk.models.Spectrometer' = None
    facility: 'usnan_sdk.models.Facility' = None

    # Computed/derived fields (prefixed with _)
    _is_public: Optional[bool] = None
    _num_in_set: Optional[int] = None
    _source: Optional[str] = None
    _perm_reason: Optional[str] = None
    _perm_write: Optional[bool] = None
    _perm_make_public: Optional[bool] = None
    _pi_name: Optional[str] = None
    _nan_person_name: Optional[str] = None
    _field_strength_mhz: Optional[float] = None
    _facility_short_name: Optional[str] = None
    _direct_detection_nucleus: Optional[str] = None
    _nuclei: Optional[str] = None
    _session_start: Optional[str] = None
    _session_finish: Optional[str] = None
    _sample_name: Optional[str] = None
    _copied_to_nmrbox: Optional[bool] = None

    # Related objects
    dimensions: Optional[List[Dimension]] = None
    _versions: Optional[List[DatasetVersion]] = None

    @classmethod
    def from_dict(cls, client: 'usnan_sdk.USNANClient', data: Dict[str, Any]) -> 'Dataset':
        """Create a Dataset instance from API response data"""

        return cls(
            # Core fields
            id=data['id'],
            _client=client,
            _initialized=True,
            dataset_name=data.get('dataset_name'),
            identifier=data.get('identifier'),
            tags=data.get('tags'),
            title=data.get('title'),
            version=data.get('version'),
            public_time=data.get('public_time'),
            published_ts=data.get('published_ts'),
            state=data.get('state'),

            # Dataset details
            person_id=data.get('person_id'),
            pulse_sequence=data.get('pulse_sequence'),
            experiment_start_time=data.get('experiment_start_time'),
            sample_id=data.get('sample_id'),
            solvent=data.get('solvent'),
            temperature_k=data.get('temperature_k'),
            is_non_uniform=data.get('is_non_uniform'),
            is_locked=data.get('is_locked'),
            sample_sparsity=data.get('sample_sparsity'),
            num_dimension=data.get('num_dimension'),
            num_dimension_collected=data.get('num_dimension_collected'),
            experiment_end_time=data.get('experiment_end_time'),
            workstation_user=data.get('workstation_user'),
            experiment_name=data.get('experiment_name'),
            session_id=data.get('session_id'),
            pi_id=data.get('pi_id'),

            # Additional fields
            mas_rate=data.get('mas_rate'),
            z0_drift_correction=data.get('z0_drift_correction'),
            mixing_sequence=data.get('mixing_sequence'),
            mixing_time=data.get('mixing_time'),
            decoupling_sequence=data.get('decoupling_sequence'),
            is_multi_receiver=data.get('is_multi_receiver'),
            time_shared=data.get('time_shared'),
            classification=data.get('classification'),
            notes=data.get('notes'),
            preferred=data.get('preferred'),
            spectrometer=usnan_sdk.models.Spectrometer.from_identifier(client, data.get('_spectrometer_identifier'), data.get('spectrometer_name')),
            facility=usnan_sdk.models.Facility.from_identifier(client, data.get('_facility_identifier')),

            # Computed fields
            _is_public=data.get('_is_public'),
            _num_in_set=data.get('_num_in_set'),
            _source=data.get('_source'),
            _perm_reason=data.get('_perm_reason'),
            _perm_write=data.get('_perm_write'),
            _perm_make_public=data.get('_perm_make_public'),
            _pi_name=data.get('_pi_name'),
            _nan_person_name=data.get('_nan_person_name'),
            _field_strength_mhz=data.get('_field_strength_mhz'),
            _facility_short_name=data.get('_facility_short_name'),
            _direct_detection_nucleus=data.get('_direct_detection_nucleus'),
            _nuclei=data.get('_nuclei'),
            _session_start=data.get('_session_start'),
            _session_finish=data.get('_session_finish'),
            _sample_name=data.get('_sample_name'),
            _copied_to_nmrbox=data.get('_copied_to_nmrbox'),

            # Related objects
            dimensions=[Dimension.from_dict(d) for d in data.get('dimensions', [])],
            _versions=[DatasetVersion.from_dict(v) for v in data.get('_versions', [])]
        )

    @classmethod
    def from_identifier(cls, client: 'usnan_sdk.USNANClient', identifier: int) -> 'Dataset':
        return cls(id=identifier, _initialized=False, _client=client)


    def __getattribute__(self, name):
        # Always allow access to private attributes and methods to avoid infinite recursion
        if name.startswith('_'):
            return super().__getattribute__(name)

        # Auto-initialize if not already initialized
        if not super().__getattribute__('_initialized'):
            # Load the full data from the API
            full_spectrometer = super().__getattribute__('_client').datasets.get(super().__getattribute__('id'))
            # Copy all the loaded data to this instance
            for key, value in full_spectrometer.__dict__.items():
                if not key.startswith('_'):
                    setattr(self, key, value)
            super().__setattr__('_initialized', True)

        return super().__getattribute__(name)

    def __repr__(self) -> str:
        """Return a concise representation of the dataset"""
        return f"Dataset('{self.id}')"
