# Import necessary modules and functions
import model.requests
from view.widgets_functions import *  # Import all widget-related functions from the view module
from model.requests import userConnect  # Import userConnect object from the model requests module
from model.utils import center_window  # Import center_window function from the model utils module

global userConnect  # Declare userConnect as a global variable to track user state

# Define the Greeting class to manage the main greeting window
class Greeting:
    def __init__(self, root: Tk):
        self.btn_logout = None
        self.root = root  # Store the root Tkinter window instance
        center_window(self.root, 870, 600)  # Center the window on the screen with specified dimensions
        self.root.geometry("330x480")  # Set the window size

        # Create the title container frame and set its properties
        self.container_title = vie_define_frame(self.root, 0, 0, pad=10, columnspan=True)
        self.title = vie_define_label(self.container_title, "Welcome to flightDeal !", 20, 0, 0, True)

        # Create the connection container frame and set its properties
        self.container_connection = vie_define_lb_frame(self.container_title, 0, 1, columnspan=True)
        self.container_connection.config(font=5, padx=30)

        # Create and configure the name frame and its widgets
        self.name_frame = vie_define_frame(self.container_connection, 0, 2)
        self.name_label = vie_define_label(self.name_frame, "Your name", 8, 0, 2, columnspan=True)
        self.name_entry = vie_define_entry(self.name_frame, 20, 0, 3, columnspan=True)

        # If a user is connected, pre-fill the name entry field
        if userConnect["id"] is not None:
            self.name_entry.insert(0, userConnect["name"])

        # Create and configure the password frame and its widgets
        self.passwd_frame = vie_define_frame(self.container_connection, 0, 4)
        self.passwd_label = vie_define_label(self.passwd_frame, "Your password", 8, 0, 4, columnspan=True)
        self.passwd_entry = vie_define_entry(self.passwd_frame, 20, 0, 5, columnspan=True)

        # If a user is connected, pre-fill the password entry field
        if userConnect["id"] is not None:
            self.passwd_entry.insert(0, userConnect["passwd"])

        # Create and configure the email frame and its widgets
        self.email_frame = vie_define_frame(self.container_connection, 0, 5)
        self.email_label = vie_define_label(self.email_frame, "Your email", 8, 0, 5, columnspan=True)
        self.email_entry = vie_define_entry(self.email_frame, 20, 0, 6, columnspan=True)

        # Create the button frame for account actions
        self.btns_frame = vie_define_frame(self.container_connection, 0, 7)

        # Define and position the Create, Login, and Logout buttons
        self.btn_create = vie_define_button(self.btns_frame, string="Create", col=0, row=7, function=lambda: print("create account"))
        self.btn_login = vie_define_button(self.btns_frame, string="Login", col=1, row=7, function=lambda: print("login"))

        self.btn_logout
        if model.requests.isUserConnected():
            self.btn_logout = vie_define_button(self.btns_frame, string="Logout", col=2, row=7, function=lambda: print("logout"))

        # Define and position the Quit, Profil, and Search buttons
        self.btn_quit = vie_define_button(self.container_title, string="Quit", col=0, row=8, function=self.quitRoot, columnspan=False)
        self.btn_profil = vie_define_button(self.container_title, string="Profil", col=0, row=8, function=lambda: print("profil"), columnspan=True)
        self.btn_search = vie_define_button(self.container_title, string="Search", col=1, row=8, function=lambda: print("search"), columnspan=False)

    # Define the method to quit the root Tkinter window
    def quitRoot(self):
        self.root.quit()

    # Getter methods for entry fields and buttons
    def getNameEntry(self) -> Entry:
        return self.name_entry

    def getPasswdEntry(self) -> Entry:
        return self.passwd_entry

    def getEmailEntry(self) -> Entry:
        return self.email_entry

    def getContainer(self):
        return self.container_title

    def getQuitBtn(self) -> Button:
        return self.btn_quit

    def getLoginBtn(self) -> Button:
        return self.btn_login

    def getLogoutBtn(self) -> Button:
        return self.btn_logout

    def getSearchBtn(self) -> Button:
        return self.btn_search

    def getProfilBtn(self) -> Button:
        return self.btn_profil

    def getCreateAccountBtn(self) -> Button:
        return self.btn_create
