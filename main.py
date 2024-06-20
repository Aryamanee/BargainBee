# Final Project Client - main.py
# Aryaman Sawhney
# Interacts with the server to create a user experience

# Set the default height and width of the window and disable kivys multitouch emulation(we dont need it)
from kivy.config import Config

Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("input", "mouse", "mouse,disable_multitouch")

# import all of the neccessary libraries - gui, requests, os and time
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import plyer
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os
import time


# the client class, it pairs with the server and sends requests to it
class Client:
    # init function, server is the hostname without the http:// prefix
    def __init__(self, server):
        self.server = server

    # new account function
    def new_account(self, name, username, password):
        # try to request the server to create an account with params
        try:
            resp = requests.get(
                f"http://{self.server}/new_account?name={name}&username={username}&password={password}"
            )
        # return false if it was not possible due to a connection error
        except requests.exceptions.ConnectionError:
            return False
        # return false if it wasnt a status code 200 otherwise return what the server says about the success of the operation
        else:
            if resp.status_code == 200:
                return resp.json()["successful"]
            else:
                return False

    # new listing function
    def new_listing(self, name, desc, uid, price):
        # try to request the server to create a new listing
        try:
            resp = requests.get(
                f"http://{self.server}/new_listing?name={name}&desc={desc}&uid={uid}&price={price}"
            )
        # return none if the thing wasn't successful otherwise return the new listing id
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()["ID"]
            else:
                return None

    # get account function
    def get_account(self, uid):
        # try to get the info: uid, name, username of an account given the uid
        try:
            resp = requests.get(f"http://{self.server}/get_account?uid={uid}")
        # return None if there was some problem otherwise return the account info
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # get account by username function
    def get_account_by_username(self, username):
        # try to get the account info using the username as a username is unique along with a UID
        try:
            resp = requests.get(
                f"http://{self.server}/get_account_by_username?username={username}"
            )
        # return None if there was some problem otherwise return the account info
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # function to try and get the pfp using a uid
    def get_pfp(self, uid):
        # try to get the pfp
        try:
            resp = requests.get(f"http://{self.server}/get_pfp?uid={uid}")
        # if there was a problem, return None otherwise return the bytes of the photo
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.content
            else:
                return None

    # function to get a listing given the id of that listing
    def get_listing(self, id):
        # try getting the listing
        try:
            resp = requests.get(f"http://{self.server}/get_listing?id={id}")
        # return None if there was a problem otherwise return the listing metadata
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # function to get all of the listings of the user
    def get_listings(self, uid):
        # try to get the listing from the server
        try:
            resp = requests.get(f"http://{self.server}/get_listings?uid={uid}")
        # return None if there was a problem otherwise return the listings' metadata
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # function to get a listing photo
    def get_listing_photo(self, id):
        try:
            # request the listing photo from the server
            resp = requests.get(f"http://{self.server}/get_listing_photo?id={id}")
        # return None if there was an error, else return the bytes of the image
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.content
            else:
                return None

    # function to set a profile photo
    def set_pfp(self, path, uid):
        # try to send a put request for a png image for a certain pfp and uid
        try:
            resp = requests.put(
                f"http://{self.server}/set_pfp?uid={uid}",
                headers={"Accept": "application/json"},
                files={
                    "pfp": (
                        path.split("/")[-1],
                        open(path, "rb"),
                        "image/png",
                    ),
                },
            )
        # return true or false, indicating the success
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # function to set a listing photo
    def set_listing_photo(self, path, id):
        # try sending a png image of the listing for a certain uid
        try:
            resp = requests.put(
                f"http://{self.server}/set_listing_photo?id={id}",
                headers={"Accept": "application/json"},
                files={
                    "listing_photo": (
                        path.split("/")[-1],
                        open(path, "rb"),
                        "image/png",
                    ),
                },
            )
        # return true or false, indicating the success
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # login function
    def login(self, username, password):
        # request the server to know what is right or wrong with the username or passwird
        try:
            resp = requests.get(
                f"http://{self.server}/login?username={username}&password={password}"
            )
        # if there is an error, return both parameters as incorrect
        except requests.exceptions.ConnectionError:
            return {"username": False, "password": False}
        # if there is a wrong status code, return both as false and return what the server has to say if it is a successfull request with code 200
        else:
            if resp.status_code != 200:
                return {"username": False, "password": False}
            else:
                return resp.json()

    # get next listign function - recomendations from the server
    def get_next_listing(self, uid):
        # try to get the next recomendation from the server,  tell the user so the server knows what user to cater it towards
        try:
            resp = requests.get(f"http://{self.server}/get_next_listing?uid={uid}")
        # return None if it couldnt find a next listing otherwise return the listing info
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # set view duration function - lets the server know about the users prefs
    def set_view_duration(self, uid, id, duration):
        # try to send the view duration of the listing
        try:
            resp = requests.post(
                f"http://{self.server}/set_view_duration?uid={uid}&id={id}&duration={duration}"
            )
        # return the status of the sending true or false
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # get_basket function
    def get_basket(self, uid):
        # try to get the basket for a certain uid
        try:
            resp = requests.get(f"http://{self.server}/get_basket?uid={uid}")
        # return the basket of the user if successful, otherwise return None
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()
            else:
                return None

    # add to basket func
    def add_to_basket(self, uid, id):
        # try to add to the basket for a certain uid and id of listing
        try:
            resp = requests.get(f"http://{self.server}/add_to_basket?uid={uid}&id={id}")
        # return true or false regarding the success of the request
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # remove from basket func
    def remove_from_basket(self, uid, id):
        # try to remove  the item from the basket
        try:
            resp = requests.get(
                f"http://{self.server}/remove_from_basket?uid={uid}&id={id}"
            )
        # return true or false regarding the status of the request
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # create chat func
    def create_chat(self, P1, P2):
        # try to create a chat between two users
        try:
            resp = requests.get(f"http://{self.server}/create_chat?P1={P1}&P2={P2}")
        # return true or false regarding the success of the request
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # get chat func
    def get_chat(self, P1, P2):
        # try to get the chat between two users
        try:
            resp = requests.get(f"http://{self.server}/get_chat?P1={P1}&P2={P2}")
        # return none if there was some error otherwise return the chat
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()["chat"]
            else:
                return None

    # write message func
    def write_message(self, uid, to, content):
        # try to write the message with the uid its from the uid its to and the content
        try:
            resp = requests.get(
                f"http://{self.server}/write_message?uid={uid}&to={to}&content={content}"
            )
        # return true or false regarding the success of the message sending
        except requests.exceptions.ConnectionError:
            return False
        else:
            if resp.status_code == 200:
                return True
            else:
                return False

    # get chats function - get all the people a certain user is chatting with
    def get_chats(self, uid):
        try:
            resp = requests.get(f"http://{self.server}/get_chats?uid={uid}")
        # return None if there was an error, otherwise return all of the chats
        except requests.exceptions.ConnectionError:
            return None
        else:
            if resp.status_code == 200:
                return resp.json()["chats"]
            else:
                return None


