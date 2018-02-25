from getpass import getpass
from requests.exceptions import HTTPError
import re
import json
import pyrebase
from utils import warning_msg, error_msg

fb = pyrebase.initialize_app({
    'apiKey': 'AIzaSyDeiUcMYMH7tjr8ZGwF6eOaVAIdvj8tcRA',
    'authDomain': 'tomatopower-42.firebaseapp.com',
    'databaseURL': 'https://tomatopower-42.firebaseio.com',
    'projectId': 'tomatopower-42',
    'storageBucket': 'tomatopower-42.appspot.com',
    'messagingSenderId': '297540980261'})

auth = fb.auth()
db = fb.database()

def fb_get_user():
    '''
        () -> dict
        returns a user.
    '''
    print('     ***** Tomato Power *****'
        + '\n 1) Sign In'\
        + '\n 2) Sign Up'\
        + '\n 3) Recover account'\
        + '\n n) Exit')

    try:
        opt = int(input('>>= '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return fb_get_user()
    
    if opt == 1:
        return fb_sign_in()
    elif opt == 2:
        return fb_sign_up()
    elif opt == 3:
        fb_recover_account()
        return fb_get_user()
    else:
        exit(0)

def fb_sign_in(num_attempts=0):
    '''
        (num_attemps: int) -> dict

        Keyword arguments:
        num_attempts -- number of attempts

        should return a user.
    '''
    if num_attempts > 2:
        warning_msg('Maximum number of attempts exceeded! Try again later.')
        exit(1)

    email = check_email(input('E-mail: ').strip())
    if email:
        password = getpass()
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            email_verified = auth.get_account_info(user['idToken'])['users'][0]['emailVerified']

            if not email_verified:
                auth.send_email_verification(user['idToken'])
                warning_msg('E-mail not verified! Please check your e-mail and try again.')
            else:
                return user
        except HTTPError as err:
            error_msg_json = json.loads(err.args[1])['error']['errors'][0]
            if error_msg_json.get('message') == 'EMAIL_NOT_FOUND':
                warning_msg('E-mail not registered!')
                return fb_get_user()
            else:
                warning_msg('Operation error! Try again.')
    num_attempts += 1
    return fb_sign_in(num_attempts)

def fb_sign_up(num_attempts=0):
    '''
        (num_attempts: int) -> dict

        Keyword arguments:
        num_attempts -- number of attempts

        should returns a user.
    '''
    if num_attempts > 2:
        error_msg('Maximum number of attempts exceeded! Try again later.')
        exit(1)

    name = input('Your name: ').strip()
    email = check_email(input('E-mail: ').strip())

    if email:
        password = getpass()
        rpassword = getpass('Repeat password: ')
        if len(password) >= 6:
            if password == rpassword:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    acc_info = auth.get_account_info(user['idToken'])['users'][0]

                    data = {'userId' : user['localId'],
                            'email': email,
                            'name': name,
                            'createdAt': acc_info['createdAt']}
                    fb_insert_user(user['idToken'], data)

                    auth.send_email_verification(user['idToken'])
                    warning_msg(f'We have sent an email to {email}\nYou need to verify your email to sign in.')
                    return fb_sign_in()
                except HTTPError as err:
                    error_msg_json = json.loads(err.args[1])['error']['errors'][0]
                    if error_msg_json.get('message') == 'EMAIL_EXISTS':
                        warning_msg('Email already exists! Try again.')
                    else:
                        warning_msg('Operation error! Try again.')
            else:
                warning_msg('Passwords are not the same! Try again.')
        else:
            warning_msg('Password should be at least 6 characters! Try again.')
    
    num_attempts += 1
    return fb_sign_up(num_attempts) 

# TODO: recover account
def fb_recover_account():
    pass

def fb_refresh_user_token(r_token):
    '''
        (r_token: str) -> dict
        returns a user with a fresh token.
    '''
    return auth.refresh(r_token)

def fb_insert_task(user, task):
    '''
        (user: dict, task: dict) -> ()
        inserts a task into Firebase Realtime Database.
    '''
    task_type = task['type']
    task.update({'userId' : user['userId']})
    del task['type']

    if task_type == 1:
        db.child('studies').child('code').push(task, user['idToken'])
    elif task_type == 2:
        db.child('studies').child('study').push(task, user['idToken'])
    else:
        db.child('othertask').push(task, user['idToken'])

def fb_insert_user(uit, data):
    '''
        (uit: str, data: dict) -> ()
        inserts a user into Firebase Realtime Database.
    '''
    db.child('users').push(data, uit)

def check_email(email):
    '''
        (email: str) -> str or None
        returns an email or None.
    '''
    if not re.match(r'[\w.-]+@[\w.-]+\.\w+', email):
        warning_msg('E-mail invalid! Try again.')
        return None
    return email