import requests

sub_list = open('/usr/share/wordlists/dirb/small.txt').read()
directories = sub_list.splitlines()
a = input ("Enter URL")

for dir in directories:
    dir_enum = a + dir
    r = requests.get(dir_enum)
    if r.status_code==404:
        pass
    else:
        print("Directory:" ,dir_enum)