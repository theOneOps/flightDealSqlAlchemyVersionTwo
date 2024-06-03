from tkinter import messagebox
from typing import Union, TypedDict
import model.utils
from model.utils import center_window
from model.requests import *
from view.widgets_functions import *


# Define a custom TypedDict to specify the structure of dictionary items used in the class.
class myDict(TypedDict):
    parent: Union[Widget, None]
    type_seat: str
    id_vol: str
    provider_name: str
    country_dep: str
    country_arr: str
    date_dep: str
    date_arr: str
    date_book: str
    price: str
    id_book: str
    Action: int  # 0 -> "Action", 1 -> "Add's button", 2 -> "Complete"
    row: int


# Define the Profil class, which inherits from Tkinter's Frame class.
class Profil(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)  # Initialize the parent class.
        self.filter_frame = None
        self.root = root
        self.row = 0
        self.results = []
        center_window(self.root, 1100, 540)  # Center the window on the screen.
        self.root.geometry("1140x540")
        self.grid(
            sticky=NSEW)  # Ensure the frame fills the window using grid layout.
        self.create_scrollable_canvas()
        self.filterframeCreate()

    # Create a scrollable canvas within the frame.
    def create_scrollable_canvas(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create the canvas.
        self.canvas = Canvas(self)
        self.canvas.config(width=1120, height=200)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        # Add a vertical scrollbar to the canvas.
        self.scrollbar = Scrollbar(self, orient="vertical",
                                   command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky=NS)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas.
        self.content_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor=NW)

        # Bind the frame's size change to adjust the canvas scroll region.
        self.content_frame.bind("<Configure>", self.on_frame_configure)

        # Add initial content to the content_frame.
        self.add_content()

    # Update the scroll region of the canvas when the frame's size changes.
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Reload the content based on the current filter settings.
    def reload(self):
        selected_seat_type = self.type_seat_var.get()
        selected_country_dep = self.country_dep_var.get()
        selected_country_arr = self.country_dest_var.get()
        selected_date_dep = self.date_dep_var.get()
        selected_date_arr = self.date_arr_var.get()
        selected_date_book = self.date_book_var.get()
        selected_price = self.price_var.get()
        selected_provider_name = self.provider_name_var.get()
        selected_cmp = self.cmp_var.get()

        if selected_price != "":
            selected_price = float(selected_price)
        else:
            selected_price = math.inf

        self.add_content(selected_seat_type, selected_date_dep,
                         selected_date_arr, selected_date_book,
                         selected_country_dep, selected_country_arr,
                         selected_price, selected_cmp, selected_provider_name)

    # Add content to the content_frame based on the filter criteria.
    def add_content(self, type_seat="", date_dep="", date_arr="", date_book="",
                    country_dep="", country_arr="", price=math.inf,
                    cmp="equals", providerName=""):

        # Clear previous content.
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Search for bookings based on the filter criteria.
        self.results = searchBook(type_seat, date_dep, date_arr, date_book,
                                  country_dep, country_arr, price, cmp,
                                  providerName)

        self.row = 0

        # Create header row.
        self.create_title_Value({
            "parent": self.content_frame,
            "id_vol": "flight_number",
            "country_dep": "country_dep",
            "country_arr": "country_arr",
            "date_dep": "date_dep",
            "date_arr": "date_arr",
            "date_book": "date_book",
            "price": "price",
            "id_book": "id_book",
            "provider_name": "provider_name",
            "type_seat": "type_seat",
            "Action": 0,
            "row": self.row,
        })

        self.row += 1

        # Populate the content with booking details.
        idx = 0
        for flight, procure, classe, price, provider, book in self.results:
            self.create_title_Value(
                {
                    "parent": self.content_frame,
                    "id_vol": book.flight_number,
                    "country_dep": flight.country_dep,
                    "country_arr": flight.country_arr,
                    "date_dep": flight.date_dep,
                    "date_arr": flight.date_arr,
                    "date_book": book.date_book,
                    "price": price.price_value,
                    "id_book": book.id_book,
                    "provider_name": provider.name_provider,
                    "type_seat": classe.name_class,
                    "Action": 1,  # if capacity_left[idx] else 2,
                    "row": self.row,
                }
            )
            idx += 1
            self.row += 1

    # Create the filter frame with various filter options.
    def filterframeCreate(self):
        if self.filter_frame is not None:
            for widget in self.filter_frame.winfo_children():
                widget.destroy()

        self.filter_frame = vie_define_lb_frame(self.root, 0, self.row,
                                                columnspan=False)

        values = model.utils.classes_names

        frame_type_seat: Frame = vie_define_frame(self.filter_frame, 0,
                                                  self.row)
        type_seat_label: Label = vie_define_label(frame_type_seat, "type_seat",
                                                  10, 0, self.row, True)

        self.type_seat_var = StringVar()
        self.combobox_type_seat: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.type_seat_var, row=self.row + 1,
            width=10)

        values = list(set(getResultsFrom(searchBook(), False)["price"]))

        frame_price: Frame = vie_define_frame(self.filter_frame, 1, self.row)
        price_label: Label = vie_define_label(frame_price, "price", 10, 1,
                                              self.row, True)

        self.price_var = StringVar()
        self.Combobox_price: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.price_var, col=1, row=self.row + 1,
            width=10)

        values = ("equals", "supequals", "infequals", "inf", "sup")

        frame_cmp: Frame = vie_define_frame(self.filter_frame, 2, self.row)
        cmp_label: Label = vie_define_label(frame_cmp, "cmp", 10, 2, self.row,
                                            True)

        self.cmp_var = StringVar()
        self.Combobox_cmp: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.cmp_var, col=2, row=self.row + 1,
            width=10)

        values = list(set(getResultsFrom(searchBook(), False)["country_dep"]))

        frame_country_dep: Frame = vie_define_frame(self.filter_frame, 3,
                                                    self.row)
        country_dep_label: Label = vie_define_label(frame_country_dep,
                                                    "country_dep", 10, 3,
                                                    self.row, True)
        self.country_dep_var = StringVar()
        self.Combobox_country_dep: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.country_dep_var, col=3,
            row=self.row + 1, width=10)

        self.row += 2

        values = list(set(getResultsFrom(searchBook(), False)["country_arr"]))

        frame_country_arr: Frame = vie_define_frame(self.filter_frame, 0,
                                                    self.row)
        country_arr_label: Label = vie_define_label(frame_country_arr,
                                                    "country_arr", 10, 0,
                                                    self.row, True)
        self.country_dest_var = StringVar()
        self.Combobox_country_arr: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.country_dest_var, col=0,
            row=self.row + 1, width=10)

        values = list(set(getResultsFrom(searchBook(), False)["date_dep"]))

        frame_date_dep: Frame = vie_define_frame(self.filter_frame, 1, self.row)
        date_dep_label: Label = vie_define_label(frame_date_dep, "date_dep", 10,
                                                 1, self.row, True)
        self.date_dep_var = StringVar()
        self.Combobox_date_dep: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.date_dep_var, col=1,
            row=self.row + 1, width=10)

        values = list(set(getResultsFrom(searchBook(), False)["date_arr"]))

        frame_date_arr: Frame = vie_define_frame(self.filter_frame, 2, self.row)
        date_arr_label: Label = vie_define_label(frame_date_arr, "date_arr", 10,
                                                 2, self.row, True)
        self.date_arr_var = StringVar()
        self.Combobox_date_arr: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.date_arr_var, col=2,
            row=self.row + 1, width=10)

        values = list(set(getResultsFrom(searchBook(), False)["provider_name"]))

        frame_provider: Frame = vie_define_frame(self.filter_frame, 3, self.row)
        provider_name_label: Label = vie_define_label(frame_provider,
                                                      "provider_name", 10, 3,
                                                      self.row, True)
        self.provider_name_var = StringVar()
        self.Combobox_provider_arr: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.provider_name_var, col=3,
            row=self.row + 1, width=10)

        values = list(set(getResultsFrom(searchBook(), False)["date_book"]))

        self.row += 2

        frame_date_book: Frame = vie_define_frame(self.filter_frame, 1,
                                                  self.row, columnspan=True)
        date_book_label: Label = vie_define_label(frame_date_book, "date_book",
                                                  10, 1, self.row, True)
        self.date_book_var = StringVar()
        self.Combobox_date_book: Combobox = vie_define_combobox_2(
            self.filter_frame, values, self.date_book_var, col=1,
            row=self.row + 1, width=10, columnspan=True)

        self.row += 2

        # Define the filter button
        self.btn_filter: Button = vie_define_button(self.filter_frame,
                                                    self.reload, "filter", 1,
                                                    self.row, True, width=10)

        self.row += 1

        # Define the container for navigation buttons
        self.container: Frame = vie_define_frame(self.root, 0, self.row)

        self.btn_greeting: Button = vie_define_button(self.container,
                                                      lambda: print("greeting"),
                                                      "greeting", col=0,
                                                      row=self.row + 1)
        self.btn_search: Button = vie_define_button(self.container,
                                                    lambda: print("search"),
                                                    "search", col=1,
                                                    row=self.row + 1)
        self.btn_quit: Button = vie_define_button(self.container,
                                                  lambda: self.root.quit(),
                                                  "quit", col=2,
                                                  row=self.row + 1)

    def getGreetingBtn(self):
        return self.btn_greeting

    def getSearchBtn(self):
        return self.btn_search

    # Define a button with a check to cancel a booking if the user is logged in.
    def vie_define_button_with_check(self, l_print, text, col, row,
                                     columnspan=False):
        def action():
            if isUserConnected():
                cancelBookingFlight(int(l_print["id_book"]))
                self.reload()
            else:
                messagebox.showinfo("Cancel Book's trial",
                                    "you need to login first before canceling a trial")

        return vie_define_button(l_print["parent"], action, text, col, row,
                                 columnspan)

    # Create title and value labels for the content.
    def create_title_Value(self, l_print):
        col = 0

        for i in l_print.keys():
            if i not in ["row", "parent", "Action", "id_book"]:
                label_title = vie_define_label(l_print["parent"], l_print[i], 8,
                                               col, l_print["row"], False,
                                               bg="white", fill="black")
                label_title.config(padx=10)
                col += 1

        if l_print["Action"] == 0:
            label_title = vie_define_label(l_print["parent"], "Action", 8, col,
                                           l_print["row"], False, bg="white",
                                           fill="black")
            label_title.config(padx=10)
        elif l_print["Action"] == 1:
            button_Action = self.vie_define_button_with_check(l_print, "Cancel",
                                                              col,
                                                              l_print["row"])
        else:
            label_title = vie_define_label(l_print["parent"], "Complete", 8,
                                           col, l_print["row"], False,
                                           bg="white", fill="black")
            label_title.config(padx=10)
            col += 1


if __name__ == "__main__":
    root = Tk()
    root.title("Profil view")
    root.config(bg=COLOR_HEX)
    vue_profil = Profil(root)
    root.mainloop()
