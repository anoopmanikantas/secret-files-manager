import sqlite3

db = sqlite3.connect('secret_files.db')
conn = db.cursor()

conn.execute('create new table secret (fname varchar(90),files blob)')
db.commit()
