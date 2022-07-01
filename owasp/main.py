#!/usr/bin/python3

from os import system

try:
    print("""
    Choose option:
        1. Sql injection
    """)
    a = int(input("Enter here: "))

    if a == 1:
        print("Entering sql injection....")
        system('clear')
        system('./owasp/sqli.py')
    else:
        print('wrong entry')

except KeyboardInterrupt:
    a=input("Do you want to EXIT (y/n): ")
    if a=='n' or a=='N':
        system('./owasp/main.py')
    else:
        print("Exiting...")


