from app import app  # Import your application factory
from models import Quiz  # Import your Quiz model
import unittest

# Optional: Mock library (if mocking database)
# from unittest.mock import patch
def test_create_quiz(app):  # Use app as a fixture
    print("Creating test context...")
    with app.test_context():  # Create a test context
        client = app.test_client()
        print("Created client...")

        # Simulate a POST request to create a quiz
        response = client.post('/quizzes', json={'title': 'My New Quiz'})

        assert response.status_code == 201  # Assert successful creation

        # ...

if __name__ == '__main__':
    print("Running tests...")
    unittest.main()  # Run your tests