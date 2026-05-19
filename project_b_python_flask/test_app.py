import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'UP'
    assert 'timestamp' in json_data

def test_greet_endpoint_default(client):
    rv = client.get('/api/greet')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['message'] == 'Hello, Developer!'
    assert json_data['success'] is True

def test_greet_endpoint_with_name(client):
    rv = client.get('/api/greet?name=Roshan')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['message'] == 'Hello, Roshan!'

def test_compute_endpoint(client):
    payload = {"number": 100}
    rv = client.post('/api/compute', 
                     data=json.dumps(payload),
                     content_type='application/json')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['input'] == 100
    assert json_data['processed'] is True
    assert 'result' in json_data
