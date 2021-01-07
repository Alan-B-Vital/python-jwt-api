from Database import db
import jwt
import sqlite3
import unittest

def create_table(db_conn, table_name, columns):
    db_conn.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} {columns}""")
    db_conn.commit()

def drop_table(db_conn, table_name):
    db_conn.cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
    db_conn.commit()


class DatabaseTester(unittest.TestCase):
    def test_connection(self):
        self.assertIsNotNone(db)

    def test_table_creation_and_deletion(self):
        create_table(db, 'users_test', '(name text, token text)')

        db.cursor.execute("""SELECT sql
                FROM sqlite_master
                WHERE name = 'users_test';""")
        self.assertEqual(db.cursor.fetchone()[0], 'CREATE TABLE users_test (name text, token text)')

        drop_table(db, "users_test")
        self.assertRaises(sqlite3.OperationalError, db.cursor.execute, "SELECT * FROM users_test")

    def test_add_user(self):
        table = 'users'
        create_table(db, table, '(name text, token text)')

        user = 'Kamila'
        secret = 'secret'
        token = jwt.encode({'user_name': user}, secret,  algorithm="HS256")

        self.assertTrue(db.add_user(user, token, table=table))

        db.cursor.execute(f"SELECT * FROM {table}")
        queary = db.cursor.fetchone()
        self.assertEqual(queary, (1, user, token))

        drop_table(db, "users_test")

    def test_get_user_from_token(self):
        table = 'users'
        create_table(db, table, '(name text, token text)')

        user = 'Kamila'
        secret = 'secret'
        token = jwt.encode({'user_name': user}, secret, algorithm="HS256")

        db.add_user(user, token, table=table)

        queary = db.get_user_from_token(token, table=table)
        self.assertEqual(queary, user)

        drop_table(db, "users_test")