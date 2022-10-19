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

    sleep(0.5)

    f.loading(s)
    f.l(s)

    s.getch()


if __name__ == "__main__":

    wrapper(main)

