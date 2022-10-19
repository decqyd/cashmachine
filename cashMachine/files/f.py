####  IMPORTS  ####
from re import S
import smtplib, ssl  # emails
import curses  # cli
from curses import wrapper  # cli
from curses.textpad import Textbox, rectangle  # cli user input
import sys, time, os  # obvious
import main
import json

#################
####  VARIABLES  ####

global loggedin
loggedin = False

colours = {
    1: curses.COLOR_BLACK,
    2: curses.COLOR_RED,
    3: curses.COLOR_GREEN,
    4: curses.COLOR_YELLOW,
    5: curses.COLOR_BLUE,
    6: curses.COLOR_MAGENTA,
    7: curses.COLOR_CYAN,
    8: curses.COLOR_WHITE,
}

title = """  _____          _   _ _  _____   _____ _____ __  __ ______  _____ 
 |  __ \   /\   | \ | ( )/ ____| |  __ \_   _|  \/  |  ____|/ ____|
 | |  | | /  \  |  \| |/| (___   | |  | || | | \  / | |__  | (___  
 | |  | |/ /\ \ | . ` |  \___ \  | |  | || | | |\/| |  __|  \___ \ 
 | |__| / ____ \| |\  |  ____) | | |__| || |_| |  | | |____ ____) |
 |_____/_/    \_\_| \_| |_____/  |_____/_____|_|  |_|______|_____/"""

mainmenu = """

██████╗░░█████╗░███╗░░██╗██╗░██████╗  ██████╗░██╗███╗░░░███╗███████╗░██████╗
██╔══██╗██╔══██╗████╗░██║╚█║██╔════╝  ██╔══██╗██║████╗░████║██╔════╝██╔════╝
██║░░██║███████║██╔██╗██║░╚╝╚█████╗░  ██║░░██║██║██╔████╔██║█████╗░░╚█████╗░
██║░░██║██╔══██║██║╚████║░░░░╚═══██╗  ██║░░██║██║██║╚██╔╝██║██╔══╝░░░╚═══██╗
██████╔╝██║░░██║██║░╚███║░░░██████╔╝  ██████╔╝██║██║░╚═╝░██║███████╗██████╔╝
╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═════╝░  ╚═════╝░╚═╝╚═╝░░░░░╚═╝╚══════╝╚═════╝░"""

loginv = """             _,.---._         _,---.   .=-.-..-._         
   _.-.    ,-.' , -  `.   _.='.'-,  \ /==/_ /==/ \  .-._  
 .-,.'|   /==/_,  ,  - \ /==.'-     /|==|, ||==|, \/ /, / 
|==|, |  |==|   .=.     /==/ -   .-' |==|  ||==|-  \|  |  
|==|- |  |==|_ : ;=:  - |==|_   /_,-.|==|- ||==| ,  | -|  
|==|, |  |==| , '='     |==|  , \_.' )==| ,||==| -   _ |  
|==|- `-._\==\ -    ,_ /\==\-  ,    (|==|- ||==|  /\ , |  
/==/ - , ,/'.='. -   .'  /==/ _  ,  //==/. //==/, | |- |  
`--`-----'   `--`--''    `--`------' `--`-` `--`./  `--`  """

m = ["View Balance", "Deposit", "Withdraw", "Transfer", "Change PIN", "Exit"]
ls = ["Login", "Sign Up", "Exit"]
####################
####  FUNCTIONS  ####


def lineprint(t):
    for i in t:
        sys.stdout.write(i)
        sys.stdout.flush()
    time.sleep(0.1)


