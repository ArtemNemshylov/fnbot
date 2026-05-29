import sqlite3


class DataBaseConnection:
    def __init__(self, dbname):
        self.connection = sqlite3.connect(dbname)
        self.connection.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT)''')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS daily_snapshots (
            user_id INTEGER,
            snapshot_date TEXT,
            kills INTEGER,
            deaths INTEGER,
            wins INTEGER,
            matches INTEGER,
            minutes INTEGER,
            account_type TEXT,
            PRIMARY KEY (user_id, snapshot_date)
        )''')
        try:
            self.connection.execute("ALTER TABLE daily_snapshots ADD COLUMN account_type TEXT")
        except sqlite3.OperationalError:
            pass




    def execute(self, query, *args):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            self.connection.commit()
        cursor.close()

    def fetchone(self, query, *args):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            result = cursor.fetchone()
            cursor.close()
            return result

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    db = DataBaseConnection('users.db')
    db.create_db()
    db.close()