from db import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    quizzes = db.relationship('Quiz', back_populates='user')
    results = db.relationship('Result', back_populates='user')  
    questions = db.relationship('Question', back_populates='user', cascade='all, delete-orphan')
    
    is_admin = db.Column(db.Boolean, default=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    user = db.relationship('User', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan')
    results = db.relationship('Result', back_populates='quiz')

class Option(db.Model):
    __tablename__ = 'option'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False) 

    question = db.relationship('Question', back_populates='options', foreign_keys=[question_id])

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    correct_option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)


    user = db.relationship('User', back_populates='questions')
    quiz = db.relationship('Quiz', back_populates='questions')

    correct_option = db.relationship(
        'Option',
        foreign_keys=[correct_option_id],
        backref='questions_correct'
    )

    options = db.relationship('Option', back_populates='question', foreign_keys='Option.question_id', cascade="all, delete-orphan")



class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)

    user = db.relationship('User', back_populates='results')
    quiz = db.relationship('Quiz', back_populates='results')
    question = db.relationship('Question')
    option = db.relationship('Option')

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
    quiz = db.relationship('Quiz', backref=db.backref('scores', lazy=True))
    user = db.relationship('User', backref=db.backref('scores', lazy=True))

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    question = db.relationship('Question', back_populates='choices')
