import sqlite3


def drop_table():
    with sqlite3.connect('comedy.db') as connection:
        c = connection.cursor()
        c.execute("""DROP TABLE IF EXISTS comedy;""")
    return True


def create_db():
    with sqlite3.connect('comedy.db') as connection:
        c = connection.cursor()
        table = """CREATE TABLE comedy(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comedian TEXT NOT NULL,
            album TEXT NOT NULL,
            rating INTEGER NOT NULL
        );
        """
        c.execute(table)
    return True


if __name__ == '__main__':
    drop_table()
    create_db()
