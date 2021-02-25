import sqlite3

CREATE_CARD_TABLE = """CREATE TABLE IF NOT EXISTS card(
id INTEGER PRIMARY KEY, 
number TEXT, 
pin TEXT, 
balance INTEGER DEFAULT 0);"""

INSERT_CARD = "INSERT INTO card(number, pin) VALUES (?, ?);"

GET_ALL_CARDS = "SELECT * FROM card;"

GET_CARD_BALANCE = "SELECT * FROM card WHERE id = ? LIMIT 1;"

UPDATE_BALANCE = "UPDATE card SET balance = ? WHERE id = ?;"

DELETE_CARD = "DELETE FROM card WHERE id = ?;"


def connect():
    return sqlite3.connect('card.s3db')


def create_table(conn):
    with conn:
        conn.execute(CREATE_CARD_TABLE)


def add_card(conn, number, pin):
    with conn:
        conn.execute(INSERT_CARD, (number, pin))


def get_all(conn):
    with conn:
        return conn.execute(GET_ALL_CARDS).fetchall()


def get_balance(conn, ids):
    with conn:
        return conn.execute(GET_CARD_BALANCE, (ids,)).fetchall()


def update_balance(conn, add):
    with conn:
        conn.execute(UPDATE_BALANCE, add)


def delete_card(conn, ids):
    with conn:
        conn.execute(DELETE_CARD, (ids,))
