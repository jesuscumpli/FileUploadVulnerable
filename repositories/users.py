import json
import sys
import mariadb

'''
QUERIES FROM USERS TABLES
'''

with open('configMariaDB.json', 'r') as f:
    configMariaDB = json.load(f)

def check_user_exists(username):
    conn = mariadb.connect(**configMariaDB)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username= '%s'" % username
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result is None:
        return False
    else:
        return True

def find_user_password(username, password):
    conn = mariadb.connect(**configMariaDB)
    cur = conn.cursor()
    cur.execute(
        "SELECT username, role FROM users WHERE username= '%s' AND password='%s'" % (username, password)
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def create_new_user(username, password, role):
    conn = mariadb.connect(**configMariaDB)
    cur = conn.cursor()
    inserted = True
    try:
        query = '''
            INSERT INTO users
            VALUES ('%s', '%s', '%s') 
        ''' % (username, password, role)
        # args = (username, password, role)
        cur.execute(query)
        conn.commit()
    except mariadb.Error as error:
        inserted = False
    finally:
        cur.close()
        conn.close()
        return inserted