
# Conference Center

This program will allow you to book times at a conference center.
It does this by asking the user for different kinds of input, be it a word or number.

## Setup

Before you do anything, you need to navigate to the data folder run the generate_sql_room.py file. This will generate the database the program uses. You need to stand in the project folder for this to work.

The program can be started from 2 different files:
1: everything_program.py includes every class that the program in the same file
2: program.py runs the program through the Menu.py file that in itself imports the different klasses needed to run the program.

### Example

The navigation of the programs different menus will only use numbers while the program will ask the user to input different words depending on the situation. Below is in example of a short run of the program.

    '------------------------'
    '------ Welcome to ------'
    '-Fake conference center-'
    '------------------------'

    [1] List all available conference rooms.
    [2] Book conference room.
    [3] Search for your booked times.
    [4] Search for amenities.
    [5] Stop program.

Do note that do find the names of the different rooms available, you need to either look at the database manually or print available rooms with the 1 option.

    Choose one of the options [1-5]: 2
    Which room do you want to book?
    Dune
    +-------------+-----------+-----------+-----------+-----------+
    | Room Name   | January   | Febuary   | March     | April     |
    +=============+===========+===========+===========+===========+
    | Dune        | Available | Available | Available | Available |
    +-------------+-----------+-----------+-----------+-----------+


    Which month do you want to book?
    January
    Which company do you represent?
    Fiskeriet AB

    '------------------------'
    '---- Do you want to ----'
    '---book another time?---'
    '------------------------'

    [1] Yes.
    [2] No.

    Choose option [1-2]: 2
    Your price is 40000sek

    '------------------------'
    '------ Welcome to ------'
    '-Fake conference center-'
    '------------------------'

    [1] List all available conference rooms.
    [2] Book conference room.
    [3] Search for your booked times.
    [4] Search for amenities.
    [5] Stop program.
