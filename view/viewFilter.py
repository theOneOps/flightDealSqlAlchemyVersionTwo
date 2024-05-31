from typing import Union, TypedDict

import model.utils
from model.requests import *
from view.widgets_functions import *


class myDict(TypedDict):
    parent: Union[
        Widget, None]
    type_seat: str
    id_vol: str
    provider_name: str
    country_dep: str
    country_arr: str
    date_dep: str
    date_arr: str
    price: str
    Action: int  # 0 -> "Action" 1 -> Add's button, 2:"Complet"
    row: int


class Search(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.filter_frame = None
        self.root = root
        self.row = 0
        self.results = []
        self.root.geometry("870x600")
        self.grid(
            sticky=NSEW)  # Ensure the frame is placed and fills the window using grid
        self.create_scrollable_canvas()
        self.filterframeCreate()

    def create_scrollable_canvas(self):
        # Configure the grid of the root
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create a canvas
        self.canvas = Canvas(self)
        self.canvas.config(width=840, height=300)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        # Add a scrollbar to the canvas
        self.scrollbar = Scrollbar(self, orient="vertical",
                                   command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky=NS)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.content_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor=NW)

        # Bind the frame's size change to adjust the canvas scroll region
        self.content_frame.bind("<Configure>", self.on_frame_configure)

        # Add some content to the content_frame
        self.add_content()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def reload(self):
        selected_seat_type = self.type_seat_var.get()
        selected_country_dep = self.country_dep_var.get()
        selected_country_arr = self.country_dest_var.get()
        selected_date_dep = self.date_dep_var.get()
        selected_date_arr = self.date_arr_var.get()
        selected_price = self.price_var.get()
        selected_provider_name = self.provider_name_var.get()
        selected_cmp = self.cmp_var.get()

        if selected_price != "":
            selected_price = float(selected_price)
        else:
            selected_price = math.inf
        self.add_content(selected_seat_type, selected_date_dep,
                         selected_date_arr,
                         selected_country_dep,
                         selected_country_arr, selected_price, selected_cmp,
                         selected_provider_name)

    def add_content(self, type_seat="", date_dep="", date_arr="",
                    country_dep="", country_arr="", price=math.inf,
                    cmp="equals", providerName=""):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.results = searchFlight(type_seat, date_dep, date_arr, country_dep,
                                    country_arr, price,
                                    cmp, providerName)
        self.row = 0
        self.create_title_Value({
            "parent": self.content_frame,
            "id_vol": "id_vol",
            "country_dep": "country_dep",
            "country_arr": "country_arr",
            "date_dep": "date_dep",
            "date_arr": "date_arr",
            "price": "price",
            "type_seat": "type_seat",
            "Action": 0,
            "row": self.row,
        })
        self.row += 1
        idx = 0
        capacity_left = getResultsFrom(self.results)["capacity_left"]
        for flight, procure, classe, price, provider in self.results:
            self.create_title_Value(
                {
                    "parent": self.content_frame,
                    "id_vol": flight.id_flight,
                    "country_dep": flight.country_dep,
                    "country_arr": flight.country_arr,
                    "date_dep": flight.date_dep,
                    "date_arr": flight.date_arr,
                    "price": price.price_value,
                    "type_seat": classe.name_class,
                    "Action": 1 if capacity_left[idx] else 2,
                    "row": self.row,
                    "provider_name": provider.name_provider
                }
            )
            idx += 1
            self.row += 1

    def filterframeCreate(self):
        if self.filter_frame is not None:
            for widget in self.filter_frame.winfo_children():
                widget.destroy()

        self.filter_frame = vie_define_lb_frame(self.root, 0,
                                                self.row,
                                                columnspan=True)

        values = model.utils.classes_names

        frame_type_seat: Frame = vie_define_frame(self.filter_frame, 0,
                                                  self.row)
        type_seat_label: Label = vie_define_label(frame_type_seat,
                                                  "type_seat", 10, 0, self.row,
                                                  True)

        self.type_seat_var = StringVar()
        self.combobox_type_seat: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.type_seat_var, row=self.row + 1, width=10)

        values = getResultsFrom(searchFlight())["price"]

        frame_price: Frame = vie_define_frame(self.filter_frame, 1,
                                              self.row)
        price_label: Label = vie_define_label(frame_price,
                                              "price", 10, 1, self.row,
                                              True)

        self.price_var = StringVar()
        self.Combobox_price: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.price_var,
            col=1, row=self.row + 1, width=10)

        values = ("equals", "supequals", "infequals", "inf", "sup")

        frame_cmp: Frame = vie_define_frame(self.filter_frame, 2,
                                            self.row)
        cmp_label: Label = vie_define_label(frame_cmp,
                                            "cmp", 10, 2, self.row,
                                            True)

        self.cmp_var = StringVar()
        self.Combobox_cmp: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.cmp_var,
            col=2, row=self.row + 1, width=10)

        values = getResultsFrom(searchFlight())["country_dep"]

        frame_country_dep: Frame = vie_define_frame(self.filter_frame, 3,
                                                    self.row)
        country_dep_label: Label = vie_define_label(frame_country_dep,
                                                    "country_dep", 10, 3,
                                                    self.row,
                                                    True)
        self.country_dep_var = StringVar()
        self.Combobox_country_dep: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.country_dep_var,
            col=3, row=self.row + 1, width=10)

        self.row += 2

        values = getResultsFrom(searchFlight())["country_arr"]

        frame_country_arr: Frame = vie_define_frame(self.filter_frame, 0,
                                                    self.row)
        country_arr_label: Label = vie_define_label(frame_country_arr,
                                                    "country_arr", 10, 0,
                                                    self.row,
                                                    True)
        self.country_dest_var = StringVar()
        self.Combobox_country_arr: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.country_dest_var,
            col=0, row=self.row + 1, width=10)

        values = getResultsFrom(searchFlight())["date_dep"]

        frame_date_dep: Frame = vie_define_frame(self.filter_frame, 1,
                                                 self.row)
        date_dep_label: Label = vie_define_label(frame_date_dep,
                                                 "date_dep", 10, 1, self.row,
                                                 True)
        self.date_dep_var = StringVar()
        self.Combobox_date_dep: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.date_dep_var,
            col=1, row=self.row + 1, width=10)

        values = getResultsFrom(searchFlight())["date_arr"]

        frame_date_arr: Frame = vie_define_frame(self.filter_frame, 2,
                                                 self.row)
        date_arr_label: Label = vie_define_label(frame_date_arr,
                                                 "date_arr", 10, 2, self.row,
                                                 True)
        self.date_arr_var = StringVar()
        self.Combobox_date_arr: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.date_arr_var,
            col=2, row=self.row + 1, width=10)

        values = getResultsFrom(searchFlight())["provider_name"]

        frame_provider: Frame = vie_define_frame(self.filter_frame, 3,
                                                 self.row)
        provider_name_label: Label = vie_define_label(frame_provider,
                                                      "provider_name",
                                                      10, 3, self.row,
                                                      True)
        self.provider_name_var = StringVar()
        self.Combobox_provider_arr: Combobox = vie_define_combobox_2(
            self.filter_frame,
            values,
            self.provider_name_var,
            col=3, row=self.row + 1, width=10)

        self.row += 2

        self.btn_filter: Button = vie_define_button(self.filter_frame,
                                                    self.reload,
                                                    "filter", 1, self.row,
                                                    True,
                                                    width=10)

        self.row += 1

        self.container: Frame = vie_define_frame(self.root, 0, self.row)

        self.btn_greeting: Button = vie_define_button(self.container,
                                                      lambda: print(
                                                          "greeting"),
                                                      "greeting",
                                                      col=0, row=self.row + 1)
        self.btn_greeting.config(padx=10)
        self.btn_profil: Button = vie_define_button(self.container,
                                                    lambda: print(
                                                        "profil"), "profil",
                                                    col=1, row=self.row + 1)

        self.btn_quit: Button = vie_define_button(self.container,
                                                  lambda: self.root.quit(),
                                                  "quit",
                                                  col=2, row=self.row + 1)

    def getGreetingBtn(self):
        return self.btn_greeting

    def getProfilBtn(self):
        return self.btn_profil

    def create_title_Value(self, l_print):
        col = 0

        for i in l_print.keys():
            if i not in ["row", "parent", "Action", "provider_name"]:
                label_title = vie_define_label(l_print["parent"], l_print[i], 8,
                                               col, l_print["row"], False,
                                               bg="white",
                                               fill="black")
                label_title.config(padx=10)
                col += 1

        if l_print["Action"] == 0:
            label_title = vie_define_label(l_print["parent"], "Action", 8, col,
                                           l_print["row"], False, bg="white",
                                           fill="black")
            label_title.config(padx=10)


        elif l_print["Action"] == 1:
            button_Action = vie_define_button(l_print["parent"],
                                              lambda: (self.reload(),
                                                       bookFlight(l_print[
                                                                      "type_seat"],
                                                                  int(l_print[
                                                                          "id_vol"]),
                                                                  l_print[
                                                                      "provider_name"])),
                                              "Take",
                                              col, l_print[
                                                  "row"])

        else:
            label_title = vie_define_label(l_print["parent"], "Complet", 8,
                                           col,
                                           l_print["row"], False, bg="white",
                                           fill="black")
            label_title.config(padx=10)
            col += 1

            if __name__ == "__main__":
                root = Tk()
                root.title("Search view")
                root.config(bg=COLOR_HEX)
                vue_search = Search(root)
                root.mainloop()
