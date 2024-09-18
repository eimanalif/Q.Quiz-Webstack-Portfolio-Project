from flask import Flask, send_from_directory, jsonify, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm
from models import User, Quiz, Question, Answer, Result, Option, Score
from config import Config
from db import db
import os
from flask_migrate import Migrate

# Initialize the app and configure it
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    quizzes = Quiz.query.all() 
    return render_template('home.html', quizzes=quizzes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/take_quiz/<int:quiz_id>', methods=['GET'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if not questions:
        flash('No questions available for this quiz.', 'info')
    return render_template('take_quiz.html', quiz=quiz, questions=questions)

@app.route('/quiz/<int:quiz_id>', methods=['POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    score = 0
    for question in quiz.questions:
        selected_answer_id = request.form.get(f'question_{question.id}')
        selected_answer = Answer.query.get(selected_answer_id)
        if selected_answer and selected_answer.is_correct:
            score += 1
    result = Result(user_id=current_user.id, quiz_id=quiz.id, score=score, total=len(quiz.questions))
    db.session.add(result)
    db.session.commit()
    flash(f'You scored {score} out of {len(quiz.questions)}!', 'success')
    return redirect(url_for('results'))

@app.route('/results')
@login_required
def results():
    user_results = Result.query.filter_by(user_id=current_user.id).all()
    return render_template('results.html', results=user_results)

@app.route('/add_quiz', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        user_id = current_user.id  # Get the ID of the logged-in user
        new_quiz = Quiz(title=title, description=description, user_id=user_id)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_quiz.html')

@app.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        quiz.title = request.form['title']
        quiz.description = request.form['description']
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.user_id != current_user.id:
        abort(403)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.route('/quizzes')
def quizzes():
    quizzes = Quiz.query.all()
    return render_template('quizzes.html', quizzes=quizzes)

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    answers = request.form
    score = 0
    for question in quiz.questions:
        correct_option = Option.query.filter_by(question_id=question.id, is_correct=True).first()
        selected_option_id = answers.get(f'q{question.id}')
        if selected_option_id and int(selected_option_id) == correct_option.id:
            score += 1
    return f"Your score: {score}/{len(quiz.questions)}"

@app.route('/choose_quiz')
@login_required
def choose_quiz():
    quizzes = Quiz.query.all()
    return render_template('choose_quiz.html', quizzes=quizzes)

@app.route('/view_scores')
@login_required
def view_scores():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    return render_template('view_scores.html', scores=scores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)