from midterm import read_data_from_file_into_dict, positional_epochs, epoch_data, print_countries, country_data, get_regions, region_data, get_cities, city_data
import pytest
from flask import Flask, request
import requests
import xmltodict
from midterm import app

@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client

def test_read_data_from_file_into_dict():
    x = read_data_from_file_into_dict()
    assert x == 'Data has been read from file\n'

def test_print_countries(client):
    resp = client.get('/countries')
    assert b'United_States' in resp.data

def test_positional_epochs(client):
    with open('ISS.OEM_J2K_EPH.xml', 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read())
        assert len(iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector'])==5524

def test_epoch_data(client):
    resp = client.get('/epochs/?epoch=2022-042T12:00:00.000Z')
    assert b'Epoch:' in resp.data

def test_country_data(client):
    resp = client.get('/countries/?country=United_States')
    assert b'Texas' in resp.data

def test_get_regions(client):
    resp = client.get('/regions/?country=United_States')
    assert b'Texas' in resp.data

def test_region_data(client):
    resp = client.get('/regions/data/?region=Texas')
    assert b'Austin' in resp.data

def test_get_cities(client):
    resp = client.get('/cities/?country=United_States&region=Texas')
    assert b'Austin' in resp.data

def test_city_data(client):
    resp = client.get('/cities/data/?city=Austin')
    assert b'Texas' in resp.data

def test_userguide(client):
    resp = client.get('/')
    assert b'Once' in resp.data
pytest.main()
