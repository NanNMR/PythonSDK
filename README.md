# USNAN SDK

Python SDK for interacting with the USNAN API.

## Installation

```bash
pip install usnan
```

## Quick Start

```python
import usnan

client = usnan.USNANClient()

# Search public datasets
config = usnan.models.SearchConfig().add_filter('is_knowledgebase', value=True, match_mode='equals')
for dataset in client.datasets.search(config):
    print(dataset)
```

## Authentication

Authenticate with your NMR Hub account to access additional datasets:

```python
# Browser-based login (opens browser, SSO)
client.login()

# Device authorization (for headless/remote environments)
client.login(method='device')

# Direct token (for automation)
client.login(method='token', token='eyJ...')
```

Your session is saved locally and restored automatically on future runs. Call `client.logout()` to revoke it.

## Documentation

See the full documentation at [ReadTheDocs](https://pythonsdk.readthedocs.io/en/latest/index.html).

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```
