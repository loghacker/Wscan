#!/usr/bin/python3
import time
import urllib.request
import webbrowser
import requests
import base64
import pickle
import json
from json import JSONEncoder
from termcolor import colored
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
from os import system
from os.path import exists

#sql injection
def sqli():
    try:
        system('clear')
        s = requests.Session()
        s.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

        def get_all_forms(url):

            soup = bs(s.get(url).content, "html.parser")
            return soup.find_all("form")

        def get_form_details(form):
            details = {}
            try:
                action = form.attrs.get("action").lower()
            except:
                action = None
            method = form.attrs.get("method", "get").lower()
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.attrs.get("type", "text")
                input_name = input_tag.attrs.get("name")
                input_value = input_tag.attrs.get("value", "")
                inputs.append({"type": input_type, "name": input_name, "value": input_value})
            details["action"] = action
            details["method"] = method
            details["inputs"] = inputs
            return details

        def is_vulnerable(response):
            errors = {

                "you have an error in your sql syntax;",
                "warning: mysql",

                "unclosed quotation mark after the character string",

                "quoted string not properly terminated",
            }
            for error in errors:

                if error in response.content.decode().lower():
                    return True
            return False

        def scan_sql_injection(url):

            for c in "\"'":
                new_url = f"{url}{c}"
                print("[!] Trying", new_url)
                res = s.get(new_url)
                if is_vulnerable(res):
                    print("[+] SQL Injection vulnerability detected, link:", new_url)
                    return
            forms = get_all_forms(url)
            print(f"[+] Detected {len(forms)} forms on {url}.")
            for form in forms:
                form_details = get_form_details(form)
                for c in "\"'":
                    # the data body we want to submit
                    data = {}
                    for input_tag in form_details["inputs"]:
                        if input_tag["value"] or input_tag["type"] == "hidden":
                            try:
                                data[input_tag["name"]] = input_tag["value"] + c
                            except:
                                pass
                        elif input_tag["type"] != "submit":
                            data[input_tag["name"]] = f"test{c}"
                    url = urljoin(url, form_details["action"])
                    if form_details["method"] == "post":
                        res = s.post(url, data=data)
                    elif form_details["method"] == "get":
                        res = s.get(url, params=data)
                    if is_vulnerable(res):
                        print("[+] SQL Injection vulnerability detected, link:", url)
                        print("[+] Form:")
                        pprint(form_details)
                        break

        print(str("URL:http://testphp.vulnweb.com/artists.php?artist=1"))
        url = input("URL:")  # input the url
        scan_sql_injection(url)

        b = input("\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            sqli()
        else:
            system('./owasp/main.py')


    except KeyboardInterrupt:
        a = input("Do you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            sqli()
        else:
            system('./owasp/main.py')

#XSS
def xss():
    try:
        system('clear')
        def get_all_forms(url):
            soup = bs(requests.get(url).content, "html.parser")
            return soup.find_all("form")

        def get_form_details(form):
            details = {}
            action = form.attrs.get("action").lower()
            method = form.attrs.get("method", "get").lower()
            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.attrs.get("type", "text")
                input_name = input_tag.attrs.get("name")
                inputs.append({"type": input_type, "name": input_name})
            details["action"] = action
            details["method"] = method
            details["inputs"] = inputs
            return details

        def submit_form(form_details, url, value):
            target_url = urljoin(url, form_details["action"])
            inputs = form_details["inputs"]
            data = {}
            for input in inputs:
                if input["type"] == "text" or input["type"] == "search":
                    input["value"] = value
                input_name = input.get("name")
                input_value = input.get("value")
                if input_name and input_value:
                    data[input_name] = input_value

            if form_details["method"] == "post":
                return requests.post(target_url, data=data)
            else:
                return requests.get(target_url, params=data)

        def scan_xss(url):
            forms = get_all_forms(url)
            print(f"[+] Detected {len(forms)} forms on {url}.")
            js_script = "<Script>alert('hi')</scripT>"
            is_vulnerable = False
            for form in forms:
                form_details = get_form_details(form)
                content = submit_form(form_details, url, js_script).content.decode()
                if js_script in content:
                    print(f"[+] XSS Detected on {url}")
                    print(f"[*] Form details:")
                    pprint(form_details)
                    is_vulnerable = True
            return is_vulnerable

        print("URL: https://xss-game.appspot.com/level1/frame")
        url = input("URL: ")
        print(scan_xss(url))

        b = input("\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            xss()
        else:
            system('./owasp/main.py')


    except KeyboardInterrupt:
        a = input("Do you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            xss()
        else:
            system('./owasp/main.py')

# broken access control
def idor():
    try:
        system("clear")
        urlin = input("Enter Url (http://examble.com/id): ")
        acc_id = input("Enter id from url: ")
        for i in range(10):
            id = acc_id.replace(acc_id[len(acc_id) - 1], str(i))
            id1 = id.replace(id[len(id) - 1], str(i))
            url = urlin.replace(acc_id, id1)
            print(url)
            status_code = urllib.request.urlopen(url).getcode()
            if status_code == 200:
                webbrowser.open(url)
        print("\n\nLooks idor available in these sites check manually")

        b = input("\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            idor()
        else:
            system('./owasp/main.py')
    except KeyboardInterrupt:
        a = input("\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            idor()
        else:
            system('./owasp/main.py')
    except:
        print("""\n\nSeems secure :( 
You can't do idor attack on this website""")
        b = input("\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            idor()
        else:
            system('./owasp/main.py')

#Broken authentication Control
def bac():
    try:
        system('clear')
        url = input("Enter url (http://google.com): ")
        s = requests.Session()
        res = s.get(url)
        cook = s.cookies.get_dict()
        if 'user' in cook or 'username' in cook or 'passwd' in cook or 'password' in cook or 'pass' in cook or 'role' in cook:
            print("\n\n[1] : Chance to be get hacked by broken cookie authentication\n\n")
            print(cook)
        else:
            print("\n\n[1] : Cookie side is secure\n\n")
            print(cook)
        b = input("\n\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            bac()
        else:
            system('./owasp/main.py')

    except KeyboardInterrupt:
        a = input("\n\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            bac()
        else:
            system('./owasp/main.py')
    except:
        print (colored("\n\nYour entry was wrong.\n","red"))
        print(colored("Try correct url format (http://google.com)", "green"))
        time.sleep(5)
        bac()

#sensitive data exposure
def sens():
    try:
        system('clear')
        path = input("Enter wordlist (/usr/share/rockyout.txt): ")
        check = exists(path)
        if check == True:
            sub_list = open(path).read()
            directories = sub_list.splitlines()
            a = input("Enter URL (http://google.com/):")
            print("\n")
            for dir in directories:
                dir_enum = a + dir
                r = requests.get(dir_enum)
                if r.status_code == 404:
                    pass
                else:
                    print("Directory:", dir_enum)
        else:
            print("Wordlist not exist. Try again")
            time.sleep(5)
            sens()
            b = input("\n\n Do you want scan again (y/n): ")
            if b == 'y' or b == 'Y':
                sens()
            else:
                system('./owasp/main.py')

    except KeyboardInterrupt:
        a = input("\n\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            sens()
        else:
            system('./owasp/main.py')

    except:
        print (colored("\n\nYour entry was wrong.\n","red"))
        print(colored("Try correct url format (http://google.com)", "green"))
        time.sleep(5)
        sens()


#Physhing
def phish():
    try:
        system('clear')
        base64_message = 'Lw=='
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        a = message

        def get_url():
            domain = input("\nEnter domain or IP (10.13.1.1 or domain): ")
            if 'ngrok' in domain:
                print("\nThis site seems to be a phishing link")
            else:
                finaldomain = domain + a
                contents = requests.get(
                    'https://api.hetrixtools.com/v2/8f2c60680cdb0cb53b87b68e86a86bda/blacklist-check/domain/'
                    + finaldomain).json()
                url = contents['blacklisted_count']

                if url > 0:
                    print("\ndomain is blaclisted")
                elif url == 0:
                    print("\nThe domain is not a phishing site")

        get_url()
        b = input("\n\n Do you want scan again (y/n): ")
        if b == 'y' or b == 'Y':
            phish()
        else:
            system('./owasp/main.py')
    except KeyboardInterrupt:
        a = input("\n\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            phish()
        else:
            system('./owasp/main.py')

    except:
        print (colored("\n\nYour entry was wrong.\n","red"))
        print(colored("Try correct url format (google.com or IP)", "green"))
        time.sleep(5)
        phish()

#security misconfiguration
def sm():
    try:
        import requests
        import random
        from threading import Thread
        import os

        url = input("Enter url ( https://requestswebsite.notanothercoder.repl.co/confirm-login ): ")
        username = input("Enter username (admin): ")
        n = int(input("Enter password length(8): "))
        tn = int(input("Enter thread count(20): "))

        def send_request(username, password):
            data = {
                "username": username,
                "password": password
            }

            r = requests.get(url, data=data)
            return r

        chars = "abcdefghijklmnopqrstuvwxyz0123456789"

        def main():
            while True:
                if "correct_pass.txt" in os.listdir():
                    break
                valid = False
                while not valid:
                    rndpasswd = random.choices(chars, k=n)
                    passwd = "".join(rndpasswd)
                    file = open("owasp/tries.txt", 'r')
                    tries = file.read()
                    file.close()
                    if passwd in tries:
                        pass
                    else:
                        valid = True

                r = send_request(username, passwd)

                if 'failed to login' in r.text.lower():
                    with open("owasp/tries.txt", "a") as f:
                        f.write(f"{passwd}\n")
                        f.close()
                    print(f"Incorrect {passwd}\n")
                else:
                    print(f"Correct Password {passwd}!\n")
                    with open("correct_pass.txt", "w") as f:
                        f.write(passwd)
                    break

        for x in range(tn): 
            Thread(target=main).start()
    except KeyboardInterrupt:
        a = input("\n\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            sm()
        else:
            system('./owasp/main.py')

    except:
        print (colored("\n\nYour entry was wrong.\n","red"))
        print(colored("Try correct url format (http://google.com)", "green"))
        time.sleep(5)
        sm()

#external xml entity
def xxe():
    try:
        system('clear')
        url = input("Enter url: ")
        x = requests.get(url)
        a = x.headers['Content-Type']
        print('\n\nContent type: ', a)

        if 'xml' in a:
            print("\nThis page seems vulnerable to XML external entity (XXE) injection")
            b = input("\n\n Do you want scan again (y/n): ")
            if b == 'y' or b == 'Y':
                xxe()
            else:
                system('./owasp/main.py')
        else:
            print("\n This page doesn't contain XML data, So this is Secure to XXE")
            b = input("\n\n Do you want scan again (y/n): ")
            if b == 'y' or b == 'Y':
                xxe()
            else:
                system('./owasp/main.py')
    except KeyboardInterrupt:
        a = input("\n\nDo you want to EXIT (y/n): ")
        if a == 'n' or a == 'N':
            xxe()
        else:
            system('./owasp/main.py')

    except:
        print (colored("\n\nYour entry was wrong.\n","red"))
        print(colored("Try correct url format (http://google.com)", "green"))
        time.sleep(5)
        xxe()