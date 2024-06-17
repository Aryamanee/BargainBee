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
from kivy.uix.gridlayout import GridLayout
import os
import time


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
            resp = requests.get(f"http://{self.server}/get_listing?id={id}")
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

    def get_next_listing(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_next_listing?uid={uid}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    def set_view_duration(self, uid, id, duration):
        try:
            resp = requests.post(
                f"http://{self.server}/set_view_duration?uid={uid}&id={id}&duration={duration}"
            )
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    def get_basket(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_basket?uid={uid}")
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    def add_to_basket(self, uid, id):
        try:
            resp = requests.get(f"http://{self.server}/add_to_basket?uid={uid}&id={id}")
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    def remove_from_basket(self, uid, id):
        try:
            resp = requests.get(
                f"http://{self.server}/remove_from_basket?uid={uid}&id={id}"
            )
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False


class LogInScreen(Screen):
    pass


class SignUpScreen(Screen):
    pass


class ChangeServerScreen(Screen):
    pass


class AccountPage(Screen):
    pass


class NewListingScreen(Screen):
    pass


class MyListingsPage(Screen):
    pass


class BasketPage(Screen):
    pass


class ExplorePageOne(Screen):
    pass


class ExplorePageTwo(Screen):
    pass


class WindowManager(ScreenManager):
    swipe_threshold = 100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page1 = True
        self.touch_start_y = 0
        self.history = []
        self.current_listing = -1
        self.start_view = 0

    def prepare(self):
        self.current_listing += 1
        self.page1 = True
        self.history.append(app.client.get_next_listing(app.account["UID"]))
        self.start_view = time.time()
        lID = self.history[self.current_listing]["ID"]
        self.get_screen("explore1").ids.name.text = (
            "Title: "
            + self.history[self.current_listing]["name"]
            + "\nDescription: "
            + self.history[self.current_listing]["desc"]
            + "\nPrice: $"
            + str(self.history[self.current_listing]["price"])
            + "\nSeller: "
            + app.client.get_account(self.history[self.current_listing]["UID"])["name"]
        )
        self.get_screen("explore1").ids.image.source = (
            f"http://{app.client.server}/get_listing_photo?id={lID}"
        )

    def on_touch_down(self, touch):
        self.touch_start_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.current == "explore1" or self.current == "explore2":
            if self.touch_start_y >= self.height * 0.3:
                if touch.y - self.touch_start_y < -self.swipe_threshold:
                    self.previous_screen()
                elif touch.y - self.touch_start_y > self.swipe_threshold:
                    self.next_screen()
                return super().on_touch_up(touch)

    def next_screen(self):
        app.client.set_view_duration(
            app.account["UID"],
            self.history[self.current_listing]["ID"],
            time.time() - self.start_view,
        )
        self.start_view = time.time()
        self.current_listing += 1
        if self.current_listing == len(self.history):
            self.history.append(app.client.get_next_listing(app.account["UID"]))
        self.page1 = not self.page1
        lID = self.history[self.current_listing]["ID"]
        if self.page1:
            self.get_screen("explore1").ids.name.text = self.get_screen(
                "explore1"
            ).ids.name.text = (
                "Title: "
                + self.history[self.current_listing]["name"]
                + "\nDescription: "
                + self.history[self.current_listing]["desc"]
                + "\nPrice: $"
                + str(self.history[self.current_listing]["price"])
                + "\nSeller: "
                + app.client.get_account(self.history[self.current_listing]["UID"])[
                    "name"
                ]
            )
            self.get_screen("explore1").ids.image.source = (
                f"http://{app.client.server}/get_listing_photo?id={lID}"
            )
            self.current = "explore1"
        else:
            self.get_screen("explore2").ids.name.text = self.get_screen(
                "explore1"
            ).ids.name.text = (
                "Title: "
                + self.history[self.current_listing]["name"]
                + "\nDescription: "
                + self.history[self.current_listing]["desc"]
                + "\nPrice: $"
                + str(self.history[self.current_listing]["price"])
                + "\nSeller: "
                + app.client.get_account(self.history[self.current_listing]["UID"])[
                    "name"
                ]
            )
            self.get_screen("explore2").ids.image.source = (
                f"http://{app.client.server}/get_listing_photo?id={lID}"
            )
            self.current = "explore2"
        self.transition.direction = "up"

    def previous_screen(self):
        if self.current_listing > 0:
            app.client.set_view_duration(
                app.account["UID"],
                self.history[self.current_listing]["ID"],
                time.time() - self.start_view,
            )
            self.start_view = time.time()
            self.current_listing -= 1
            self.page1 = not self.page1
            lID = self.history[self.current_listing]["ID"]
            if self.page1:
                self.get_screen("explore1").ids.name.text = self.get_screen(
                    "explore1"
                ).ids.name.text = (
                    "Title: "
                    + self.history[self.current_listing]["name"]
                    + "\nDescription: "
                    + self.history[self.current_listing]["desc"]
                    + "\nPrice: $"
                    + str(self.history[self.current_listing]["price"])
                    + "\nSeller: "
                    + app.client.get_account(self.history[self.current_listing]["UID"])[
                        "name"
                    ]
                )
                self.get_screen("explore1").ids.image.source = (
                    f"http://{app.client.server}/get_listing_photo?id={lID}"
                )
                self.current = "explore1"
            else:
                self.get_screen("explore2").ids.name.text = self.get_screen(
                    "explore1"
                ).ids.name.text = (
                    "Title: "
                    + self.history[self.current_listing]["name"]
                    + "\nDescription: "
                    + self.history[self.current_listing]["desc"]
                    + "\nPrice: $"
                    + str(self.history[self.current_listing]["price"])
                    + "\nSeller: "
                    + app.client.get_account(self.history[self.current_listing]["UID"])[
                        "name"
                    ]
                )
                self.get_screen("explore2").ids.image.source = (
                    f"http://{app.client.server}/get_listing_photo?id={lID}"
                )
                self.current = "explore2"
            self.transition.direction = "down"


class BargainApp(App):
    hostname_file = open("prefs/server.txt", "r")
    client = Client(hostname_file.read())
    hostname_file.close()
    account = None

    def get_server(self):
        hostname_file = open("prefs/server.txt", "r")
        hostname = hostname_file.read()
        hostname_file.close()
        return hostname

    def set_server(self):
        hostname = app.root.get_screen("changeserver").ids.hostname_input.text
        hostname_file = open("prefs/server.txt", "w")
        hostname_file.write(hostname)
        hostname_file.close()
        app.client.server = hostname

    def build(self):
        return Builder.load_file("bargain.kv")

    def login(self):
        loginstat = self.client.login(
            app.root.get_screen("login").ids.login_username_input.text,
            app.root.get_screen("login").ids.login_password_input.text,
        )
        if loginstat["username"]:
            if loginstat["password"]:
                app.account = app.client.get_account_by_username(
                    app.root.get_screen("login").ids.login_username_input.text
                )
                curr_pfp = open("img/cpfp.png", "wb")
                curr_pfp.write(app.client.get_pfp(app.account["UID"]))
                curr_pfp.close()
                app.root.get_screen("accountpage").ids.hello_text.text = (
                    "Hello, " + app.account["name"].split(" ")[0] + "!"
                )
                app.root.get_screen("accountpage").ids.pfp.source = "img/cpfp.png"
                app.root.current = "accountpage"
                app.root.get_screen("login").manager.transition.direction = "up"
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
            app.root.get_screen("signup").ids.selected_pfp_signup.source = filename[0]

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
                curr_pfp = open("img/cpfp.png", "wb")
                new_pfp = open(filename[0], "rb")
                curr_pfp.write(new_pfp.read())
                curr_pfp.close()
                new_pfp.close()
                app.root.get_screen("accountpage").ids.pfp.source = filename[0]
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
            app.root.get_screen("newlisting").ids.selected_image_new_listing.source = (
                filename[0]
            )

    def signup(self):
        result = app.client.new_account(
            app.root.get_screen("signup").ids.signup_name_input.text,
            app.root.get_screen("signup").ids.signup_username_input.text,
            app.root.get_screen("signup").ids.signup_password_input.text,
        )
        if result:
            result_uid = app.client.get_account_by_username(
                app.root.get_screen("signup").ids.signup_username_input.text
            )
            if result_uid != None:
                result_pfp = app.client.set_pfp(
                    app.root.get_screen("signup").ids.selected_pfp_signup.source,
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
            app.root.get_screen("newlisting").ids.listing_name_input.text,
            app.root.get_screen("newlisting").ids.listing_description_input.text,
            app.account["UID"],
            int(app.root.get_screen("newlisting").ids.listing_price_input.text),
        )

        if result != None:
            result_lp = app.client.set_listing_photo(
                app.root.get_screen("newlisting").ids.selected_image_new_listing.source,
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

    def view_listing(self, id):
        app.root.current_listing += 1
        app.root.page1 = True
        app.root.history.append(app.client.get_listing(id))
        app.root.start_view = time.time()
        app.root.get_screen("explore1").ids.name.text = (
            "Title: "
            + app.root.history[app.root.current_listing]["name"]
            + "\nDescription: "
            + app.root.history[app.root.current_listing]["desc"]
            + "\nPrice: $"
            + str(app.root.history[app.root.current_listing]["price"])
            + "\nSeller: "
            + app.client.get_account(app.root.history[app.root.current_listing]["UID"])[
                "name"
            ]
        )
        app.root.get_screen("explore1").ids.image.source = (
            f"http://{app.client.server}/get_listing_photo?id={id}"
        )
        app.root.current = "explore1"
        app.root.transition.direction = "down"

    def populate_listings(self):
        app.root.get_screen("listingspage").ids.listings.clear_widgets()
        listings = app.client.get_listings(app.account["UID"])
        if listings != None:
            for i in listings:
                curr_id = listings[i]["ID"]
                name = listings[i]["name"]
                button_name = Button(text=name, size_hint_y=None, height=100)
                button_name.bind(
                    on_release=lambda view, curr_id=curr_id: app.view_listing(curr_id)
                )
                app.root.get_screen("listingspage").ids.listings.add_widget(button_name)
        else:
            Popup(
                title="Error Loading Listings!",
                content=Label(text="Error Loading Listings!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()

    def add_to_basket(self):
        app.client.add_to_basket(
            self.account["UID"], app.root.history[app.root.current_listing]["ID"]
        )

    def remove_from_basket(self, id):
        app.client.remove_from_basket(app.account["UID"], id)
        app.populate_basket()

    def populate_basket(self):
        app.root.get_screen("basketpage").ids.listings.clear_widgets()
        listings = app.client.get_basket(app.account["UID"])
        if listings != None:
            for i in listings:
                name = listings[i]["name"]
                layout = GridLayout(rows=1, cols=2, size_hint_y=None, height=100)
                button_name = Button(text=name, size_hint_y=None, height=100)
                button_delete = Button(text="Remove")
                curr_id = listings[i]["ID"]
                button_name.bind(
                    on_release=lambda view, curr_id=curr_id: app.view_listing(curr_id)
                )
                button_delete.bind(
                    on_release=lambda delete, curr_id=curr_id: app.remove_from_basket(
                        curr_id
                    )
                )
                layout.add_widget(button_name)
                layout.add_widget(button_delete)
                app.root.get_screen("basketpage").ids.listings.add_widget(layout)
        else:
            Popup(
                title="Error Loading Basket!",
                content=Label(text="Error Loading Basket!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()


app = BargainApp()
app.run()
