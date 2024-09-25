import sqlite3

def create():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS students (id INTEGER, name TEXT)''')
        cur.execute('''INSERT INTO students VALUES (1, 'Sof')''')
        cur.execute('''INSERT INTO students VALUES (2, 'Vik')''')
        cur.execute('''INSERT INTO students VALUES (3, 'Nat')''')


def read():

    students = []
    
    #hente data fra database
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM students')
    
        for i in cur.fetchall():
            students.append(i)

    return students

print(read)