
from view.viewFilter import Search


class ControllerSearch:
    def __init__(self, root):
        for widget in root.winfo_children():
            widget.destroy()

        root.title("Search view")
        self.view = Search(root)


        # self.view.getFilterBtn().config(command=lambda : print("hello world"))

        print("lets go !")

# if __name__ == "__main__":
# root = Tk()
# root.title("Profil view")
# profil = ControllerProfil(root)
# root.mainloop()