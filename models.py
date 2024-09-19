from db import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Relationships
    quizzes = db.relationship('Quiz', back_populates='creator', lazy=True)
    results = db.relationship('Result', back_populates='user', lazy=True)
    scores = db.relationship('Score', back_populates='user', lazy=True)
    questions = db.relationship('Question', back_populates='user', lazy=True)

    is_admin = db.Column(db.Boolean, default=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(255), nullable=True) 
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)  # User (creator) of the quiz
    
    # Relationships
    creator = db.relationship('User', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', lazy=True, cascade="all, delete-orphan")
    results = db.relationship('Result', back_populates='quiz', lazy=True)
    scores = db.relationship('Score', back_populates='quiz', lazy=True)

    def __repr__(self):
        return f'<Quiz {self.title}>'

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    # Relationships
    quiz = db.relationship('Quiz', back_populates='questions')
    user = db.relationship('User', back_populates='questions')
    answers = db.relationship('Answer', back_populates='question', cascade='all, delete-orphan')
    choices = db.relationship('Choice', back_populates='question')

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('question.id'), nullable=False)

    # Relationships
    question = db.relationship('Question', back_populates='answers')

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)  # User who took the quiz
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False)  # Quiz taken

    # Relationships
    user = db.relationship('User', back_populates='results')
    quiz = db.relationship('Quiz', back_populates='results')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer)

    # Relationships
    user = db.relationship('User', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')

class Choice(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String(100), nullable=False)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    question = relationship('Question', back_populates='choices')
