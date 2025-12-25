import json

import pytest
from pytest_mock import MockerFixture
from services.uploader import GitHubClient


@pytest.mark.asycncio
async def test_upload(mocker: MockerFixture, mock_okved_file) -> None:
    client = GitHubClient()
    mock_response_data = [{"code": "01", "name": "Test"}]
    mocker.patch(
        "services.uploader.GitHubClient.get_okved_data",
        return_value=mock_response_data,
    )
    response = await client.get_okved_data()
    assert response == mock_response_data

    with open(mock_okved_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        assert saved_data == mock_response_data
