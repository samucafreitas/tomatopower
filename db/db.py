from os import path
import sqlite3

BASE_DIR = path.dirname(path.realpath(__file__))
DATABASE = path.join(BASE_DIR, 'tpdb.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute('''PRAGMA foreign_keys = ON''')

    cur.execute('''CREATE TABLE IF NOT EXISTS languages(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(6) NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS subjects(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(10) NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS otherTasksSubjects(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(10) NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name VARCHAR(20) NOT NULL UNIQUE,
                        dt_registration TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS codes(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fk_user_id REFERENCES users(id),
                        fk_language_id REFERENCES languages(id),
                        description VARCHAR(150) NOT NULL,
                        pomo_time INTEGER,
                        dt_registration TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS studies(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fk_user_id REFERENCES users(id),
                        fk_subject_id REFERENCES subjects(id),
                        description VARCHAR(150) NOT NULL,
                        pomo_time INTEGER,
                        dt_registration TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS otherTasks(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        fk_user_id REFERENCES users(id),
                        fk_othertaskssubject_id REFERENCES otherTasksSubjects(id),
                        description VARCHAR(150) NOT NULL,
                        pomo_time INTEGER,
                        dt_registration TIMESTAMP DEFAULT (DATETIME('now', 'localtime')))''')

    conn.commit()
    conn.close()
