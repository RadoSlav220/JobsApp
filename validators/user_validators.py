from config import *


def validate_user_elements(name: str, username: str, password: str, user_type: str) -> None:
    validate_name(name)
    validate_username(username)
    validate_password(password)
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


def validate_user_type(user_type: str) -> None:
    if user_type is None or user_type == '':
        raise ValueError('Missing user type')

    if user_type != 'recruiter' and user_type != 'applicant':
        raise ValueError('Invalid user type')