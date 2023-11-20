import sqlite3

class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    
    def execute_query(self, query):
        return self.cur.execute(query).fetchall()