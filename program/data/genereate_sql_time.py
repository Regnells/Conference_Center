import json
import sqlite3

CREATE_TABLE_TIMES = '''
                CREATE TABLE IF NOT EXISTS bookings(
                    unit TEXT NOT NULL,
                    January TEXT,
                    Febuary TEXT,
                    March TEXT,
                    April TEXT
                        )
                '''

INSERT_DATA = '''
    INSERT INTO bookings(
        unit,
        January,
        Febuary,
        March,
        April
    )
    VALUES (?, ?, ?, ?, ?)
    '''


with open("program/data/conference_time.json") as f:
    data_to_database_executemany = []
    bookings = json.load(f)
    for booking in bookings['bookings']:
        data_to_database_executemany.append(tuple(booking.values()))

    with sqlite3.connect('program/data/conference_rooms.db') as conn:
        conn.execute(CREATE_TABLE_TIMES)
        conn.executemany(INSERT_DATA, data_to_database_executemany)