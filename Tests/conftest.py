import pytest
from flask import Flask
from Models.models import Receipt, db
from app import app as flask_app
import logging

"""to run test in terminal: python3 -m pytest -s -v or python -m pytest -s -v"""
@pytest.fixture
def app():
    """Set up Flask app for testing."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture(scope='session')
def logger():
    # Sun 15 Sep: logger not working.... ...if possible someone fix this logger ...
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler('test.log')
                        ])

    logger = logging.getLogger()
    logger.info("Logger is working.")
    return logger

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Initialize the database with some data if theres any..."""
    r_arr = []
    r_arr.append(Receipt(date="2022-01-01", category="Food", total_amount=15.0, status="unverified"))
    r_arr.append( Receipt(date="2022-02-01", category="Dining", total_amount=20.0, status="unverified"))
    r_arr.append( Receipt(date="2022-03-01", category="Food", total_amount=25.0, status="unverified"))
    r_arr.append( Receipt(date="2022-04-01", category="Food", total_amount=30.0, status="verified"))
    r_arr.append( Receipt(date="2022-05-01", category="Food", total_amount=35.0, status="verified"))
    
    r_arr.append(Receipt(date="2022-01-02", category="Toll", total_amount=16.0, status="verified"))
    r_arr.append(Receipt(date="2022-02-02", category="Gas", total_amount=40.0, status="verified"))
    r_arr.append(Receipt(date="2022-03-02", category="Gas", total_amount=50.0, status="verified"))
    r_arr.append(Receipt(date="2022-04-02", category="Gas", total_amount=60.0, status="unverified"))
    r_arr.append(Receipt(date="2022-05-02", category="Hotel", total_amount=66.0, status="unverified"))

    for r in r_arr:
        db.session.add(r)
    yield db
    db.session.remove()
    db.drop_all()
