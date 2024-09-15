import os

class Config:
    # Secret key for securing sessions and forms
    SECRET_KEY = '6ab3373251476733f91574db2a9fddef'
    # Database URI for SQLAlchemy
    # Default to SQLite for local development; override with DATABASE_URL in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # Disable modification tracking to save memory and improve performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # You can add other configuration options, such as mail server or pagination
    # Example (if you're using email):
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
