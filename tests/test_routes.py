import pytest
from app import create_app, db

# Pytest fixture to create a test client for the Flask app
@pytest.fixture
def client():
    # Create the Flask app instance using your factory function
    app = create_app()
    
    # Enable testing mode in Flask 
    app.config['TESTING'] = True

    # Push an application context to allow DB operations during testing
    with app.app_context():
        

        # Yield the test client instance to the test functions
        yield app.test_client()

        

# Test the GET /classes endpoint
def test_get_classes(client):
    # Send a GET request to /classes
    response = client.get('/classes')
    
    # Assert that the HTTP response status code is 200 OK
    assert response.status_code == 200
    
    # Assert that the response JSON is a list (of fitness classes)
    assert isinstance(response.json, list)

# Test the POST /book endpoint with missing email to check validation
def test_booking_missing_email(client):
    # Send a POST request to /book with JSON missing 'client_email'
    response = client.post('/book', json={
        "class_id": 1,
        "client_name": "John Cena"
    })
    
    # Assert that the response status code is 400 Bad Request due to missing field
    assert response.status_code == 400
    
    # Assert the error message contains 'Missing' indicating which field is missing
    assert 'Missing' in response.json['error']
