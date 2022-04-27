from classes.SQLUtils import *
import sys

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