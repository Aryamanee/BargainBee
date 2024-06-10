from kivy.config import Config

Config.set("graphics", "resizable", "1")
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")

import requests
from kivy.app import App, Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import plyer
from kivy.uix.popup import Popup
from kivy.uix.label import Label


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


class LogInScreen(Screen):
    pass


class SignUpScreen(Screen):
    pass


class AccountPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class BargainApp(App):
    client = Client("localhost:8000")
    account = None

    def build(self):
        return Builder.load_file("bargain.kv")

    def login(self):
        loginstat = self.client.login(
            self.root.get_screen("login").ids.login_username_input.text,
            self.root.get_screen("login").ids.login_password_input.text,
        )
        if loginstat["username"]:
            if loginstat["password"]:
                app.account = app.client.get_account_by_username(
                    self.root.get_screen("login").ids.login_username_input.text
                )
                curr_pfp = open("img/cpfp.png", "wb")
                curr_pfp.write(app.client.get_pfp(app.account["UID"]))
                curr_pfp.close()
                self.root.get_screen("accountpage").ids.hello_text.text = (
                    "Hello, " + app.account["name"].split(" ")[0] + "!"
                )
                self.root.get_screen("accountpage").ids.pfp.reload()
                app.root.current = "accountpage"
                self.root.get_screen("login").manager.transition.direction = "up"
            else:
                Popup(
                    title="Incorrect Password!",
                    content=Label(text="Incorrect Password!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()
        else:
            Popup(
                title="Login Error!",
                content=Label(text="Incorrect Username or Login Error!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()

    def choose_pfp(self):
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        if len(filename) == 1:
            self.root.get_screen("signup").ids.selected_pfp_signup.source = filename[0]

    def set_pfp(self):
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        if len(filename) == 1:
            result_pfp = app.client.set_pfp(
                filename[0],
                app.account["UID"],
            )
            if result_pfp:
                Popup(
                    title="Succesful PFP Change!",
                    content=Label(text="PFP Change Successful!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()
                self.root.get_screen("accountpage").ids.pfp.source = filename[0]
            else:
                Popup(
                    title="Signup Error!",
                    content=Label(text="Signup Error!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()

    def signup(self):
        result = app.client.new_account(
            self.root.get_screen("signup").ids.signup_name_input.text,
            self.root.get_screen("signup").ids.signup_username_input.text,
            self.root.get_screen("signup").ids.signup_password_input.text,
        )
        if result:
            result_uid = app.client.get_account_by_username(
                self.root.get_screen("signup").ids.signup_username_input.text
            )
            if result_uid != None:
                result_pfp = app.client.set_pfp(
                    self.root.get_screen("signup").ids.selected_pfp_signup.source,
                    result_uid["UID"],
                )
                if result_pfp:
                    Popup(
                        title="Succesful Signup!",
                        content=Label(text="Successful Signup! Go Login Now."),
                        size_hint=(None, None),
                        size=(400, 400),
                    ).open()
                else:
                    Popup(
                        title="Signup Error!",
                        content=Label(text="Signup Error!"),
                        size_hint=(None, None),
                        size=(400, 400),
                    ).open()
            else:
                Popup(
                    title="Signup Error!",
                    content=Label(text="Signup Error!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()
        else:
            Popup(
                title="Signup Error!",
                content=Label(text="Username Taken or Signup Error!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()


app = BargainApp()
app.run()
