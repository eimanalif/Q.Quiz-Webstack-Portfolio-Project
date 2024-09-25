from flask_wtf import FlaskForm
from wtforms import  FieldList, StringField, PasswordField, TextAreaField, FormField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from wtforms import RadioField, SubmitField
# from flask_wtf.csrf import CSRFTokenField

class RegistrationForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChoiceForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    text = StringField('Choice Text', validators=[DataRequired()])
    is_correct = BooleanField('Correct')

class QuestionForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    text = StringField('Question Text', validators=[DataRequired()])
    choices = FieldList(FormField(ChoiceForm), min_entries=4, max_entries=4)

class QuizForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    title = StringField('Quiz Title', validators=[DataRequired()])
    description = StringField('Quiz Description', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=10)  # 10 questions per quiz
    submit = SubmitField('Add Quiz')

class ChoiceForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    text = StringField('Choice Text', validators=[DataRequired()])
    is_correct = BooleanField('Is Correct?')

class AddQuizForm(FlaskForm):
    # csrf_token = CSRFTokenField()
    title = StringField('Quiz Title', validators=[DataRequired()])
    description = TextAreaField('Description')  # Optional description
    questions = FieldList(FormField(QuestionForm), min_entries=1)  # At least one question
    choices = FieldList(FieldList(ChoiceForm))  # Nested list for choice data per question

    def validate_choices(self, field):
        # Custom validation for choices:
        # Ensure at least one choice is marked correct per question
        for question_choices in field.data:
            is_correct_found = False
            for choice in question_choices:
                if choice['is_correct']:
                    is_correct_found = True
                    break
            if not is_correct_found:
                raise ValidationError('At least one choice must be marked correct per question.')