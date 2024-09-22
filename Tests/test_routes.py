

# from Models.models import Receipt, db
from Models.models import Receipt
from constant import BASED_URL

def test_api_get_index(client):
    """
    Test that the API responds with a "200 OK" message when the /initx endpoint is called.
    """
    response = client.get(BASED_URL+'initx')
    json_data = response.get_json()
    assert json_data['code'] == 200
    assert json_data['message'] == "Init System! - 200 OK"
    assert json_data['data'] is None
    assert json_data['messages'] == []


def test_api_get_receipts_by_status_unverified(client,init_database):
    """
    Test api_get_receipts_by_status unverified
    """
    db = init_database
    response = client.get(f"{BASED_URL}receipts/unverified")
    json_data = response.get_json()
    # receipt_count = db.session.query(Receipt).count()
    assert 5 ==  len(json_data['data'])

def test_api_get_receipts_by_status_verified(client,init_database):
    """
      Test api_get_receipts_by_status verified
    """
    db = init_database
    response = client.get(f"{BASED_URL}receipts/verified")
    json_data = response.get_json()
    # receipt_count = db.session.query(Receipt).count()
    assert 5 ==  len(json_data['data'])


def test_extract_receipts(client,init_database):
    """a bit challenging because it required image or a uri..."""
    pass

# def test_something(init_database):
#     db = init_database
#     assert db is not None
#     print(":::", db.session.query(Receipt).count())
