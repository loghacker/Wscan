import requests
session = requests.session()
response = session.get('http://google.com')
print(session.cookies.get_dict())
if 'user' in session.cookies.get_dict():
    print("chance to be broken authentication")



