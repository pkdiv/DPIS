from datetime import datetime
from register import register_utils
from db import db_utils

hostname="sql6.freesqldatabase.com"
username="sql6444336"
password="jvQ8tRrEEV"
database="sql6444336"

conn_details = {
    'host':hostname,
    'user': username,
    'password': passwordf,
    'database': database,
    'raise_on_warnings': True
}

db = db_utils.connect_db(conn_details)
print('Connection established.')
cursor = db.cursor()



try:
    id = register_utils.register_user(details, cursor)
    db.commit()
except:
    db.rollback()
    print('Error: Could not insert into the database.')

if id:
    print(f'ID: {id}')
    print('\nUser registered.')
else:
    print('User could not be registered.')
