#!/usr/bin/python3

from os import system
import scan
try:
    system('clear')
    print("""
    Choose option:
        1. Sql injection
        2. XSS injection
        3. Broken access control / IDOR 
        4. Broken Authentication Control 
        5. Sensitive data exposure
        
        Enter 0 to go back
    """)
    a = int(input("Enter here: "))

    if a == 1:
        scan.sqli()
    elif a == 2:
        scan.xss()
    elif a==3:
        scan.idor()
    elif a==4:
        scan.bac()
    elif a==5:
        scan.sens()
    elif a==0:
        system("./main.py")
    else:
        print('wrong entry')

except KeyboardInterrupt:
    a=input("Do you want to EXIT (y/n): ")
    if a=='n' or a=='N':
        system('./owasp/main.py')

    else:
        system("./main.py")


