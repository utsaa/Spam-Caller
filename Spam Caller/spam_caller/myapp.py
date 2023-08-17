import requests
import json
from requests.auth import HTTPDigestAuth,HTTPBasicAuth

# url="http://127.0.0.1:8000/admin/login/?next=/admin/"
url="http://127.0.0.1:8000/api/phoneapi/auth"
url2="http://127.0.0.1:8000/api/phoneapi/?phone=9088264711"
user="utsa"
pasw="1234"
# r=requests.get(url=url, auth=HTTPBasicAuth(user,pasw))
# print(r.json())

session=requests.Session()
session.auth=(user,pasw)
auth=session.post(url=url)
print(auth)
r=requests.get(url=url2)
print(r.json())