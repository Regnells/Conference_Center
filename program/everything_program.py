import sqlite3
import json
from tabulate import tabulate
import sys

# This class is used to format SQL query output using tabulate.
class Formatting:
    def tabulate_format_room(self, room):
        print(tabulate([room], headers=["Room Name","Projector","Cameras","Available Months","Price","Contact Person"], tablefmt='grid'))
        print("\n")

    def tabulate_format_time(self, room):
        print(tabulate([room], headers=["Room Name","January","Febuary","March","April"], tablefmt='grid'))
        print("\n")

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

# This class is used to apply all the different SQL methods.
class Booking:
    def __init__(self):
        self.sql = SqlUtils()

    # We return room_choice as we are using this to help us in other methods in this class.
    def book_choose_room(self):
        room_choice = input("Which room do you want to book?\n").lower()
        self.sql.sql_room_search(room_choice)
        return room_choice

    # Again, the ifs statement is an unfortunate side effect of SQL not being able to handle SET ?
    def book_update_room(self, room_choice):
        month_choice = input("Which month do you want to book?\n").lower()
        company = input("Which company do you represent?\n")
        if month_choice == "january":
            self.sql.sql_update_january(room_choice.lower(), company)
        elif month_choice == "febuary":
            self.sql.sql_update_febuary(room_choice.lower(), company)
        elif month_choice == "march":
            self.sql.sql_update_march(room_choice.lower(), company)
        elif month_choice == "april":
            self.sql.sql_update_april(room_choice.lower(), company)

        self.sql.sql_count_available(room_choice)
        self.sql.sql_lower_available(room_choice)

    # As SQL queries return tuples, we're extracting the desired output using [0].
    def book_room_price(self, room_choice):
        price = self.sql.sql_get_price(room_choice)
        # This try/except is used to catch if the input for room_choice isn't capitalized correctly  and the reason I use sys.exit(1) is since the problem
        # cascades down into the program in several places while also borking the room price calc method in the Menu class.
        try:
            return price[0]
        except:
            print("Room name needs to correctly capitalized")
            # Ty https://stackoverflow.com/questions/438894/how-do-i-stop-a-program-when-an-exception-is-raised-in-python for the solution.
            sys.exit(1)

    # We have this method return int(price) to make sure the price tracking method works in the Menu class.
    def book_room(self):
        room_choice = self.book_choose_room()
        self.book_update_room(room_choice)
        price = self.book_room_price(room_choice)
        return int(price)

    # We are converting the input to lower to handle weird input formats.
    def book_search_company(self):
        search_term = input("What is your company name?\n").lower()
        self.sql.sql_search_bookings(search_term)

    def book_projector(self):
        self.sql.sql_print_projector()

    def book_camera(self):
        self.sql.sql_print_camera()

