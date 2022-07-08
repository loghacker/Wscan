#!/usr/bin/python3

from os import system

try:
    print("""
    Choose option:
        1. Owasp scanner
    """)
    a = int(input("Enter here: "))

    if a == 1:
        system('./owasp/main.py')
    else:
        print('wrong entry')

except KeyboardInterrupt:
    a=input("Do you want to EXIT (y/n): ")
    if a=='n' or a=='N':
        system('./main.py')
    else:
        print("Exiting...")


