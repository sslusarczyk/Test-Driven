import pytest
from main import app
from unittest.mock import Mock

@pytest.mark.parametrize("list_type", ["popular", "top_rated", "upcoming", "now_playing"])
def test_homepage_with_different_list_types(monkeypatch, list_type):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(f'/?list_type={list_type}')
        assert response.status_code == 200
        api_mock.assert_called_once_with(f'movie/{list_type}')