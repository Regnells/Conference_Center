from tabulate import tabulate

# This class is used to format SQL query output using tabulate.
class Formatting:
    def tabulate_format_room(self, room):
        print(tabulate([room], headers=["Room Name","Projector","Cameras","Available Months","Price","Contact Person"], tablefmt='grid'))
        print("\n")

    def tabulate_format_time(self, room):
        print(tabulate([room], headers=["Room Name","January","Febuary","March","April"], tablefmt='grid'))
        print("\n")