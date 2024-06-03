from tkinter import Tk, messagebox  # Import necessary modules from Tkinter.

import model.requests  # Import the requests module from the model package.
from controller.pageFilter import ControllerSearch  # Import the search controller.
from controller.pageProfil import ControllerProfil  # Import the profile controller.
from model.requests import connectUser, addUser  # Import user management functions.
from model.utils import center_window  # Import the utility to center the window.
from view.viewConnection import Greeting  # Import the Greeting view class.

# Function to check if a string is not empty or only whitespace.
def is_not_empty_or_whitespace(entry: str):
    stripped_entry = entry.strip()  # Remove leading and trailing whitespace.
    return len(stripped_entry) > 0  # Return True if the string is not empty.

# Define the controller class for the Greeting view.
class ControllerGreeting():
    def __init__(self, root):
        self.root = root  # Store the root Tkinter window.
        self.initialize_greeting_view()  # Initialize the greeting view.

        center_window(self.root, 330, 480)  # Center the window.

    # Method to initialize the Greeting view.
    def initialize_greeting_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear all existing widgets from the window.

        self.view = Greeting(self.root)  # Create a new Greeting view instance.
        center_window(self.root, 330, 480)  # Center the window.
        self.root.geometry("330x480")  # Set the window size.
        self.root.title("Welcome view !")  # Set the window title.

        self.setup_buttons()  # Setup the buttons with their respective commands.

    # Method to setup buttons and their functionalities.
    def setup_buttons(self):
        # Function to create a new account.
        def createAccount():
            name_entry = self.view.getNameEntry().get()  # Get the entered name.
            passwd_entry = self.view.getPasswdEntry().get()  # Get the entered password.
            if not is_not_empty_or_whitespace(name_entry) or not is_not_empty_or_whitespace(passwd_entry):
                messagebox.showinfo("Connection", "The nameEntry and passwordEntry cannot be empty or filled with blanks")
            else:
                isAccountCreate = addUser(name_entry, passwd_entry, self.view.getEmailEntry().get())
                if isAccountCreate:
                    messagebox.showinfo("Creation of account", "You successfully created a new account")
                else:
                    messagebox.showinfo("Creation of account", "That name is already used, account not created!")

        # Function to return to the welcome page.
        def returnToWelcomePage():
            for widget in self.root.winfo_children():
                widget.destroy()  # Clear all existing widgets.
            self.initialize_greeting_view()  # Re-initialize the greeting view.

        # Function to handle user login.
        def login():
            name_entry = self.view.getNameEntry().get()  # Get the entered name.
            passwd_entry = self.view.getPasswdEntry().get()  # Get the entered password.

            if model.requests.isUserConnected():
                messagebox.showinfo("You're already connected",
                                    "Try to disconnect first before login "
                                    "again ! \n")
            else:
                isConnect = connectUser(name_entry,
                                        passwd_entry)  # Attempt to connect the user.
                if isConnect:
                    messagebox.showinfo("Connection",
                                        "You successfully logged in!")
                    for widget in self.root.winfo_children():
                        widget.destroy()  # Clear all existing widgets.
                    ControllerProfil(self.root, returnToWelcomePage,
                                     searchFunc)  # Switch to the profile view.
                else:
                    messagebox.showinfo("Connection",
                                        "The connection failed.\nMaybe your authentication's entries are false!")

        # Function to handle user logout.
        def logoutFunc():
            if model.requests.disconnectUser():
                messagebox.showinfo("Log out trial", "You successfully logged out!")
            else:
                messagebox.showinfo("Log out trial", "There is no user logged in. Log out failed!")

        # Function to handle the search action.
        def searchFunc():
            for widget in self.root.winfo_children():
                widget.destroy()  # Clear all existing widgets.
            ControllerSearch(self.root, returnToWelcomePage, profilFunc)  # Switch to the search view.

        # Function to handle viewing the profile.
        def profilFunc():
            if model.requests.isUserConnected():
                for widget in self.root.winfo_children():
                    widget.destroy()  # Clear all existing widgets.
                ControllerProfil(self.root, returnToWelcomePage, searchFunc)  # Switch to the profile view.
            else:
                messagebox.showinfo("Page profil view", "You need to login first to view your profile!")

        # Assign commands to the buttons in the Greeting view.
        self.view.getProfilBtn().config(command=profilFunc)
        self.view.getSearchBtn().config(command=searchFunc)
        self.view.getLoginBtn().config(command=login)
        self.view.getCreateAccountBtn().config(command=createAccount)
        if model.requests.isUserConnected():
            self.view.getLogoutBtn().config(command=logoutFunc)

# Main execution block.
if __name__ == "__main__":
    root = Tk()  # Create the main Tkinter window.
    root.geometry("330x480")  # Set the window size.
    root.title("Greeting view")  # Set the window title.
    ControllerGreeting(root)  # Instantiate the controller.
    root.mainloop()  # Run the Tkinter main loop.
