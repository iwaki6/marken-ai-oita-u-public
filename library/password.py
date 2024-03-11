# import DBaccess
import library.DBaccess as DBaccess
import bcrypt
import hashlib
from email_validator import validate_email, EmailNotValidError

# app_login.py calls this function. You may choose how to treat passwords.
def check_password(password, user_info):
    result = simple_check(password, user_info['password'])
    # result = sha256_check(password, user_info['password'])
    # result = bcrypt_check(password, user_info['password'], user_info['salt'])
    
    return result


# Methods to treat passwords
def simple_check(password, correct_password):
    return password==correct_password

def simple_register_user(email, password, role):
    email = check_email_address(email)
    if email == False:
        return False
    data = {
        'email': email,
        'password': password,
        'role': role
    }
    if role == 'admin':
        return DBaccess.write_superuser(data)
    
    return False


def sha256_check(password, correct_password_hash):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest() == correct_password_hash

def sha256_register_user(email, password, role):
    email = check_email_address(email)
    if email == False:
        return False
    hash_object = hashlib.sha256(password.encode())
    data = {
        'email': email,
        'password': hash_object.hexdigest(),
        'role': role
    }
    if role == 'admin':
        return DBaccess.write_superuser(data)
    
    return False


def bcrypt_check(password, correct_password_hash, salt):
    return bcrypt.hashpw(password.encode(), salt) == correct_password_hash

def bcrypt_register_user(email, password, role):
    email = check_email_address(email)
    if email == False:
        return False
    salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
    data = {
        'email': email,
        'password': bcrypt.hashpw(password.encode(), salt),
        'salt': salt,
        'role': role
    }
    if role == 'admin':
        return DBaccess.write_superuser(data)
    
    return False

def check_email_address(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        email = email_info.normalized
        return email
    except EmailNotValidError as e:
        return False


# You can use this file as a script by using the following commands
# print(simple_register_user('dummy@dummy', 'dummy', 'admin'))
# print(sha256_register_user('dummy@dummy', 'dummy', 'admin'))
# print(bcrypt_register_user('dummy@dummy', 'dummy', 'admin'))
