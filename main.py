from kivy.config import Config

Config.set("graphics", "resizable", "1")
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("input", "mouse", "mouse,disable_multitouch")

import requests
from kivy.app import App, Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import plyer
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import os


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

    def new_listing(self, name, desc, uid, price):
        try:
            resp = requests.get(
                f"http://{self.server}/new_listing?name={name}&desc={desc}&uid={uid}&price={price}"
            )
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                print(resp.json())
                return resp.json()["ID"]
            else:
                return None

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

    def get_listing(self, id):
        try:
            resp = requests.get(f"http://{self.server}/get_listing?ID={id}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    def get_listings(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_listings?uid={uid}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
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


class NewListingScreen(Screen):
    pass


class MyListingsPage(Screen):
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
                self.root.get_screen("accountpage").ids.pfp.source = "img/cpfp.png"
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
        backup_cwd = os.getcwd()
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        os.chdir(backup_cwd)
        if len(filename) == 1:
            self.root.get_screen("signup").ids.selected_pfp_signup.source = filename[0]

    def set_pfp(self):
        backup_cwd = os.getcwd()
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        os.chdir(backup_cwd)
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
                print(os.getcwd())
                curr_pfp = open("img/cpfp.png", "wb")
                new_pfp = open(filename[0], "rb")
                curr_pfp.write(new_pfp.read())
                curr_pfp.close()
                new_pfp.close()
                self.root.get_screen("accountpage").ids.pfp.source = filename[0]
            else:
                Popup(
                    title="PFP Error!",
                    content=Label(text="PFP Error!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()

    def choose_listing_photo(self):
        backup_cwd = os.getcwd()
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        os.chdir(backup_cwd)
        if len(filename) == 1:
            self.root.get_screen("newlisting").ids.selected_image_new_listing.source = (
                filename[0]
            )

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

    def new_listing(self):
        result = app.client.new_listing(
            self.root.get_screen("newlisting").ids.listing_name_input.text,
            self.root.get_screen("newlisting").ids.listing_description_input.text,
            app.account["UID"],
            int(self.root.get_screen("newlisting").ids.listing_price_input.text),
        )

        if result != None:
            result_lp = app.client.set_listing_photo(
                self.root.get_screen(
                    "newlisting"
                ).ids.selected_image_new_listing.source,
                result,
            )
            if result_lp:
                Popup(
                    title="Listing Created!",
                    content=Label(text="Congrats! Your Listing has been posted!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()
            else:
                Popup(
                    title="Listing Error!",
                    content=Label(text="Listing Error!"),
                    size_hint=(None, None),
                    size=(400, 400),
                ).open()
        else:
            Popup(
                title="Listing Error!",
                content=Label(text="Listing Error!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()

    def populate_listings(self):
        self.root.get_screen("listingspage").ids.listings.clear_widgets()
        listings = app.client.get_listings(app.account["UID"])
        print(listings)
        for i in listings:
            name = listings[i]["name"]
            self.root.get_screen("listingspage").ids.listings.add_widget(
                Button(text=name, size_hint_y=None, height=100)
            )


app = BargainApp()
app.run()
