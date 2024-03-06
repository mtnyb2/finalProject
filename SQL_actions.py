import sqlite3
conn = sqlite3.connect('Manual Database.db') 
cursor = conn.cursor()

create_tiny_worker = """CREATE TABLE TinyWorker (id CHARACTER(10) PRIMARY KEY,
                 name VARCHAR(255),
                        fname VARCHAR(255));
"""

#cursor.execute('''DROP TABLE TinyWorker''')

cursor.execute(create_tiny_worker)

def insert_new_worker (id, name, fname):
        cursor.execute('''INSERT INTO TinyWorker VALUES (?, ?, ?)''', (id, name, fname))

insert_new_worker(5727,'111', 'Saportas')

print("Data Inserted in the table: ") 
data=cursor.execute('''SELECT * FROM TinyWorker''') 
for row in data:
    print(row)

conn.close()