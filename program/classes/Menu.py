from classes.SQLUtils import *
from classes.Menu import *
from classes.Booking import *

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

    def menu_main_input(self):
        try:
            return int(input("Choose one of the options [1-5]: "))
        except Exception:
            print("Letters are not a valid input")
    
    def menu_main_choice(self):
        print(self.MAIN_MENU_TEXT)
        choice = self.menu_main_input()
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

    def menu_main_loop(self):
        self.running = True
        while self.running:
            self.menu_main_choice()
    
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