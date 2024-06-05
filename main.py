import requests

two = open("2.png", "rb")
requests.put("http://127.0.0.1:8000/set_pfp?uid=0", data=two.read())
two.close()
