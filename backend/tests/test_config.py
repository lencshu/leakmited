# tests/test_config.py
import pytest
import os
from unittest.mock import patch

from src.core.config import Settings


@pytest.mark.sls
def test_config_env_loaded():
    s = Settings()
    assert s.DB_HOST is not None
    assert s.DB_PORT is not None
    assert s.DB_NAME is not None
    assert s.DB_USER is not None
    assert s.DB_PASS is not None
