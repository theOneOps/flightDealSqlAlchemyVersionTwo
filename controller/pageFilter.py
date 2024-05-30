from view.viewFilter import Search


class ControllerSearch:
    def __init__(self, root, funcGreeting, funcProfil):
        # Clear the existing widgets
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Search view")
        self.view = Search(root)

        self.view.getGreetingBtn().config(command=funcGreeting)

        self.view.getProfilBtn().config(command=funcProfil)

        # self.view.getGreetingBtn()

        # Additional setup if necessary
        print("lets go !")
