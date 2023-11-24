import sqlite3
from Config import CONFIG, LOGGER

class Database:
    instance = None

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.instance = self

    
    @classmethod
    def execute_query(cls, query, commit=False):
        db = Database(CONFIG.db_path)
        result = db.cur.execute(query).fetchall()
        if commit:
            db.conn.commit()
        db.conn.close()
        return result
    
    @classmethod
    def execute_create_query(cls, query) -> int:
        db = Database(CONFIG.db_path)
        db.cur.execute(query).fetchall()
        db.conn.commit()
        db.conn.close()
        return db.cur.lastrowid
    
    @classmethod
    def get_db(cls):
        if cls.instance is None:
            LOGGER.info('New db instance requested')
            return Database(CONFIG.db_path)
        else:
            return cls.instance
        
    @classmethod
    def convert_date(cls, date):
        d, m, y = date.split('-')
        return f"'{y}-{m}-{d}'"
        
    @classmethod
    def convert_boolean(cls, val):
        return 1 if val else 0
