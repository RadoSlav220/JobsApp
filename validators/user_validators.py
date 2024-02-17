import re
from config import *

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_user_elements(name: str, username: str, password: str, email:str, user_type: str) -> None:
    validate_name(name)
    validate_username(username)
    validate_password(password)
    validate_email(email)
    validate_user_type(user_type)


def validate_name(name: str) -> None:
    if name is None or name == '':
        raise ValueError('Missing name')
    
    if len(name) > USER_NAME_MAXIMUM_LENGTH:
        raise ValueError('Name is too long')


def validate_username(username: str) -> None:
    if username is None or username == '':
        raise ValueError('Missing username')
    
    if len(username) > USER_USERNAME_MAXIMUM_LENGTH:
        raise ValueError('Username is too long')


def validate_password(password: str) -> None:
    if password is None or password == '':
        raise ValueError('Missing password')

    if len(password) < USER_PASSWORD_MINIMUM_LENGTH:
        raise ValueError('Password is too short')
    
    if len(password) > USER_PASSWORD_MAXIMUM_LENGTH:
        raise ValueError('Password is too long')


def validate_email(email: str) -> None:
    if email is None or email == '':
        raise ValueError('Missing password')

    if len(email) > USER_EMAIL_MAXIMUM_LENGTH:
        raise ValueError('Email is too long')
    
    if not re.match(EMAIL_PATTERN, email):
        raise ValueError('Invalid email address')


def validate_user_type(user_type: str) -> None:
    if user_type is None or user_type == '':
        raise ValueError('Missing user type')

    if user_type != 'recruiter' and user_type != 'applicant':
        raise ValueError('Invalid user type')