from scripts.unsplash_api import get_resolutions, search_images
from scripts.progres_counter import ProgresCounter
import pytest
import requests
import scripts.unsplash_api as unsplash


def test_get_resolutions_extended():
    assert get_resolutions() == [
        'small',
        'regular',
        'full',
        'raw'
    ]


progress = ProgresCounter(0, 100)
progress.set_new_task('test', 1)


def test_search_images_api_connection():
    images = search_images('cat', 10, 'small', progress)
    assert len(images) == 10


class FakeResponse:
    def __init__(self, json) -> None:
        self._json = json

    def json(self):
        return self._json


def fake_images_api_get(*args, **kwargs):
    json = {
            'results': [
                {},
                {}
            ]
        }
    return FakeResponse(json)


def fake_image_download(image, resolution, alternative_name):
    return (alternative_name, None)


def test_search_images_incorrect_api_result(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: '')
    with pytest.raises(unsplash.IncorrectPageResultExpection):
        search_images('cat', 2, 'small', progress)


def test_search_images_result(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_images_api_get)
    monkeypatch.setattr(unsplash, "_download_image", fake_image_download)
    quary = 'cat'
    result = search_images(quary, 2, 'small', progress)
    assert len(result) == 2
    assert result[0][0] == quary
    assert result[0][1] is None


def test_search_images_invalid_input():
    with pytest.raises(unsplash.IncorrectQueryExpection):
        search_images(None, 1, 'small', progress)

    with pytest.raises(unsplash.IncorrectQueryExpection):
        search_images('', 1, 'small', progress)

    with pytest.raises(unsplash.IncorrectQueryExpection):
        search_images('test', -1, 'small', progress)

    with pytest.raises(unsplash.IncorrectResolutionExpection):
        search_images('test', 1, 'invalid', progress)

    with pytest.raises(AttributeError):
        search_images('test', 1, 'small', None)
