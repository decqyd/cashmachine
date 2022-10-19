####  IMPORTS  ####
import smtplib, ssl  # emails
import curses  # cli
from curses import wrapper  # cli
from curses.textpad import Textbox, rectangle  # cli user input
import sys, time, os  # obvious
import main
import json
import pyfiglet

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

depositv = """ .S_sSSs      sSSs   .S_sSSs      sSSs_sSSs      sSSs   .S  sdSS_SSSSSSbs  
.SS~YS%%b    d%%SP  .SS~YS%%b    d%%SP~YS%%b    d%%SP  .SS  YSSS~S%SSSSSP  
S%S   `S%b  d%S'    S%S   `S%b  d%S'     `S%b  d%S'    S%S       S%S       
S%S    S%S  S%S     S%S    S%S  S%S       S%S  S%|     S%S       S%S       
S%S    S&S  S&S     S%S    d*S  S&S       S&S  S&S     S&S       S&S       
S&S    S&S  S&S_Ss  S&S   .S*S  S&S       S&S  Y&Ss    S&S       S&S       
S&S    S&S  S&S~SP  S&S_sdSSS   S&S       S&S  `S&&S   S&S       S&S       
S&S    S&S  S&S     S&S~YSSY    S&S       S&S    `S*S  S&S       S&S       
S*S    d*S  S*b     S*S         S*b       d*S     l*S  S*S       S*S       
S*S   .S*S  S*S.    S*S         S*S.     .S*S    .S*P  S*S       S*S       
S*S_sdSSS    SSSbs  S*S          SSSbs_sdSSS   sSS*S   S*S       S*S       
SSS~YSSY      YSSP  S*S           YSSP~YSSY    YSS'    S*S       S*S       
                    SP                                 SP        SP        
                    Y                                  Y         Y """

withdrawv = """██╗    ██╗██╗████████╗██╗  ██╗██████╗ ██████╗  █████╗ ██╗    ██╗
██║    ██║██║╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██║    ██║
██║ █╗ ██║██║   ██║   ███████║██║  ██║██████╔╝███████║██║ █╗ ██║
██║███╗██║██║   ██║   ██╔══██║██║  ██║██╔══██╗██╔══██║██║███╗██║
╚███╔███╔╝██║   ██║   ██║  ██║██████╔╝██║  ██║██║  ██║╚███╔███╔╝
 ╚══╝╚══╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ """

changepinv = """  ______   __    __   ______   __    __   ______   ________        _______   ______  __    __ 
 /      \ /  |  /  | /      \ /  \  /  | /      \ /        |      /       \ /      |/  \  /  |
/$$$$$$  |$$ |  $$ |/$$$$$$  |$$  \ $$ |/$$$$$$  |$$$$$$$$/       $$$$$$$  |$$$$$$/ $$  \ $$ |
$$ |  $$/ $$ |__$$ |$$ |__$$ |$$$  \$$ |$$ | _$$/ $$ |__          $$ |__$$ |  $$ |  $$$  \$$ |
$$ |      $$    $$ |$$    $$ |$$$$  $$ |$$ |/    |$$    |         $$    $$/   $$ |  $$$$  $$ |
$$ |   __ $$$$$$$$ |$$$$$$$$ |$$ $$ $$ |$$ |$$$$ |$$$$$/          $$$$$$$/    $$ |  $$ $$ $$ |
$$ \__/  |$$ |  $$ |$$ |  $$ |$$ |$$$$ |$$ \__$$ |$$ |_____       $$ |       _$$ |_ $$ |$$$$ |
$$    $$/ $$ |  $$ |$$ |  $$ |$$ | $$$ |$$    $$/ $$       |      $$ |      / $$   |$$ | $$$ |
 $$$$$$/  $$/   $$/ $$/   $$/ $$/   $$/  $$$$$$/  $$$$$$$$/       $$/       $$$$$$/ $$/   $$/ """

signupv = """    ___     __     ___      _  _         _  _      ___  
   F __".   FJ   ,"___".   F L L]       FJ  L]    F _ ",
  J (___|  J  L  FJ---L]  J   \| L     J |  | L  J `-' |
  J\___ \  |  | J |  [""L | |\   |     | |  | |  |  __/F
 .--___) \ F  J | \___] | F L\\  J     F L__J J  F |__/ 
 J\______JJ____LJ\_____/FJ__L \\__L   J\______/FJ__|    
  J______F|____| J_____F |__L  J__|    J______F |__L"""

transferv = """|''||''| '||''|.       |     '|.   '|'  .|'''.|  '||''''| '||''''|  '||''|.   
   ||     ||   ||     |||     |'|   |   ||..  '   ||  .    ||  .     ||   ||  
   ||     ||''|'     |  ||    | '|. |    ''|||.   ||''|    ||''|     ||''|'   
   ||     ||   |.   .''''|.   |   |||  .     '||  ||       ||        ||   |.  
  .||.   .||.  '|' .|.  .||. .|.   '|  |'....|'  .||.     .||.....| .||.  '|' """

