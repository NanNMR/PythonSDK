# USNAN SDK

Python SDK for interacting with the USNAN API.

## Installation

```bash
pip install usnan-sdk
```

## Usage

```python
from usnan_sdk import USNANClient

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
