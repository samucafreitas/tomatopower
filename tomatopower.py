#!/usr/bin/env python3
#
# Uses python-vlc   -> https://github.com/oaubert/python-vlc
# Uses Alarm Sounds -> http://soundbible.com/tags-alarm.html
#
# File              : tomatopower.py
# Author            : Sam Uel <samucaof42@gmail.com>
# Date              : 26 dec 2017
# Last Modified Date: 25 feb 2017
# Last Modified By  : Sam Uel <samucaof42@gmail.com>
#
# Abandon all hope, ye who enter here! - Dante Alighieri
import time
import sys
import tty
from os import path, system
from threading import Thread
import vlc
import menu
from utils import ( icons,
                    pomo_time_print,
                    break_time_print,
                    restoreCursor,
                    welcome_msg )
from db import db, codedml, studydml, othertaskdml

def chron():
    while True:
        now = time.time()
        future = now + case
        secs_count = case

        while now < future:
            now = time.time()
            time.sleep(1)
            minutes, seconds = divmod(secs_count, 60)

            if reset:
                secs_count = case
                future = now + case
            elif pause:
                future = now + secs_count
            else:
                secs_count -= 1

            chron_icon, chron_status = chron_state()

            pomo_time = '{:02d}:{:02d}'.format(minutes, seconds)
            pomo_time_print(pomo_time, chron_status, chron_icon)

        alarm(f'{icons["alarm"]} Time is up!')
        task_save()
        time_is_up()

def time_is_up():
    global pause

    now = time.time()
    future = now + case_break
    secs_count = case_break

    while now < future:
        now = time.time()
        time.sleep(1)
        minutes, seconds = divmod(secs_count, 60)

        secs_count -= 1

        break_time = '{:02d}:{:02d}'.format(minutes, seconds)
        break_time_print(break_time)
    alarm(f'{icons["alarm"]} Go back to work!')
    pause = True

def alarm(msg):
    system('macopix --message-expire 6000 --message \'{}\''.format(msg))
    player.set_media(media)
    player.play()

def task_save():
    if task['type'] == 1:
        codedml.insert(user[0], task)
    elif task['type'] == 2:
        studydml.insert(user[0], task)
    else:
        othertaskdml.insert(user[0], task)

def chron_state():
    if reset:
        return icons['reset'], 'reset'
    elif pause:
        return icons['pause'], 'pause'

    return icons['play'], 'play'

def get_key():
    tty.setcbreak(sys.stdin.fileno())
    key = sys.stdin.read(1)
    return key

def chron_control():
    global reset, pause

    while True:
        key = get_key()

        if key == 'q':
            sys.stdout.write(restoreCursor)
            sys.stdout.flush()
            sys.exit(0)
        elif key == 'r':
            reset = True
        elif key == 'p' or key == ' ':
            pause = True
        elif key == 's':
            if reset: reset = not reset
            if pause: pause = not pause

if __name__ == '__main__':
    db.init_db()
    reset = False
    pause = True # chron starts paused

    user, sound, task = menu.get_user(),\
                        menu.get_sound(),\
                        menu.get_task()
    case = task['pomotime'] * 60
    case_break = task['breaktime'] * 60

    welcome_msg(user[1])

    instance = vlc.Instance()
    player = instance.media_player_new()
    BASE_DIR = path.dirname(path.realpath(__file__))
    media = instance.media_new(path.join(BASE_DIR, 'sounds/'+sound))

    control_thread = Thread(target=chron_control)
    chron_thread = Thread(target=chron, daemon=True)
    control_thread.start()
    chron_thread.start()
