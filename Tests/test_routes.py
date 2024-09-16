

def test_api_get_index(client):
    response = client.get('/initx')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 200
    assert json_data['message'] == "Init System! - 200 OK"
    assert json_data['data'] is None
    assert json_data['messages'] == []

def test_api_get_receipts(client):
    response = client.get('/receipts')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 200
    assert json_data['message'] is None
    assert json_data['data'] is None
    assert json_data['messages'] == []

    response = client.get('/receipts/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 200
    assert json_data['message'] is None
    assert json_data['data'] is None
    assert json_data['messages'] == []

    response = client.get('/receipts/2')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['code'] == 200
    assert json_data['message'] is None
    assert json_data['data'] is None
    assert json_data['messages'] == []