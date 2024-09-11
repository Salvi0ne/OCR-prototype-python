from Routes.route import main_blueprint
from flask import Flask
import pytest

@pytest.fixture
def client():
        app = Flask(__name__)
        app.register_blueprint(main_blueprint)
        app.testing = True
        with app.test_client() as client:
            yield client

def test_initx_route(client):
        response = client.get('/initx')
        assert response.status_code == 200
        assert response.data == b'Init System! - 200 OK'