# define all of the screens - they can be empty we will fill them in the kivy file
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


class ChatsScreen(Screen):
    pass


class MessageScreen(Screen):
    pass


# windowmanager class
class WindowManager(ScreenManager):
    # set the swipe threshold to 100 pixels- to scroll to the next listing you must swipe at least 100 pixels
    swipe_threshold = 100

    # init function
    def __init__(self, **kwargs):
        # initialize the parent class
        super().__init__(**kwargs)
        # page1 bool symbolizes weather we are on the first page or second page- there are two pages for seemless scrolling
        self.page1 = True
        # the y value at which the touch started - we will use this later for our swiping functionality as it was easier to make one myself rather than use something from kivy itself
        self.touch_start_y = 0
        # self.history is all of the listing that have happened
        self.history = []
        # current listing is the listing the current user is on
        self.current_listing = -1
        # start_view is the time at which the user started viewing any given listing - will be sent to the server to learn prefs
        self.start_view = 0

    # prepare the screen to show the listing after the explore button has been clicked on the homepage
    def prepare(self):
        # add 1 to the current listing value
        self.current_listing += 1
        # start on page 1
        self.page1 = True
        # add a new listing from the recomendations
        self.history.append(app.client.get_next_listing(app.account["UID"]))
        # set the time we started viewing the listing
        self.start_view = time.time()
        # get the listing id of the new listing then populate all of the screen elements with the info
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
        # finally set the source of the listing image(kivy async image)
        self.get_screen("explore1").ids.image.source = (
            f"http://{app.client.server}/get_listing_photo?id={lID}"
        )

    # touch down function for moving to next listing, save the y value where the finger or mouse touched down
    def on_touch_down(self, touch):
        self.touch_start_y = touch.y
        return super().on_touch_down(touch)

    # touch up function, determine if were on one of the explore pages, if so if we moved down the threshold then go to the previous listing, otherwise go to the next one
    def on_touch_up(self, touch):
        if self.current == "explore1" or self.current == "explore2":
            if self.touch_start_y >= self.height * 0.3:
                if touch.y - self.touch_start_y < -self.swipe_threshold:
                    self.previous_screen()
                elif touch.y - self.touch_start_y > self.swipe_threshold:
                    self.next_screen()
                return super().on_touch_up(touch)

    # next screen function
    def next_screen(self):
        # populate the screen with the next listing, now if we scrolled back and there is already a next listing, no need to load another one otherwise get it to load a new listing
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
        # go to the previous listing if this isnt the first listing, load it in and switch to the other explore page for a seamless transiton
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


