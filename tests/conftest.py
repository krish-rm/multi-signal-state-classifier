"""Test configuration and fixtures."""

import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_data_dir():
    """Create test data directory."""
    dir_path = "data/test"
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


