from tkinter import Tk, messagebox

import model.requests
from controller.pageFilter import ControllerSearch
from controller.pageProfil import ControllerProfil
from model.requests import connectUser, addUser
from view.viewConnection import Greeting


def is_not_empty_or_whitespace(entry: str):
    stripped_entry = entry.strip()
    return len(stripped_entry) > 0


class ControllerGreeting():
    def __init__(self, root):
        self.view = Greeting(root)

        def createAccount():
            name_entry = self.view.getNameEntry().get()
            passwd_entry = self.view.getPasswdEntry().get()

            # Check if either entry is empty or filled with only whitespaces
            if not is_not_empty_or_whitespace(
                    name_entry) or not is_not_empty_or_whitespace(
                passwd_entry):
                messagebox.showinfo("Connection",
                                    "The nameEntry and passwordEntry cannot be empty or filled with blanks")
            else:
                isAccountCreate = addUser(name_entry,
                                          passwd_entry,
                                          self.view.getEmailEntry().get())
                if isAccountCreate:
                    messagebox.showinfo("Creation of account",
                                        "You successfully create a new account")
                else:
                    messagebox.showinfo("Creation of account",
                                        "that name is already used, account not "
                                        "created !")

        def returnToWelcomePage():
            for widget in root.winfo_children():
                widget.destroy()

            controller_connection = ControllerGreeting(root)

        def login():
            name_entry = self.view.getNameEntry().get()
            passwd_entry = self.view.getPasswdEntry().get()
            isConnect = connectUser(name_entry,
                                    passwd_entry)
            if isConnect:
                messagebox.showinfo("Connection",
                                    "You successfully logged in !")

                for widget in root.winfo_children():
                    widget.destroy()

                controller_profil = ControllerProfil(root,
                                                     returnToWelcomePage,
                                                     searchFunc)

                # controller_search = ControllerSearch(root,
                # returnToWelcomePage,
                # profilFunc)


            else:
                messagebox.showinfo("Connection",
                                    "the connection failed.\nMaybe your "
                                    "authentication's entries are false !")

        def logoutFunc():
            if model.requests.disconnectUser():
                messagebox.showinfo("Log out trial",
                                    "You successfully logout !")
            else:
                messagebox.showinfo("Log out trial",
                                    "there is no user log in. Log out failed !")


        def searchFunc():
            for widget in root.winfo_children():
                widget.destroy()

            controller_search = ControllerSearch(root,
                                                 returnToWelcomePage,
                                                 profilFunc)

        def profilFunc():
            if model.requests.isUserConnected():
                for widget in root.winfo_children():
                    widget.destroy()
                controller_profil = ControllerProfil(root,
                                                     returnToWelcomePage,
                                                     searchFunc)
            else:
                messagebox.showinfo("Page profil view",
                                    "You need to login first to view your profil!")


        self.view.getProfilBtn().config(command=profilFunc)

        self.view.getSearchBtn().config(command=searchFunc)

        self.view.getLoginBtn().config(command=login)

        self.view.getCreateAccountBtn().config(command=createAccount)

        self.view.getLogoutBtn().config(command=logoutFunc)


if __name__ == "__main__":
    root = Tk()
    root.title("Greeting view")
    profil = ControllerGreeting(root)
    root.mainloop()
