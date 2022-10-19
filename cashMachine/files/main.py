####  IMPORTS  ####
import smtplib, ssl  # emails
import curses  # cli
from curses import wrapper  # cli
import sys  # obvious
from time import sleep
import f

###################


def main(s):
    f.p_init(s)
    curses.noecho()
    curses.cbreak()
    s.keypad(True)
    s.refresh()
    if not f.loggedin:
        f.loading(s)
        f.l(s)
    elif f.loggedin:
        f.loading(s)
        f.menu(s)


if __name__ == "__main__":
    wrapper(main)
