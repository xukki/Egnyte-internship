import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO messages (mrole, content) VALUES (?, ?)",
            ('system', 'You are an Ai assistant who replies to queries about json data provided to you by the user.')
            )

connection.commit()
connection.close()