# BargainApp class
class BargainApp(App):
    # load the hostname and set the account to none as the user hasnt logged in yet
    hostname_file = open("prefs/server.txt", "r")
    client = Client(hostname_file.read())
    hostname_file.close()
    account = None

    # start a 1 second timer that will be used to update the messages during a chat
    def on_start(self):
        Clock.schedule_interval(self.update_chat, 1)

    # get server function, returns contents of prefs/server.txt
    def get_server(self):
        hostname_file = open("prefs/server.txt", "r")
        hostname = hostname_file.read()
        hostname_file.close()
        return hostname

    # set server function, sets contents of prefs/server.txt
    def set_server(self):
        hostname = app.root.get_screen("changeserver").ids.hostname_input.text
        hostname_file = open("prefs/server.txt", "w")
        hostname_file.write(hostname)
        hostname_file.close()
        app.client.server = hostname

    # build function, loads the kvlang file with all of the gui layouts
    def build(self):
        return Builder.load_file("bargain.kv")

    # login function, uses the stuff entered on the screen, and tries to login using the client class, it moves to the account page if successful otherwise it gives a popup of unsuccessful login depending on the error
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

    # choose pfp, uses plyer to select png file and sets it onto the signup screen as a selected pfp
    def choose_pfp(self):
        backup_cwd = os.getcwd()
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        os.chdir(backup_cwd)
        if len(filename) == 1:
            app.root.get_screen("signup").ids.selected_pfp_signup.source = filename[0]

    # opens a file using plyer and tries to set it using the client, if its successful or not it gives a popup to let you know
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

    # choose listing photo function, sets the selection on the the selected pfp image on the screen for creating a listing
    def choose_listing_photo(self):
        backup_cwd = os.getcwd()
        filename = plyer.filechooser.open_file(filters=["*png"], multiple=False)
        os.chdir(backup_cwd)
        if len(filename) == 1:
            app.root.get_screen("newlisting").ids.selected_image_new_listing.source = (
                filename[0]
            )

    # signup function takes the inputs from the signup screen then uploads the selected image, if all is good it tells you to go login otherwise it tells you an error popup
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

    # new listing function creates the listing and sends the selected listing photo and gives a popup regarding the status
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

    # opens a given listing on an explorepage - useful for the basket and to view your own listings then moves you to the explore page
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

    # populate all of the listings in the mylistings page
    def populate_listings(self):
        # clear all of the listings off the screen letting us update it, this may have been called previously in our instace
        app.root.get_screen("listingspage").ids.listings.clear_widgets()
        # get all of the logged in users listings
        listings = app.client.get_listings(app.account["UID"])
        # if there are listings, go through each of them and add a button which redirects you to view that listing
        if listings != None:
            for i in listings:
                curr_id = listings[i]["ID"]
                name = listings[i]["name"]
                button_name = Button(text=name, size_hint_y=None, height=100)
                button_name.bind(
                    on_release=lambda view, curr_id=curr_id: app.view_listing(curr_id)
                )
                app.root.get_screen("listingspage").ids.listings.add_widget(button_name)
        # if it couldnt get listings give a popup error
        else:
            Popup(
                title="Error Loading Listings!",
                content=Label(text="Error Loading Listings!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()

    # add to basket function just uses the info that this function knows and sends it to the client
    def add_to_basket(self):
        app.client.add_to_basket(
            self.account["UID"], app.root.history[app.root.current_listing]["ID"]
        )

    # this is a redirection from the explore page to open a chat with that seller
    def message_seller(self):
        # create the chat if it doesnt exist, if it already does nothing will happen
        app.client.create_chat(
            self.account["UID"], app.root.history[app.root.current_listing]["UID"]
        )
        # open that chat
        app.open_chat(app.root.history[app.root.current_listing]["UID"])

    # remove from basket function to remove an item from the basket then repopulate the basket to update
    def remove_from_basket(self, id):
        app.client.remove_from_basket(app.account["UID"], id)
        app.populate_basket()

    # fill the basket, similar to the populate listings page but it also adds a button to remove the item from the basket
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

    # populate all of the users current chats
    def populate_messages(self):
        # sort of similar to the other populate functions, just for the current chats and with a buttons that open that chat
        app.root.get_screen("chatsscreen").ids.chats.clear_widgets()
        chats = app.client.get_chats(app.account["UID"])
        if chats != None:
            for user in chats:
                name = user["name"]
                button_name = Button(text=name, size_hint_y=None, height=100)
                curr_id = user["UID"]
                button_name.bind(
                    on_release=lambda chat, curr_id=curr_id: app.open_chat(curr_id)
                )
                app.root.get_screen("chatsscreen").ids.chats.add_widget(button_name)
        else:
            Popup(
                title="Error Loading Chats!",
                content=Label(text="Error Loading Chats!"),
                size_hint=(None, None),
                size=(400, 400),
            ).open()

    # open chat function, uid is the one to open a chat with
    def open_chat(self, uid):
        # populate the messaging screen - similar to other populating screens but place it on the left or right depending on if the message came from the current user or the other user that our user is chatting with
        # we also just add the name of the other user to the top bar
        app.current_chat_uid = uid
        app.root.get_screen("messagescreen").ids.messages.clear_widgets()
        is_second = uid < app.account["UID"]
        user = app.client.get_account(uid)
        app.root.get_screen("messagescreen").ids.name.text = user["name"]
        chat = app.client.get_chat(app.account["UID"], uid)
        for message in chat:
            layout = BoxLayout(size_hint_y=None, height=40)
            if message[1] == is_second:
                message = Label(text=message[0], size_hint=(0.7, 1))
                layout.add_widget(Label(size_hint=(0.3, 1), height=30))
                layout.add_widget(message)
            else:
                message = Label(text=message[0], size_hint=(0.7, 1))
                layout.add_widget(message)
                layout.add_widget(Label(size_hint=(0.3, 1), height=30))
            app.root.get_screen("messagescreen").ids.messages.add_widget(layout)
        app.root.current = "messagescreen"
        app.root.transition.direction = "up"

    # update chat function - relaod all the messages to include any new messages
    def update_chat(self, dt=None):
        if app.root.current == "messagescreen":
            chat = app.client.get_chat(app.account["UID"], app.current_chat_uid)
            is_second = app.current_chat_uid < app.account["UID"]
            app.root.get_screen("messagescreen").ids.messages.clear_widgets()
            for message in chat:
                layout = BoxLayout(size_hint_y=None, height=40)
                if message[1] == is_second:
                    message = Label(text=message[0], size_hint=(0.7, 1))
                    layout.add_widget(Label(size_hint=(0.3, 1), height=30))
                    layout.add_widget(message)
                else:
                    message = Label(text=message[0], size_hint=(0.7, 1))
                    layout.add_widget(message)
                    layout.add_widget(Label(size_hint=(0.3, 1), height=30))
                app.root.get_screen("messagescreen").ids.messages.add_widget(layout)

    # send message function takes what ever is in the textbox, ships it off to the server and then empties the textbox finally it updates the chat
    def send_message(self):
        if app.root.get_screen("messagescreen").ids.new_message.text != "":
            app.client.write_message(
                app.account["UID"],
                app.current_chat_uid,
                app.root.get_screen("messagescreen").ids.new_message.text,
            )
            app.root.get_screen("messagescreen").ids.new_message.text = ""
            self.update_chat()


# run the app
app = BargainApp()
app.run()
