from os import path
import sqlite3

BASE_DIR = path.dirname(path.realpath(__file__))
DATABASE = path.join(BASE_DIR, 'tpdb.db')

def close_commit(func):
    def magic(*args):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        sql = func(*args)
        cur.execute(sql[0], sql[1])
        conn.commit()
        conn.close()
    return magic

@close_commit
def insert(user_name):
    return 'INSERT INTO users(user_name) VALUES(?)', (user_name,)

@close_commit
def delete(uid):
    return 'DELETE FROM users WHERE id = ?', (uid,)

@close_commit
def update(uid, name, login, password):
    return 'UPDATE users SET name = ?, login = ?, password = ? WHERE id = ?',\
                                                (name, login, password, uid)

def select_user(user_name):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_name = ?', (user_name,))
    data = cur.fetchone()
    conn.commit()
    conn.close()

    if data is None:
        insert(user_name)
        return select_user(user_name)

    return data
