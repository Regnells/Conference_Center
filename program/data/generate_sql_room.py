import json
import sqlite3

CREATE_TABLE_CONFERENCE = '''
                CREATE TABLE IF NOT EXISTS conference(
                    unit TEXT NOT NULL,
                    projector TEXT NOT NULL,
                    cameras TEXT NOT NULL,
                    available_months INT NOT NULL,
                    price TEXT NOT NULL,
                    contact_person TEXTN NOT NULL
                        )
                '''

INSERT_DATA = '''
    INSERT INTO conference(
        unit,
        projector,
        cameras,
        available_months,
        price,
        contact_person
    )
    VALUES (?, ?, ?, ?, ?, ?)
    '''


with open("program/data/conference_rooms.json") as f:
    data_to_database_executemany = []
    rooms = json.load(f)
    for room in rooms['rooms']:
        data_to_database_executemany.append(tuple(room.values()))

    with sqlite3.connect('program/data/conference_rooms.db') as conn:
        conn.execute(CREATE_TABLE_CONFERENCE)
        conn.executemany(INSERT_DATA, data_to_database_executemany)

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