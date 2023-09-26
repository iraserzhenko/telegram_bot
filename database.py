import imports


def create_tables():
    connect = imports.sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS logins(
            id INTEGER,
            username TEXT,
            full_name TEXT
        )""")
    connect.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS friends(
                    id INTEGER,
                    username TEXT,
                    friend_usn TEXT,
                    friend_id INTEGER
                )""")
    connect.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS accepted(
                    id INTEGER,
                    username TEXT,
                    f_usn TEXT,
                    f_id INTEGER
                )""")
    connect.commit()
