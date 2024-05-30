from view.viewProfil import Profil


class ControllerProfil:
    def __init__(self, root, funcWelcome, funcSearch):
        # Clear the existing widgets
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Profil view")
        self.view = Profil(root)

        self.view.getGreetingBtn().config(command=funcWelcome)
        self.view.getSearchBtn().config(command=funcSearch)

        # Additional setup if necessary
        print("lets go !")
