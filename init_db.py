import sqlite3

conn = sqlite3.connect('banco.db') #conexão com o banco
BANCO = 'banco.sql'

with open(BANCO) as banco:
    conn.executescript(banco.read())

conn.commit()
conn.close()