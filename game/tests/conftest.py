import json

import pytest
from services.okved_mather import OkvedMatcher


@pytest.fixture
def mock_data():
    return [
        {"code": "26515", "original_code": "26.51.5", "name": "Приборы"},
        {"code": "0111", "original_code": "01.11", "name": "Пшеница"},
    ]


@pytest.fixture
def matcher(mock_data):
    return OkvedMatcher(mock_data)


@pytest.fixture
def mock_okved_file(tmp_path):
    file_path = tmp_path / "okved_cache.json"
    mock_data = [{"code": "01", "name": "Test"}]
    file_path.write_text(json.dumps(mock_data))
    return str(file_path)
