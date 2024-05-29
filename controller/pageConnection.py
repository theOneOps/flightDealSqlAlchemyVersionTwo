from tkinter import Tk, messagebox

from controller.pageProfil import ControllerProfil
from model.requests import connectUser, addUser
from view.viewConnection import Greeting


class ControllerGreeting():
    def __init__(self, root):
        self.view = Greeting(root)

        def createAccount():
            isAccountCreate = addUser(self.view.getNameEntry().get(),
                                      self.view.getPasswdEntry(
                                      ).get(),
                                      self.view.getEmailEntry().get())
            if isAccountCreate:
                messagebox.showinfo("Creation of account",
                                    "You successfully create a new account")
            else:
                messagebox.showinfo("Creation of account",
                                    "that name is already used, account not "
                                    "created !")

        self.view.getCreateAccountBtn().config(command=createAccount)

        def login():
            isConnect = connectUser(self.view.getNameEntry().get(),
                                    self.view.getPasswdEntry(
                                    ).get())
            if isConnect:
                messagebox.showinfo("Connection",
                                    "You successfully logged in !")

                controller_search = ControllerProfil(root)


            else:
                messagebox.showinfo("Connection",
                                    "the connection failed.\nMaybe your "
                                    "authentication's entries are false !")

        self.view.getLoginBtn().config(command=login)


if __name__ == "__main__":
    root = Tk()
    root.title("Greeting view")
    profil = ControllerGreeting(root)
    root.mainloop()
