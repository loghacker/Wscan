#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
from os import system

try:
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

    if __name__ == "__main__":
        import sys
        print(str("URL:http://testphp.vulnweb.com/artists.php?artist=1"))
        url = input("URL:")  # input the url
        scan_sql_injection(url)

    b=input("\n Do you want scan again (y/n): ")
    if b=='y' or b=='Y':
        system('./owasp/sqli.py')
    else:
        system('./owasp/main.py')


except KeyboardInterrupt:
    a = input("Do you want to EXIT (y/n): ")
    if a == 'n' or a == 'N':
        system('./owasp/sqli.py')
    else:
        system('./owasp/main.py')