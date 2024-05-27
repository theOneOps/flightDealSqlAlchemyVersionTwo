from view.widgets_functions import *


class Greeting:

    def __init__(self, root: Tk):

        self.root = root
        self.container_title: Frame = vie_define_frame(self.root, 0, 0, pad=10,
                                                       columnspan=True)
        self.title: Label = vie_define_label(self.container_title, "Welcome to "
                                                                   "flightDeal !",
                                             20, 0, 0, True)

        self.container_connection: LabelFrame = vie_define_lb_frame(
            self.container_title,
            0, 1,
            columnspan=True)

        self.container_connection.config(font=5, padx=30)

        self.name_frame: Frame = vie_define_frame(self.container_connection, 0,
                                                  2)
        self.name_label: Label = vie_define_label(self.name_frame, "Your name",
                                                  8,
                                                  0, 2, columnspan=True)
        self.name_entry: Entry = vie_define_entry(self.name_frame, 20, 0, 3,
                                                  columnspan=True)

        self.passwd_frame: Frame = vie_define_frame(self.container_connection,
                                                    0, 4)
        self.passwd_label: Label = vie_define_label(self.passwd_frame,
                                                    "Your password", 8,
                                                    0, 4, columnspan=True)
        self.passwd_entry: Entry = vie_define_entry(self.passwd_frame, 20, 0, 5,
                                                    columnspan=True)

        self.email_frame: Frame = vie_define_frame(self.container_connection,
                                                    0, 5)
        self.email_label: Label = vie_define_label(self.passwd_frame,
                                                    "Your email", 8,
                                                    0, 5, columnspan=True)
        self.email_entry: Entry = vie_define_entry(self.passwd_frame, 20, 0, 6,
                                                    columnspan=True)


        self.btn_create: Button = vie_define_button(self.passwd_frame,
                                                    string="create", col=0,
                                                    row=7,
                                                    function=lambda: print(
                                                        "create account"),
                                                    columnspan=False)

        self.btn_login: Button = vie_define_button(self.passwd_frame,
                                                   string="login", col=1, row=7,
                                                   function=lambda: print(
                                                       "login"),
                                                   columnspan=False)


        self.btn_quit: Button = vie_define_button(root,
                                                  string="quit", col=0, row=7,
                                                  function=self.quitRoot)

        self.btn_search: Button = vie_define_button(root,
                                                    string="search", col=1,
                                                    row=7,
                                                    function=lambda: print(
                                                        "search"),
                                                    columnspan=True)

    def quitRoot(self):
        self.root.quit()
    def getNameEntry(self) -> Entry:
        return self.name_entry

    def getPasswdEntry(self) -> Entry:
        return self.passwd_entry

    def getEmailEntry(self) -> Entry:
        return self.email_entry

    def getLoginBtn(self) -> Button:
        return self.btn_login

    def getCreateAccountBtn(self) -> Button:
        return self.btn_create

