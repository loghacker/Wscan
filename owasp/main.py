#!/usr/bin/python3

from os import system
import scan
try:
    system('clear')
    print("""
    Choose option:
        1.  Injection
        2.  Broken Authentication and Session Management
        3.  Sensitive data exposure
        4.  XML External Entites (XXE)
        5.  Broken access control / IDOR
        6.  Security Misconfiguration
        7.  Cross-site scripting (XSS)
        8.  Insecure Deserialization
        9.  Using Components with Known Vulnerabilities
        10. Insufficient Logging and Monitoring
        
        Enter 0 to go back
    """)
    a = int(input("Enter here: "))

    if a == 1:
        scan.sqli()
    elif a==2:
        scan.bac()
    elif a==3:
        scan.sens()
    elif a==4:
        scan.()
    elif a==5:
        scan.idor()
    elif a==6:
        scan.()
    elif a == 7:
        scan.xss()
    elif a==8:
        scan.()
    elif a==9:
        scan.()
    elif a==10:
        scan.()
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


