from flask import Flask, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from models import User, Quiz, Question, Result
from forms import RegistrationForm, LoginForm
from config import Config
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect, url_for, session, flash
import random
from models import Quiz, Question, Answer
from forms import QuizForm
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if 'logged_in' in session:
        return f'Welcome, {session["user_id"]}!'
    else:
        flash('You are not logged in!', 'danger')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Set session variables
            session['user_id'] = user.id
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

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

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id): 
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm()

    if request.method == 'POST' and form.validate_on_submit():
        score = 0
        for question in quiz.questions:
            selected_answer_id = request.form.get(f'question_{question.id}')
            selected_answer = Answer.query.get(selected_answer_id)
            if selected_answer and selected_answer.is_correct:
                score += 1

        session['score'] = score
        return redirect(url_for('quiz_results'))

    return render_template('quiz.html', quiz=quiz, form=form)

@app.route('/quiz/results')
def quiz_results():
    score = session.get('score')
    return render_template('results.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
