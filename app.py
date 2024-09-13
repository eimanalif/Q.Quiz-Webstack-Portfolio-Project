from flask import Flask, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from models import User, Quiz, Question, Result
from forms import RegistrationForm, LoginForm
from config import Config
from flask_login import login_user, logout_user, login_required, current_user
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

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
        flash('Your account has been created! You can now log in', 'success')
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
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/quiz')
@login_required
def quiz():
    questions = Question.query.all()
    random.shuffle(questions)
    return render_template('quiz.html', questions=questions)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    answers = request.form.to_dict()
    score = 0
    total = len(answers)
    for q_id, user_answer in answers.items():
        question = Question.query.get(q_id)
        if question.correct_answer == user_answer:
            score += 1
    result = Result(user_id=current_user.id, score=score, total=total)
    db.session.add(result)
    db.session.commit()
    return render_template('results.html', score=score, total=total)

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    questions_data = [{'id': q.id, 'question': q.text, 'choices': q.choices} for q in questions]
    return jsonify(questions_data)

if __name__ == '__main__':
    app.run(debug=True)
