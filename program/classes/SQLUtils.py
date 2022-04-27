import sqlite3
from classes.Formatting import *

# This whole class is dedicated to doing different SQL queries/updates.
class SqlUtils:
    def __init__(self):
        self.connection = sqlite3.connect("program\data\conference_rooms.db", isolation_level=None)
        self.formatting = Formatting()

    def sql_close(self):
        if self.connection:
            self.connection.close()

    def sql_available_rooms(self):
        with self.connection as cursor:
            for room in cursor.execute("SELECT * FROM conference WHERE available_months != 0"):
                self.formatting.tabulate_format_room(room)

    def sql_room_search(self, room_choice):
        with self.connection as cursor:
            for room in cursor.execute("SELECT * FROM bookings WHERE unit LIKE lower(?)", (room_choice,)):
                self.formatting.tabulate_format_time(room)

    # This is one kind of whack as I have to search through all the months for the search_term. Unsure if there is a better way to do this.
    def sql_search_bookings(self, search_term):
        with self.connection as cursor:
            for table in cursor.execute("SELECT * FROM bookings WHERE January LIKE lower(?) OR Febuary LIKE lower(?) OR March LIKE lower(?) OR April LIKE lower(?)", (search_term,search_term,search_term,search_term,)):
                self.formatting.tabulate_format_time(table)

    # Simple stuff but I'm proud of this one and lower_available
    def sql_count_available(self, room_choice):
        self.room_count = ""
        with self.connection as cursor:
            for room_count in cursor.execute("SELECT * FROM bookings WHERE unit LIKE lower(?)", (room_choice,)):      
                self.room_count = room_count.count("Available")

    def sql_lower_available(self, room_choice):
        with self.connection as cursor:
            cursor.execute("UPDATE conference SET available_months = ? WHERE unit LIKE lower(?)", (self.room_count, room_choice,))
    
    def sql_print_projector(self):
        with self.connection as cursor:
            for projector in cursor.execute("SELECT * FROM conference WHERE projector = 'yes' AND available_months != 0"):      
                self.formatting.tabulate_format_room(projector)

    def sql_print_camera(self):
        with self.connection as cursor:
            for camera in cursor.execute("SELECT * FROM conference WHERE cameras = 'yes' AND available_months != 0"):      
                self.formatting.tabulate_format_room(camera)

    def sql_get_price(self, room_choice):
        with self.connection as cursor:
            for price in cursor.execute("SELECT price FROM conference WHERE unit LIKE lower(?)", (room_choice,)):    
                return price

    # The following methods are an unfortunate side effect of SQL not being able to handle SET ? What is DRY btw?
    def sql_update_january(self, room_choice, company):
        with self.connection as cursor:
            cursor.execute("UPDATE bookings SET January = ? WHERE unit LIKE lower(?)", (str(company), room_choice,) )

    def sql_update_febuary(self, room_choice, company):
        with self.connection as cursor:
            cursor.execute("UPDATE bookings SET Febuary = ? WHERE unit LIKE lower(?)", (str(company), room_choice,) )

    def sql_update_march(self, room_choice, company):
        with self.connection as cursor:
            cursor.execute("UPDATE bookings SET March = ? WHERE unit LIKE lower(?)", (str(company), room_choice,) )

    def sql_update_april(self, room_choice, company):
        with self.connection as cursor:
            cursor.execute("UPDATE bookings SET April = ? WHERE unit LIKE lower(?)", (str(company), room_choice,) )