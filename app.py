from flask import Flask, render_template, redirect, url_for, jsonify, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm, AddQuizForm, QuizForm, QuestionForm, ChoiceForm
from models import User, Quiz, Question, Result, Choice
from config import Config
from sqlalchemy.exc import IntegrityError
from db import db
from flask_migrate import Migrate
import os
from utils import calculate_score
from flask_wtf.csrf import CSRFProtect

# Initialize the app and configure it
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by ID for session management.
    Flask-Login will use this to reload the user object from the user ID stored in the session.
    """
    return User.query.get(int(user_id))

# Utility function to check if a user owns a quiz
def check_quiz_owner(quiz):
    """
    Ensures that only the user who created the quiz can modify it.
    If the quiz doesn't belong to the current user, a 403 Forbidden error is raised.
    """
    if quiz.user_id != current_user.id:
        abort(403)

# Utility function to validate and process quiz answers
def check_answers(quiz, answers):
    """
    Calculate the user's score for a quiz by checking selected answers against the correct ones.
    The score is incremented for each correct answer.
    Returns the total score.
    """
    score = 0
    for question in quiz.questions:
        correct_option = Option.query.filter_by(question_id=question.id, is_correct=True).first()
        selected_option_id = answers.get(f'q{question.id}')
        if selected_option_id and int(selected_option_id) == correct_option.id:
            score += 1
    return score

# Routes
@app.route('/')
def home():
    """
    Home page that displays all available quizzes.
    """
    quizzes = Quiz.query.all()
    results = Result.query.all()
    
    return render_template('home.html', quizzes=quizzes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    On successful form validation, a new user is created and added to the database.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Account created successfully! You can now log in', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    On successful validation, user is logged in and redirected to the dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """
    Log out the current user and redirect to the home page.
    """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """
    Display the user's dashboard. Requires the user to be logged in.
    """
    return render_template('dashboard.html')

@app.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    """
    Render a quiz for the user to take.
    Handles quiz question pagination and processes form submissions to check answers.
    Stores results in the database after submission.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions  # Assuming a relationship between Quiz and Question
    results = []  # Initialize results here
    page = request.args.get('page', 1, type=int)

    # Paginate the questions (5 per page)
    questions_paginated = Question.query.filter_by(quiz_id=quiz_id).paginate(page=page, per_page=5)

    if request.method == 'POST':
        for question in questions:
            # Get the selected choice for this question
            selected_choice_id = request.form.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = Choice.query.get(selected_choice_id)

                # Find the correct choice for this question
                correct_choice = Choice.query.filter_by(question_id=question.id, is_correct=True).first()

                # Create a result object, score is 1 if the selected choice is correct
                result = Result(
                    score=1 if selected_choice == correct_choice else 0,
                    user_id=current_user.id,
                    quiz_id=quiz_id,
                    question_id=question.id,
                    choice_id=selected_choice_id
                )
                results.append(result)

        # Commit the results to the database if any results were collected
        if results:
            db.session.add_all(results)
            db.session.commit()
            return redirect(url_for('quiz_results', quiz_id=quiz_id, result_id=results[-1].id))  # Pass both quiz_id and result_id
        else:
            flash('No answers were submitted. Please select at least one option.', 'warning')
            return redirect(url_for('take_quiz', quiz_id=quiz_id))

    return render_template('take_quiz.html', quiz=quiz, questions=questions_paginated.items, pagination=questions_paginated)

@app.route('/quiz_results/<int:quiz_id>/<int:result_id>', methods=['GET'])
@login_required
def quiz_results(quiz_id, result_id):
    """
    Display the results of the quiz for the user.
    The results include the score and total number of questions.
    """
    results = Result.query.filter_by(quiz_id=quiz_id).all()
    score = calculate_score(results)  
    total_score = len(results)  

    return render_template('quiz_results.html', results=results, score=score)


