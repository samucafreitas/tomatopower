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
def insert(uid, task):
    lid = select_language(task['lang'])[0]
    desc = task['desc']
    ptime = task['pomotime']

    return 'INSERT INTO codes(fk_user_id, \
                              fk_language_id, \
                              description, \
                              pomo_time) \
                              VALUES(?, ?, ?, ?)', (uid, lid, desc, ptime)

@close_commit
def insert_language(lang_name):
    return 'INSERT INTO languages(name) VALUES(?)', (lang_name,)

@close_commit
def delete(cid):
    return 'DELETE FROM codes WHERE id = ?', (cid,)

@close_commit
def update(cid, lid, desc, ptime):
    return 'UPDATE codes SET fk_user_id = ?, \
                             fk_language_id = ?, \
                             description = ?, \
                             pomo_time = ? \
                             WHERE cid = ?', (cid, lid, desc, ptime)

def select_language(lang_name):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM languages WHERE name = ?', (lang_name,))
    data = cur.fetchone()
    conn.commit()
    conn.close()

    if data is None:
        insert_language(lang_name)
        return select_language(lang_name)

    return data
