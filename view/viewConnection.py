from view.widgets_functions import *
from model.requests import userConnect

global userConnect

class Greeting:

    def __init__(self, root: Tk):
        self.root = root
        self.root.geometry("350x500")
        self.container_title = vie_define_frame(self.root, 0, 0, pad=10,
                                                columnspan=True)
        self.title = vie_define_label(self.container_title,
                                      "Welcome to flightDeal !", 20, 0, 0, True)

        self.container_connection = vie_define_lb_frame(self.container_title, 0,
                                                        1, columnspan=True)
        self.container_connection.config(font=5, padx=30)

        self.name_frame = vie_define_frame(self.container_connection, 0, 2)
        self.name_label = vie_define_label(self.name_frame, "Your name", 8, 0,
                                           2, columnspan=True)
        self.name_entry = vie_define_entry(self.name_frame, 20, 0, 3,
                                           columnspan=True)

        if userConnect["id"] is not None:
            self.name_entry.insert(0, userConnect["name"])

        self.passwd_frame = vie_define_frame(self.container_connection, 0, 4)
        self.passwd_label = vie_define_label(self.passwd_frame, "Your password",
                                             8, 0, 4, columnspan=True)
        self.passwd_entry = vie_define_entry(self.passwd_frame, 20, 0, 5,
                                             columnspan=True)

        if userConnect["id"] is not None:
            self.passwd_entry.insert(0, userConnect["passwd"])

        self.email_frame = vie_define_frame(self.container_connection, 0, 5)
        self.email_label = vie_define_label(self.email_frame, "Your email", 8,
                                            0, 5, columnspan=True)
        self.email_entry = vie_define_entry(self.email_frame, 20, 0, 6,
                                            columnspan=True)

        self.btn_create = vie_define_button(self.email_frame, string="create",
                                            col=0, row=7,
                                            function=lambda: print(
                                                "create account"),
                                            columnspan=False)

        self.btn_login = vie_define_button(self.email_frame, string="login",
                                           col=0, row=7,
                                           function=lambda: print("login"),
                                           columnspan=True)

        self.btn_logout = vie_define_button(self.email_frame, string="logout",
                                           col=1, row=7,
                                           function=lambda: print("logout"),
                                           columnspan=False)



        # Correct positions to avoid overlap
        self.btn_quit = vie_define_button(root, string="quit", col=0, row=8,
                                          function=self.quitRoot,
                                          columnspan=False)
        self.btn_profil = vie_define_button(root, string="profil", col=0, row=8,
                                            function=lambda: print("profil"),
                                            columnspan=True)
        self.btn_search = vie_define_button(root, string="search", col=1, row=8,
                                            function=lambda: print("search"),
                                            columnspan=False)

    def quitRoot(self):
        self.root.quit()

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
