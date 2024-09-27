Q Quiz Application
Overview
The Q Quiz application is an interactive web-based quiz platform that allows users to take quizzes, track their scores, and receive feedback. It was developed as part of the ALX Webstack specialization, focusing on full-stack development with Flask, SQLAlchemy, and a variety of frontend technologies.

Features
User Authentication: Users can register and log in to track their quiz results.
Quiz Management: Admins can create, edit, and delete quizzes.
Multiple Choice Questions: Quizzes consist of multiple-choice questions with various answer options.
Real-time Feedback: Users receive immediate feedback on their quiz performance.
Responsive Design: The application is optimized for both desktop and mobile devices.


Technologies Used
Backend:

    Flask (Python-based web framework): For routing, handling HTTP requests, and serving your app's logic.

    SQLAlchemy (Object-Relational Mapper): For database interaction and managing models (like Quiz, Question, Choice, Result, etc.).

    Flask-Migrate: For database migrations, helping manage schema changes in the database.

    Flask-Bcrypt: For password hashing and handling secure user authentication.

    Flask-Login: For managing user sessions and authentication.

    Flask-WTF: For form handling, including CSRF protection.

Frontend: HTML, CSS, JavaScript

Database: SQLite For storing quiz data, user information, results, and other app-related data.

Version Control: Git

Installation
To set up the Q Quiz application locally, follow these steps:

Clone the repository: git clone https://github.com/eimanalif/Q.quiz-webstack-portfolio-project.git
 
      cd Q.quiz-webstack-portfolio-project

Create a virtual environment: 
 
      python3 -m venv venv 
      source venv/bin/activate # On Windows use venv\Scripts\activate

Install dependencies: 

        pip install -r requirements.txt

Set up the database: Run the following command to create the initial database structure: flask db upgrade

Run the application: 

        flask run 'Navigate to http://127.0.0.1:5000 in your web browser.'

Usage
To register, navigate to the registration page and create an account.
Once logged in, you can access available quizzes and start taking them.
Your results will be tracked and displayed after each quiz.

Development Report
Successes
Completed key features such as user authentication and quiz management.


Challenges
Faced issues with model relationships and debugging complex queries.
Addressed various routing errors during development.

Areas for Improvement
Enhance performance through optimization techniques.
Improve user experience with additional features such as progress tracking and more detailed feedback.

Lessons Learned
Strengthened skills in Flask, SQLAlchemy, and frontend technologies.
Gained experience in self-management and problem-solving while working independently.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Special thanks to the ALX Webstack team for their guidance and resources.

