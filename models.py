from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import orm

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    results = db.relationship('Result', backref='user', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    quiz = db.relationship('Quiz', back_populates='questions')

    # Relationship to answers
    answers = db.relationship('Answer', back_populates='question')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    # Foreign key to Question
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    # Relationship to Question
    question = db.relationship('Question', back_populates='answers')

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
