"""pytest configuration and shared fixtures"""

import pytest


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test",
    )
    config.addinivalue_line(
        "markers",
        "acceptance: mark test as an acceptance test",
    )