def l(s):
    y, x = getmiddle(s)
    y -= 10
    cri = 0
    curses.curs_set(0)
    s.clear()
    for line in mainmenu.splitlines():
        s.addstr(y - 3, x - (len(line) // 2), line)
        y += 1
        s.refresh()
    y += 5
    s.border()
    while True:
        y, x = getmiddle(s)
        y -= 10

        for line in mainmenu.splitlines():
            s.addstr(y - 3, x - (len(line) // 2), line)
            y += 1
            s.refresh()
        y += 5
        s.border()
        for i, r in enumerate(ls):
            w = x - len(r) // 2
            h = y - (len(ls) // 2) + i * 2
            if i == cri:
                s.attron(curses.color_pair(1))
                s.addstr(h, w, r)
                s.attroff(curses.color_pair(1))
            else:
                s.addstr(h, w, r)
        s.refresh()

        key = s.getch()
        if key == curses.KEY_UP and cri > 0:
            cri -= 1
        elif key == curses.KEY_DOWN and cri < len(ls) - 1:
            cri += 1
        elif key == curses.KEY_DOWN and cri >= len(ls) - 1:
            cri = 0
        elif key == curses.KEY_UP and cri <= 0:
            cri = len(ls) - 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            s.clear()
            s.refresh()
            if cri == 0:
                login(s)
            elif cri == 1:
                signup(s)
            elif cri == 2:
                quit(s)
            s.refresh()

        # set key q to exit
        elif key == ord("q"):
            sys.exit()
        s.refresh()


def p_init(s):
    initcolours(s)
    y, x = getmiddle(s)
    s.clear()
    s.border()
    tlp(s, title)
    time.sleep(0.3)
    s.addstr(
        y,
        x - (len(" WELCOME TO DAN'S DIMES ") // 2),
        "WELCOME TO DAN'S DIMES",
        curses.color_pair(1),
    )


def initcolours(s):
    # init all colours
    curses.init_pair(1, colours[1], colours[8])  # black on white
    curses.init_pair(2, colours[8], colours[1])  # white on black
    curses.init_pair(3, colours[8], colours[2])  # white on red
    curses.init_pair(4, colours[8], colours[3])  # white on green
    curses.init_pair(5, colours[8], colours[4])  # white on yellow
    curses.init_pair(6, colours[8], colours[5])  # white on blue
    curses.init_pair(7, colours[8], colours[6])  # white on magenta
    curses.init_pair(8, colours[8], colours[7])  # white on cyan


def loading(s):
    y, x = getmiddle(s)
    symbols = ["|", "/", "-", "\\"]
    for i in range(1):
        for symbol in symbols:
            # print the symbol 3/4 of the way down the screen
            s.addstr(y + 10, x, symbol)
            s.move(0, 0)
            s.refresh()
            time.sleep(0.2)


def getmiddle(s):
    y, x = s.getmaxyx()
    y = y // 2
    x = x // 2
    return y, x


# menu
def menu(s):
    s.clear()
    curses.noecho()
    curses.curs_set(0)
    cri = 0
    s.border()
    y, x = getmiddle(s)
    y -= 10
    try:
        for line in mainmenu.splitlines():
            s.addstr(y - 3, x - (len(line) // 2), line)
            y += 1
            s.refresh()
            time.sleep(0.1)
    except curses.error:
        print("Screen too small! Please re-size your window and try again :)")
        time.sleep(1)
        sys.exit()
    except:
        print("There as an error, please try again :)")
    y += 5
    while True:
        y, x = getmiddle(s)
        y -= 10
        for line in mainmenu.splitlines():
            s.addstr(y - 3, x - (len(line) // 2), line)
            y += 1
            s.refresh()
        y += 5
        s.border()
        for i, r in enumerate(m):
            w = x - len(r) // 2
            h = y - (len(m) // 2) + i * 2
            if i == cri:
                s.attron(curses.color_pair(1))
                s.addstr(h, w, r)
                s.attroff(curses.color_pair(1))
            else:
                s.addstr(h, w, r)
        s.refresh()

        key = s.getch()
        if key == curses.KEY_UP and cri > 0:
            cri -= 1
        elif key == curses.KEY_DOWN and cri < len(m) - 1:
            cri += 1
        elif key == curses.KEY_DOWN and cri >= len(m) - 1:
            cri = 0
        elif key == curses.KEY_UP and cri <= 0:
            cri = len(m) - 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            s.clear()
            s.refresh()
            if cri == 0:
                checkbalance(s)
            elif cri == 1:
                deposit(s)
            elif cri == 2:
                withdraw(s)
            elif cri == 3:
                transfer(s)
            elif cri == 4:
                changepin(s)
            elif cri == 5:
                exit(s)
            s.refresh()

        # set key q to exit
        elif key == ord("q"):
            sys.exit()
        s.refresh()


def tlp(s, t):
    y, x = getmiddle(s)
    try:
        for line in t.splitlines():
            s.addstr(y - 3, x - (len(line) // 2), line)
            y += 1
            s.refresh()
            time.sleep(0.1)
    except curses.error:
        print("Screen too small! Please re-size your window and try again :)")
        time.sleep(1)
        sys.exit()
    except:
        print("There as an error, please try again :)")


def quit(s):
    s.clear()
    sys.exit()


def withdraw(s):
    s.clear()
    s.addstr(0, 0, "Withdraw")
    s.refresh()
    s.getch()


def deposit(s):
    # deposit
    s.clear()
    s.addstr("Deposit")
    s.refresh()
    s.getch()


def checkbalance(s):
    # check balance
    s.clear()
    s.addstr("Your balance is £0")
    s.refresh()
    s.getch()


def changepin(s):
    # change pin
    s.clear()
    s.addstr("Change PIN")
    s.refresh()
    s.getch()


def transfer(s):
    # transfer
    s.clear()
    s.addstr("Transfer")
    s.refresh()
    s.getch()


def login(s):
    # close curses window to allow for input
    curses.nocbreak()
    s.keypad(False)
    curses.echo()
    curses.endwin()
    os.system("cls")
    lineprint(loginv)
    print("\n\n Account Number: \n")
    accnum = input("> ")
    print("\n\n PIN: \n")
    pin = int(input("> "))
    with open("data.json", "r") as f:
        data = json.load(f)
    if accnum in data:
        if pin == data[accnum]["pin"]:
            print("Login successful!")
            time.sleep(1)
            global loggedin
            loggedin = True
            os.system("cls")
            wrapper(main.main(s))
        else:
            print("Incorrect PIN!")
            time.sleep(1)
            os.system("cls")
            login(s)
    else:
        print("Account not found!")
        time.sleep(1)
        os.system("cls")
        login(s)


def signup(s):
    # login
    s.clear()
    s.border()
    s.addstr("sign up")
    s.refresh()
    s.getch()
