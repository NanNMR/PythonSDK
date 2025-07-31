"""
Test file for USNANClient probes functionality.
"""

import pytest
import usnan_sdk


def test_get_single_dataset():
    """ Ensure we can get a single dataset by ID."""

    client = usnan_sdk.USNANClient()
    d = client.datasets.get(363067)
    assert isinstance(d, usnan_sdk.models.Dataset)
    assert isinstance(d.facility, usnan_sdk.models.Facility)
    assert isinstance(d.spectrometer, usnan_sdk.models.Spectrometer)
    assert isinstance(d.spectrometer.installed_probe, usnan_sdk.models.Probe) or d.spectrometer.installed_probe is None

def test_search():
    """ Ensure that getting datasets via search works, including fetching all of them. """

    client = usnan_sdk.USNANClient()
    g = client.datasets.search(usnan_sdk.models.SearchConfig().add_filter('is_knowledgebase', value=True, match_mode='equals'))

    count = 0
    for x in range(0,1001):
        try:
            next(g)
            count += 1
        except StopIteration:
            break

    assert count > 25

def test_errors():
    """ Check that some errors are raised as they should be. """

    client = usnan_sdk.USNANClient()

    # Test that invalid filter name raises RuntimeError
    with pytest.raises(RuntimeError):
        d = client.datasets.search(usnan_sdk.models.SearchConfig().add_filter('is_knowlsedgebase', value=True, match_mode='equals'))
        print(next(d))

    # Test that mismatched filters cannot be applied
    with pytest.raises(ValueError):
        usnan_sdk.models.SearchConfig().add_filter('test', value=True, operator='OR').add_filter('test', value=True, operator='AND')
