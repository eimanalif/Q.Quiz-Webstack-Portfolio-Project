from app import create_app  # Import your application factory
from models import Quiz  # Import your Quiz model

def test_create_quiz():
    app = create_app('testing')  # Create an app instance in testing mode
    with app.test_client() as client:
        # Simulate a POST request to create a quiz
        response = client.post('/quizzes', json={'title': 'My New Quiz'})

        assert response.status_code == 201  # Assert successful creation

        # Check the database (optional)
        quiz = Quiz.query.get(1)  # Assuming your quiz has an ID of 1
        assert quiz.title == 'My New Quiz'

if __name__ == '__main__':
    unittest.main()  # Run your tests