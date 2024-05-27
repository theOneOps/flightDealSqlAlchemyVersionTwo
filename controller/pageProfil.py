from tkinter import Tk, messagebox

from model.requests import connectUser, addUser
from view.viewProfil import Profil


class ControllerProfil():
    def __init__(self, root):
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Profil view")
        self.view = Profil(root)


        print("lets go !")




# if __name__ == "__main__":
    # root = Tk()
    # root.title("Profil view")
    # profil = ControllerProfil(root)
    # root.mainloop()