@app.route('/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz():
    """
    Handle adding a new quiz.
    Dynamically adds questions and choices from the form input and saves them to the database.
    """
    form = QuizForm()

    if form.validate_on_submit():  # Validate the form
        print("Form submitted successfully")

        # Create a new Quiz instance
        new_quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id  # Associate the quiz with the current user
        )
        db.session.add(new_quiz)
        db.session.commit()

        quiz_id = new_quiz.id  # Retrieve the ID of the newly created quiz
        
        # Extract questions and choices from the form
        for question_data in form.questions.data:
            question_text = question_data.get('text', '')
            new_question = Question(
                content='Default content',  # Placeholder content
                quiz_id=quiz_id,
                question_text=question_text,
                user_id=current_user.id
            )
            db.session.add(new_question)
            db.session.commit()

            # Add choices for each question
            for choice_data in question_data.get('choices', []):
                choice_text = choice_data.get('text', '')
                is_correct = choice_data.get('is_correct', False)

                new_choice = Choice(
                    text=choice_text,
                    is_correct=is_correct,
                    question_id=new_question.id
                )
                db.session.add(new_choice)

            db.session.commit()

        flash('Quiz added successfully!', 'success')
        print("Redirecting to home page")
        return redirect(url_for('home'))  # Redirect after successful submission

    print("Form errors:", form.errors)  # Debug: Show form errors if validation fails
    return render_template('add_quiz.html', form=form)

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    """
    Handle editing an existing quiz.
    Allows editing quiz title, description, questions, and choices.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    check_quiz_owner(quiz)

    form = QuizForm(obj=quiz)

    if form.validate_on_submit():
        # Update quiz title and description
        quiz.title = form.title.data
        quiz.description = form.description.data
        
        # Update existing questions or add new ones
        for i, question_form in enumerate(form.questions):
            if i < len(quiz.questions):
                # Update existing question
                question = quiz.questions[i]
                question.text = question_form.text.data
            else:
                # Add new question if form has more questions than existing quiz
                new_question = Question(text=question_form.text.data, quiz_id=quiz.id)
                quiz.questions.append(new_question)
                db.session.add(new_question)
            
            # Handle choices for each question
            for j, choice_form in enumerate(question_form.choices):
                if j < len(question.choices):
                    # Update existing choice
                    choice = question.choices[j]
                    choice.text = choice_form.text.data
                    choice.is_correct = choice_form.is_correct.data
                else:
                    # Add new choice if form has more choices than existing question
                    new_choice = Choice(text=choice_form.text.data, is_correct=choice_form.is_correct.data, question_id=question.id)
                    question.choices.append(new_choice)
                    db.session.add(new_choice)
        
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_quiz.html', quiz=quiz, form=form)

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    """
    Handle deleting a question from a quiz.
    This deletes the question and its associated choices.
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    check_quiz_owner(quiz)

    for question in quiz.questions:
        for choice in question.choices:
            db.session.delete(choice)
        db.session.delete(question)
    
    Result.query.filter_by(quiz_id=quiz_id).delete()
    
    db.session.delete(quiz)
    db.session.commit()
    
    flash(f'Quiz "{quiz.title}" and all associated data deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """
    Handle quiz submission and score calculation
    """
    quiz = Quiz.query.get_or_404(quiz_id)
    answers = request.form
    score = check_answers(quiz, answers)
    return f"Your score: {score}/{len(quiz.questions)}"

@app.route('/choose_quiz')
@login_required
def choose_quiz():
    """
    Display a page where the user can select a quiz to take.
    """
    quizzes = Quiz.query.all()
    return render_template('choose_quiz.html', quizzes=quizzes)

@app.route('/view_scores')
@login_required
def view_scores():
    """
    Display the current user's quiz scores.
    """
    scores = Result.query.filter_by(user_id=current_user.id).all()
    return render_template('view_scores.html', scores=scores)

@app.errorhandler(403)
def forbidden_error(error):
    """
    Handle 403 Forbidden errors.
    """
    return render_template('403.html'), 403

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
