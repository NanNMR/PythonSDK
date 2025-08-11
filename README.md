# USNAN SDK

Python SDK for interacting with the USNAN API. See the full documentation at [ReadTheDocs](https://pythonsdk.readthedocs.io/en/latest/index.html).

## Installation

```bash
pip install usnan
```

## Usage

```python
from usnan import USNANClient

# Initialize the client
client = USNANClient()

# Get datasets
datasets = client.datasets.list()

# Get facilities
facilities = client.facilities.list()

# Get spectrometers
spectrometers = client.spectrometers.list()

# Get probes
probes = client.probes.list()
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```