m = [
    "View Balance",
    "Deposit",
    "Withdraw",
    "Transfer",
    "Change PIN",
    "Sign Out",
    "Exit",
]
ls = ["Login", "Sign Up", "Exit"]
####################
####  FUNCTIONS  ####


def lineprint(t):
    for i in t.splitlines():
        sys.stdout.write(i)
        sys.stdout.flush()
        sys.stdout.write("\n")
        time.sleep(0.01)


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
            quit(s)
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
        f = open("data.json", "r")
        data = json.load(f)
        name = data[accnum]["name"]
        strtp = f"Welcome, {name}!"
        s.addstr(y - 6, x - (len(strtp) // 2), strtp)
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
                signout(s)
            elif cri == 6:
                quit(s)

            s.refresh()

        # set key q to exit
        elif key == ord("q"):
            quit(s)
        s.refresh()


def tlp(s, t, ymod=0, xmod=0):
    y, x = getmiddle(s)
    y += ymod
    x += xmod
    try:
        for line in t.splitlines():
            s.addstr(y - 3, x - (len(line) // 2), line)
            y += 1
            s.refresh()
            time.sleep(0.1)
    except curses.error as e:
        print(e)
        time.sleep(1)
        sys.exit()
    except:
        print("There as an error, please try again :)")


def quit(s):
    s.clear()
    cursesbreak(s)
    sys.exit()


def withdraw(s):
    cursesbreak(s)
    clear()
    lineprint(withdrawv)
    print("\n How much would you like to withdraw? (Type all to withdraw all)\n")
    amount = input("> ")
    try:
        amount = int(amount)
        with open("data.json", "r+") as f:
            data = json.load(f)
            cash = data[accnum]["cash"]

            if amount > int(data[accnum]["balance"]):
                print(
                    "\n The amount you entered is more than you currently have in your bank. \n"
                )
                time.sleep(0.5)
                print(
                    "Withdrawing the maximum amount of money you have in your bank... \n"
                )
                time.sleep(1)

                amount = data[accnum]["balance"]

            data[accnum]["balance"] -= amount
            data[accnum]["cash"] += amount

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            print(
                "\n Withdrew ${:,} from your account.\n You now have ${:,} in cash.".format(
                    amount, cash
                )
            )
            f.close()
            time.sleep(1.5)
            clear()
            wrapper(main.main(s))
    except ValueError:
        if "all" in amount:
            with open("data.json", "r+") as f:
                data = json.load(f)
                cash = data[accnum]["cash"]

                amount = data[accnum]["balance"]

                data[accnum]["balance"] -= amount
                data[accnum]["cash"] += amount

                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print(
                    "\n Withdrew ${:,} from your account.\n You now have ${:,} in cash.".format(
                        amount, cash
                    )
                )
                f.close()
                time.sleep(1.5)
                clear()
                wrapper(main.main(s))
        else:
            print("Please enter a number")
            time.sleep(0.5)
            withdraw(s)
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(0.5)
        clear()
        wrapper(main.main(s))


def signout(s):
    s.clear()
    global loggedin
    loggedin = False
    cursesbreak(s)
    wrapper(main.main(s))


def deposit(s):
    cursesbreak(s)
    clear()
    lineprint(depositv)
    print("\n How much would you like to deposit? \n")
    try:
        amount = int(input("> "))
        with open("data.json", "r+") as f:
            data = json.load(f)
            data[accnum]["balance"] += amount
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            print("\nDeposited ${:,} into your account.\n".format(amount))
            f.close()
            time.sleep(1.5)
            clear()
            wrapper(main.main(s))
    except ValueError:
        print("Please enter a valid number")
        time.sleep(0.5)
        deposit(s)
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(0.5)
        clear()
        wrapper(main.main(s))


def checkbalance(s):
    # check balance
    y, x = getmiddle(s)
    s.clear()
    s.border()
    with open("data.json", "r") as f:
        data = json.load(f)
    s.addstr(y - 20, x - 8, "Your balance is ")
    # pyfiglet prints the balance in size 5
    bal = data[accnum]["balance"]
    nbal = str("{:,}".format(bal))
    jbal = " ".join(i for i in nbal)
    w = 200
    font = "doh"
    if len(jbal) < 15:
        w = 250
    elif len(jbal) < 20:
        w = 300
    elif len(jbal) < 50:
        font = "big"
    else:
        w = 100
        font = "big"
    strtp = f"$ {jbal}"
    tlp(
        s,
        pyfiglet.figlet_format(strtp, font=font, width=w),
        -len(strtp) // 2,
    )
    s.refresh()
    s.getch()
    s.clear()


def changepin(s):
    cursesbreak(s)
    clear()
    lineprint(changepinv)
    print("\nEnter your new pin \n")
    with open("data.json", "r+") as f:
        data = json.load(f)
        print("You current pin is {}".format(data[accnum]["pin"]))
        try:
            pin = int(input("> "))
            if len(str(pin)) != 4:
                print("Please enter a 4 digit pin")
                time.sleep(0.5)
                changepin(s)
            else:
                data[accnum]["pin"] = pin
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                print("\nChanged pin to {}.\n".format(pin))
                f.close()
                time.sleep(1.5)
                clear()
                wrapper(main.main(s))
        except ValueError:
            print("Please enter a number")
            time.sleep(0.5)
            changepin(s)
        except KeyboardInterrupt:
            print("\nExiting...")
            time.sleep(0.5)
            clear()
            wrapper(main.main(s))


def transfer(s):
    cursesbreak(s)
    clear()
    lineprint(transferv)
    print("\nEnter the account number you want to transfer to \n")

    try:
        acc = input("> ")

        with open("data.json", "r+") as f:
            data = json.load(f)
            if acc not in data:
                print("Account does not exist")
                time.sleep(0.5)
                transfer(s)
            else:
                print(
                    "How much would you like to transfer? (type all to tranfer all money) \n"
                )
                amount = input("> ")
                try:
                    amount = int(amount)
                    if amount > data[accnum]["balance"]:
                        print("You do not have enough money in your account")
                        time.sleep(0.5)
                        transfer(s)
                    else:
                        data[accnum]["balance"] -= amount
                        data[acc]["balance"] += amount
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        f.truncate()
                        print("\nTransfered ${:,} to account {}.\n".format(amount, acc))
                        f.close()
                        time.sleep(1.5)
                        print(
                            "\nYou have ${:,} left in your account.\n".format(
                                data[accnum]["balance"]
                            )
                        )
                        clear()
                        wrapper(main.main(s))
                except ValueError:
                    if "all" in amount:
                        with open("data.json", "r+") as f:
                            data = json.load(f)
                            cash = data[accnum]["cash"]

                            amount = data[accnum]["balance"]

                            data[accnum]["balance"] -= amount
                            data[acc]["balance"] += amount

                            f.seek(0)
                            json.dump(data, f, indent=4)
                            f.truncate()
                            print(
                                "\n Transfered ${:,} to account {}.\n".format(
                                    amount, acc
                                )
                            )
                            f.close()
                            time.sleep(1.5)
                            print("You have no money left in your account")
                            clear()
                            wrapper(main.main(s))
                    else:
                        print("Please enter a number")
                        time.sleep(0.5)
                        transfer(s)
                except KeyboardInterrupt:
                    print("\nExiting...")
                    time.sleep(0.5)
                    clear()
                    wrapper(main.main(s))
    except ValueError:
        print("Please enter a number")
        time.sleep(0.5)
        transfer(s)
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(0.5)
        clear()
        wrapper(main.main(s))


def cursesbreak(s):
    curses.nocbreak()
    s.keypad(False)
    curses.echo()
    curses.endwin()
    os.system("cls")


def login(s):
    cursesbreak(s)
    lineprint(loginv)
    print("\n\n Account Number: \n")
    global accnum
    try:
        accnum = input("> ")
        print("\n\n PIN: \n")
        pin = int(input("> "))
    except ValueError:
        print("Please enter a number")
        time.sleep(0.5)
        login(s)
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(0.5)
        clear()
        wrapper(main.main(s))

    with open("data.json", "r") as f:
        data = json.load(f)
    if accnum in data:
        if pin == data[accnum]["pin"]:
            print("\nLogin successful!")
            time.sleep(1)
            global loggedin
            loggedin = True
            os.system("cls")
            f.close()
            wrapper(main.main(s))
        else:
            print("\nIncorrect PIN!")
            time.sleep(1)
            os.system("cls")
            login(s)
    else:
        print("\nAccount not found!")
        time.sleep(1)
        os.system("cls")
        login(s)


def signup(s):
    cursesbreak(s)
    lineprint(signupv)
    try:
        print("\n\n Name: \n")
        name = input("> ")
        print("\n\n Account Number: \n")
        accnum = int(input("> "))
        if len(str(accnum)) != 16:
            print("Please enter a 16 digit account number")
            time.sleep(0.5)
            signup(s)
        print("\n\n PIN: \n")
        pin = int(input("> "))

    except ValueError:
        print("Please enter a number.")
        time.sleep(0.5)
        signup(s)
    except KeyboardInterrupt:
        print("\nExiting...")
        time.sleep(0.5)
        clear()
        wrapper(main.main(s))
    with open("data.json", "r+") as f:
        data = json.load(f)
        if accnum in data:
            print("\nAccount already exists!")
            time.sleep(1)
            os.system("cls")
            signup(s)
        else:
            data[accnum] = {}
            data[accnum]["name"] = name
            data[accnum]["pin"] = pin
            data[accnum]["balance"] = 0
            data[accnum]["cash"] = 0
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            print(f"\nAccount {name} created!")
            time.sleep(1)
            os.system("cls")
            f.close()
            wrapper(main.main(s))


def clear():
    os.system("cls")
