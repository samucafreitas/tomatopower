import sys
from getpass import getpass
from sqlite3 import IntegrityError
from db import userdml
from utils import error_msg

'''
    Here is the main menu showed when tomatopower.py starts.
    Should recursion be avoided in Python? Yeah, but I don't care.
    This is for learning purposes!
'''

def get_user():
    print('***** Tomato Power *****')
    user_name = input('User =<< ')
    return userdml.select_user(user_name)

def get_custom_time():
    '''Returns a custom time for pomodoro.'''
    print('Pomodoro Time:'\
        + '\n 1) 25 minutes (recommended)'\
        + '\n 2) 30 minutes'\
        + '\n 3) N minutes')

    try:
        opt = int(input('>>= '))
        if opt == 1:
            return 25
        elif opt == 2:
            return 30
        return int(input('N minutes =<< '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return get_custom_time()

def get_custom_break_time():
    '''Returns a custom time for break.'''
    print('Break Time:'\
        + '\n 1) 5 minutes'\
        + '\n 2) 10 minutes'\
        + '\n 3) N minutes')

    try:
        opt = int(input('>>= '))
        if opt == 1:
            return 5
        elif opt == 2:
            return 10
        return int(input('N minutes =<< '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return get_custom_break_time()

def get_sound():
    '''Returns a sound for alarm.'''
    print('Select a Sound:'\
        + '\n 1) submarine.mp3'\
        + '\n 2) foghorn.mp3'\
        + '\n 3) default')

    try:
        opt = int(input('>>= '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return get_sound()

    if opt == 1:
        return 'submarine.mp3'
    elif opt == 2:
        return 'foghorn.mp3'

    return 'submarine.mp3'

def get_task():
    '''Returns a dict.

    Task keys:
    type -- the task type: 1(coding), 2(Studying), 3(Other)
    task -- the task: coding, studying, other_task
    pomotime -- time for pomodoro
    '''
    task = {'type': None, 'pomotime': None, 'breaktime': None}

    print('Select a Task Type:'\
        + '\n 1) Coding'\
        + '\n 2) Studying'\
        + '\n 3) Other')

    try:
        opt = int(input('>>= '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return get_task()

    if opt == 1:
        task['type'] = 1
        task.update(opt_coding())
    elif opt == 2:
        task['type'] = 2
        task.update(opt_studying())
    else:
        task['type'] = 3
        task.update(opt_other_task())

    task['pomotime'] = get_custom_time()
    task['breaktime'] = get_custom_break_time()
    return task

def opt_coding():
    '''Returns a dict.

    Coding keys:
    lang -- programming language
    desc -- description
    '''
    coding = {'lang':'', 'desc':''}

    print('Pick a main language:'\
        + '\n 1) Python  2) Java'\
        + '\n 3) C++     4) C'\
        + '\n 5) Other')

    try:
        main_language = int(input('>>= '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return opt_coding()

    if main_language == 1:
        coding['lang'] = 'PYTHON'
    elif main_language == 2:
        coding['lang'] = 'JAVA'
    elif main_language == 3:
        coding['lang'] = 'C++'
    elif main_language == 4:
        coding['lang'] = 'C'
    else:
        coding['lang'] = input('Lang: ').upper()

    coding['desc'] = input('Task description: ')
    return coding

def opt_studying():
    '''Returns a dict.

    Studying keys:
    subject -- main subject study
    desc -- description
    '''
    studying = {'subject':'', 'desc':''}

    print('Pick a main subject:'\
        + '\n 1) Math and Science  2) Economics'\
        + '\n 3) Languages         4) Other')

    try:
        main_subject = int(input('>>= '))
    except ValueError as err:
        error_msg('Please, insert an integer number!', err)
        return opt_studying()

    if main_subject == 1:
        studying['subject'] = 'MATH AND SCIENCE'
    elif main_subject == 2:
        studying['subject'] = 'ECONOMICS'
    elif main_subject == 3:
        studying['subject'] = 'LANGUAGES'
    else:
        studying['subject'] = input('Task subject: ').upper()

    studying['desc'] = input('Task description: ')
    return studying

def opt_other_task():
    '''Returns a dict.

    Other task keys:
    subject -- a subject for the task
    desc -- description
    '''
    other_task = {'subject':'', 'desc':''}
    other_task['subject'] = input('Task subject: ').upper()
    other_task['desc'] = input('Task description: ')
    return other_task
