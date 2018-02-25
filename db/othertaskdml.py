from os import path
import sqlite3

DATABASE = path.join(path.dirname(__file__), 'tpdb.db')

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
    sid = select_subject(task['subject'])[0]
    desc = task['desc']
    ptime = task['pomotime']

    return 'INSERT INTO otherTasks(fk_user_id, \
                                   fk_othertaskssubject_id, \
                                   description, \
                                   pomo_time) \
                                   VALUES(?, ?, ?, ?)', (uid, sid, desc, ptime)

@close_commit
def insert_subject(subject_name):
    return 'INSERT INTO otherTasksSubjects(name) VALUES(?)', (subject_name,)

@close_commit
def delete(cid):
    return 'DELETE FROM otherTasks WHERE id = ?', (cid,)

@close_commit
def update(cid, sid, desc, ptime):
    return 'UPDATE codes SET fk_user_id = ?, \
                             fk_subject_id = ?, \
                             description = ?, \
                             pomo_time = ? \
                             WHERE cid = ?', (cid, sid, desc, ptime)

def select_subject(subject_name):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM otherTasksSubjects WHERE name = ?', (subject_name,))
    data = cur.fetchone()
    conn.commit()
    conn.close()

    if data is None:
        insert_subject(subject_name)
        return select_subject(subject_name)

    return data
