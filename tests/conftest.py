"""
PyTest configuration and fixtures for testing
"""
import pytest
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def mongodb_uri():
    """Get MongoDB URI from environment"""
    return os.getenv('MONGODB_URI', 'mongodb://localhost:27017/?replicaSet=rs0')


@pytest.fixture(scope="session")
def db_name():
    """Get database name from environment"""
    return os.getenv('MONGODB_DB_NAME', 'testdb')


@pytest.fixture(scope="session")
def mongo_client(mongodb_uri):
    """Create MongoDB client"""
    client = MongoClient(mongodb_uri)
    yield client
    client.close()


@pytest.fixture(scope="function")
def test_collection(mongo_client, db_name):
    """Provide a clean test collection for each test"""
    db = mongo_client[db_name]
    collection = db['test_collection']
    
    # Clear collection before test
    collection.delete_many({})
    
    yield collection
    
    # Clear collection after test
    collection.delete_many({})


@pytest.fixture(scope="session", autouse=True)
def setup_observability():
    """Initialize observability for tests"""
    from backend.observability import initialize_observability
    initialize_observability()
    return True
