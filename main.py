import requests
from kivy.app import App, Widget


class Client:
    def __init__(self, server):
        self.server = server

    def new_account(self, name, username, password):
        try:
            resp = requests.get(
                f"http://{self.server}/new_account?name={name}&username={username}&password={password}"
            )
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return resp.json()["successful"]
            else:
                return False

    def get_account(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_account?uid={uid}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    def get_account_by_username(self, username):
        try:
            resp = requests.get(
                f"http://{self.server}/get_account_by_username?username={username}"
            )
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    def get_pfp(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_pfp?uid={uid}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.content
            else:
                return None

    def get_listing_photo(self, id):
        try:
            resp = requests.get(f"http://{self.server}/get_listing_photo?id={id}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.content
            else:
                return None

    def set_pfp(self, path, uid):
        try:
            resp = requests.put(
                f"http://{self.server}/set_pfp?uid={uid}",
                headers={"Accept": "application/json"},
                files={
                    "pfp": (
                        path.split("/")[-1],
                        open(path, "rb"),
                        "image/jpeg",
                    ),
                },
            )
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    def set_listing_photo(self, path, id):
        try:
            resp = requests.put(
                f"http://{self.server}/set_listing_photo?id={id}",
                headers={"Accept": "application/json"},
                files={
                    "listing_photo": (
                        path.split("/")[-1],
                        open(path, "rb"),
                        "image/jpeg",
                    ),
                },
            )
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    def login(self, username, password):
        try:
            resp = requests.get(
                f"http://{self.server}/login?username={username}&password={password}"
            )
        except requests.exceptions.ConnectionError:
            return {"username": False, "password": False}
        else:
            if resp.status_code != 200:
                return {"username": False, "password": False}
            else:
                return resp.json()


class Screen(Widget):
    client = Client("127.0.0.1:8000")


class BargainApp(App):
    def build(self):
        return Screen()


app = BargainApp()
app.run()