# This class is used to handle all the menu navigation and used the Bookings methods.
class Menu:

    MAIN_MENU_TEXT = """
'------------------------'
'------ Welcome to ------'
'-Fake conference center-'
'------------------------'

[1] List all available conference rooms.
[2] Book conference room.
[3] Search for your booked times.
[4] Search for amenities.
[5] Stop program.
"""

    MENU_AMENITY_TEXT = """
'--------------------------------------------------'
'---- We currently offer these extra amenities:----'
'--------------------Projectors--------------------'
'---------------------Cameras----------------------'
'--------------------------------------------------'

[1] Show rooms where Projectors are available.
[2] Show rooms where Cameras are available.
[3] Return.
"""

    MENU_AMENITY_OPTIONS = """
'------------------------'
'---- Do you want to ----'
'------------------------'

[1] Book a time in one of the rooms?
[2] Return.
"""

    MENU_BOOK_AGAIN_TEXT = """
'------------------------'
'---- Do you want to ----'
'---book another time?---'
'------------------------'

[1] Yes.
[2] No.
"""

    def __init__(self):
        self.sql = SqlUtils()
        self.booking = Booking()
        self.price_list = []

    # This is the way the program keeps track of the price of the bookings.
    def menu_sum_price(self):
        self.sum_total_price = 0
        for price in self.price_list:
            self.sum_total_price += price
        return self.sum_total_price

    # This is where a check is made too see if the user has booked several rooms.
    # At the moment it works because of the way the different rooms have been priced, as the sum of two bookings will always
    # be > 70000.
    def menu_sum_price_check(self):
        price = self.menu_sum_price()
        if price > 70000:
            discounted_price = price - (price / 10) 
            print(f'You got Discount! 10% has been taken off your price.\nYour price is {discounted_price}sek')
        else:
            print(f'Your price is {price}sek')
        
    """
    -----------------------------------------------------------------------------------------------------------
    """
    # This loop handles the main menu.

    def main_menu_input(self):
        try:
            return int(input("Choose one of the options [1-5]: "))
        except Exception:
            print("Letters are not a valid input")
    
    def main_menu_choice(self):
        print(self.MAIN_MENU_TEXT)
        choice = self.main_menu_input()
        if choice == 1:
            self.sql.sql_available_rooms()
        elif choice == 2:
            self.price_list.append(self.booking.book_room())
            self.menu_book_loop_loop()
            self.price_list = []
        elif choice == 3:
            self.booking.book_search_company()
        elif choice == 4:
            self.menu_amenity_loop()
        elif choice == 5:
            self.sql.sql_close()
            self.running = False
        else:
            # This catches int input errors, while the try/expect in input cathces string input errors. 
            print("You have to choose between [1-5]")

    def main_menu_loop(self):
        self.running = True
        while self.running:
            self.main_menu_choice()
    
    """
    -----------------------------------------------------------------------------------------------------------
    """
    # This menu handles the amenity booking

    def menu_amenity_input(self):
        try:
            return int(input("Choose option [1-3]: "))
        except Exception:
            print("Letters are not a valid input")
    
    def menu_amenity_options(self):
        print(self.MENU_AMENITY_TEXT)
        choice = self.menu_amenity_input()
        if choice == 1:
            self.booking.book_projector()
            self.menu_amenity_book_choice()
        elif choice == 2:
            self.booking.book_camera()
            self.menu_amenity_book_choice()
        elif choice == 3:
            self.amenity_running = False
            self.price_list = []
        else:
            print("You have to choose between [1-3]")

    def menu_amenity_loop(self):
        self.amenity_running = True
        while self.amenity_running:
            self.menu_amenity_options()

    """
    -----------------------------------------------------------------------------------------------------------
    """
    # This menu handles asking the user if they want to book one of the amenity rooms or not
    
    def menu_amenity_book_input(self):
        try:
            return int(input("Choose option [1-2]: "))
        except Exception:
            print("Letters are not a valid input")
    
    def menu_amenity_book_choice(self):
        print(self.MENU_AMENITY_OPTIONS)
        choice = self.menu_amenity_book_input()
        if choice == 1:
            self.price_list.append(self.booking.book_room())
            self.menu_book_loop_loop()
        else:
            self.amenity_running = False

    """
    -----------------------------------------------------------------------------------------------------------
    """

    # This menu handles all the repeat bookings.

    def menu_book_loop_input(self):
        try:
            return int(input("Choose option [1-2]: "))
        except Exception:
            print("Letters are not a valid input")
    
    def menu_book_loop_menu(self):
        print(self.MENU_BOOK_AGAIN_TEXT)
        choice = self.menu_book_loop_input()
        if choice == 1:
            self.price_list.append(self.booking.book_room())
        elif choice == 2:
            self.menu_sum_price_check()
            self.price_list = []
            self.menu_book_loop = False
        else:
            print("You have to choose between [1-2]")
            

    def menu_book_loop_loop(self):
        self.menu_book_loop = True
        while self.menu_book_loop:
            self.menu_book_loop_menu()

    """
    -----------------------------------------------------------------------------------------------------------
    """

if __name__ == '__main__':
    Menu().main_menu_loop()