import json
import sys
import mariadb

'''
QUERIES FROM ROLES TABLE
'''

with open('configMariaDB.json', 'r') as f:
    configMariaDB = json.load(f)

def find_permissions_by_role(role):
    conn = mariadb.connect(**configMariaDB)
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM roles WHERE name='%s'" % role)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result
