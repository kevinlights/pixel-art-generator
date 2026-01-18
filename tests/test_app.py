import pytest
import sys
import os

# Add the project root to the path so we can import modules
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# Import after path setup
from api.main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    # Configure the root path for serving static files
    import pathlib
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.config['ROOT_PATH'] = root_dir
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Pixel Art Generator' in response.data


def test_generate_endpoint_exists(client):
    """Test that the generate endpoint exists."""
    # We can't fully test the generation without external services,
    # but we can test that the endpoint exists and returns the right error for missing data
    response = client.post('/generate', json={})
    # Should return 400 for missing prompt, or 500 for generation failure
    assert response.status_code in [400, 500]