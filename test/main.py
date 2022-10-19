import pyfiglet, sys, time

hw = pyfiglet.figlet_format("Hello World")
# print hw figlet line by line
for line in hw.splitlines():
    print(line)
    time.sleep(0.1)
