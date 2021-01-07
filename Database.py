import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.default_table = 'users'
        self.cursor.execute(f"""CREATE TABLE {self.default_table}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, token TEXT)""")

    def commit(self):
        self.connection.commit()

    def add_user(self, user_name, token, table=None):
        if table is None:
            table = self.default_table

        res = self.cursor.execute(f"""INSERT INTO {table} (name, token)
            VALUES ('{user_name}', '{token}')""")
        self.commit()
        return res


    def get_user_from_token(self, token, table=None):
        if table is None:
            table = self.default_table

        self.cursor.execute(f"""SELECT name FROM {table}
                    WHERE token = '{token}'""")
        res = self.cursor.fetchone()
        return res[0] if res else None


if __name__ == "Database":
    db = Database()

if __name__ == "__main__":
    db = Database()
    cursor = db.cursor
    for user in [('t_1', 'token_1'), ('t_2', 'token_2')]:
        db.add_user(user[0], user[1])

    cursor.execute("SELECT * FROM users")

    # cursor.execute("""SELECT sql
    # FROM sqlite_master
    # WHERE name = 'usears';""")
    print(cursor.fetchone())