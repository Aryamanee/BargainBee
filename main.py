import requests

url = "http://127.0.0.1:8000/set_pfp"
params = {"uid": 0}
files = {"pfp": ("0.png", open("0.png", "rb"), "image/png")}


response = requests.put(url, params=params, files=files)

for i in range(500):
    resp = requests.get(f"http://127.0.0.1:8000/get_account?uid={i}")
    if resp.status_code == 200:
        print(resp.json())
    else:
        print(f"Error Code {resp.status_code}")
