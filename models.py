from db import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Relationships
    quizzes = db.relationship('Quiz', backref='creator', lazy=True)
    results = db.relationship('Result', backref='user', lazy=True)  # This creates the reverse relationship in `Result`
    questions = db.relationship('Question', backref='author', lazy=True)
    
    is_admin = db.Column(db.Boolean, default=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(255), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User (creator) of the quiz
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True)
    results = db.relationship('Result', backref='quiz', lazy=True)

    def __repr__(self):
        return f'<Quiz {self.title}>'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  # Reference to Quiz
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to User (who created the question)
    
    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self):
        return f'<Question {self.question_text}>'

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)  # To mark if this answer is the correct one
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  # Reference to the question

    def __repr__(self):
        return f'<Answer {self.text}>'

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who took the quiz
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  # Quiz taken
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False) 
    option = db.relationship('Option', backref='results')

    def __repr__(self):
        return f'<Result {self.score}>'

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class Score(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    score = Column(Integer)


    user = relationship("User", backref="scores")
    quiz = relationship("Quiz", backref="scores")
    def __repr__(self):
        return f'<Score {self.id}>'