import sqlite3
from data_dict import random_users, create_random_user

def createTable():
    with sqlite3.connect('students.db') as conn:
        cur = conn.cursor()
        # Create the members table
        cur.execute(""" CREATE TABLE IF NOT EXISTS members
            (id INTEGER PRIMARY KEY, 
            first_name TEXT, 
            last_name TEXT,
            birth_date TEXT,
            gender TEXT,
            email TEXT,
            phonenumber TEXT,
            address TEXT,
            nationality TEXT,
            active BOOLEAN,
            github_username TEXT
            )""")
        
        # Insert random users into the members table
        cur.executemany('''INSERT INTO members (
             first_name,
             last_name,
             birth_date,
             gender, 
             email,
             phonenumber,
             address,
             nationality,
             active,
             github_username
             ) VALUES (:first_name, :last_name, :birth_date, :gender, :email, :phonenumber, :address, :nationality, :active, :github_username)''', random_users)
        
        conn.commit()

def read():
    members = []
    with sqlite3.connect('students.db') as conn:
        cur = conn.cursor()
        # Fetch from the members table
        cur.execute('SELECT * FROM members')

        for i in cur.fetchall():
            members.append(i)

    return members

createTable()
