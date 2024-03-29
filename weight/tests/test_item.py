import requests
import os

URI = os.environ.get('URI')


def test_get_item():
    response = requests.get(URI + "/item/T-123523?from=19990101010101")
    assert response.status_code == 200


def test_get_item_with_wrong_from():
    response = requests.get(URI + "/item/T-123523?from=skjdf")
    assert response.status_code == 404


def test_get_item_with_wrong_id():
    response = requests.get(URI + "/item/T-15kjhj23?from=19990101010101")
    assert response.status_code == 404


def test_get_item_with_wrong_to():
    response = requests.get(URI + "/item/T-123523?to=sdkjfsdn")
    assert response.status_code == 404
