from typing import Union, TypedDict

import model.utils
from widgets_functions import *


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


class Search:

    def __init__(self, root: Tk):
        self.title_frame = vie_define_lb_frame(root, 0, 0)

        def create_title_Value(l_print: myDict) -> None:
            col: int = 0

            for i in l_print.keys():
                if i not in ["row", "parent", "Action"]:
                    label_title: Label = vie_define_label(l_print["parent"],
                                                          l_print[i],
                                                          8,
                                                          col,
                                                          l_print["row"],
                                                          False)
                    label_title.config(padx=10)
                    col += 1

            if (l_print["Action"] == 0):
                label_title: Label = vie_define_label(l_print["parent"],
                                                      "Action",
                                                      8,
                                                      col,
                                                      l_print["row"],
                                                      False)
                label_title.config(padx=10)
                col += 1

            elif l_print["Action"] == 1:
                button_Action: Button = vie_define_button(l_print["parent"],
                                                          lambda: print(
                                                              "hello"), "Take",
                                                          col, l_print["row"]
                                                          )
            else:
                label_title: Label = vie_define_label(l_print["parent"],
                                                      "Complet",
                                                      8,
                                                      col,
                                                      l_print["row"],
                                                      False)
                label_title.config(padx=10)
                col += 1

        row: int = 0
        create_title_Value({
            "parent": self.title_frame,
            "id_vol": "id_vol",
            "country_dep": "country_dep",
            "country_arr": "country_arr",
            "date_dep": "date_dep",
            "date_arr": "date_arr",
            "type_seat": "type_seat",
            "price": "price",
            "Action": 0,
            "row": row,
            "provider_name": "provider_name"
        })
        row += 1

        create_title_Value({"parent": self.title_frame,
                            "id_vol": 1,
                            "country_dep": "france",
                            "country_arr": "canada",
                            "date_dep": "2020-07-21",
                            "date_arr": "2020-07-21",
                            "type_seat": "Economy",
                            "price": 123000.,
                            "Action": 1,
                            "row": row,
                            "provider_name": "Air France"}
                           )
        row += 1

        self.filter_frame: LabelFrame = vie_define_lb_frame(root, 0, row,
                                                            columnspan=True)

        values = model.utils.classes_names

        frame_type_seat: Frame = vie_define_frame(self.filter_frame, 0,
                                                  row)
        type_seat_label: Label = vie_define_label(frame_type_seat,
                                                  "type_seat", 10, 0, row,
                                                  True)

        self.spinbox_type_seat: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=0, row=row + 1, width=10)

        values = (100, 245, 3124, 4242)

        frame_price: Frame = vie_define_frame(self.filter_frame, 1,
                                              row)
        price_label: Label = vie_define_label(frame_price,
                                              "price", 10, 1, row,
                                              True)

        self.spinbox_price: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=1, row=row + 1, width=10)

        values = (1, 2, 3, 4)

        frame_capacity: Frame = vie_define_frame(self.filter_frame, 2,
                                                 row)
        capacity_label: Label = vie_define_label(frame_capacity,
                                                 "capacity", 10, 2, row,
                                                 True)

        self.spinbox_capacity: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=2, row=row + 1, width=10)

        row += 2

        values = ("france", "paris", "canada", "ottawa")

        frame_country_dep: Frame = vie_define_frame(self.filter_frame, 0,
                                                    row)
        country_dep_label: Label = vie_define_label(frame_country_dep,
                                                    "country_dep", 10, 0, row,
                                                    True)

        self.spinbox_country_dep: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=0, row=row + 1, width=10)

        values = ("togo", "lome", "washington", "ottawa")

        frame_country_arr: Frame = vie_define_frame(self.filter_frame, 1,
                                                    row)
        country_arr_label: Label = vie_define_label(frame_country_arr,
                                                    "country_dep", 10, 1, row,
                                                    True)

        self.spinbox_country_arr: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=1, row=row + 1, width=10)

        values = (1, 2)

        frame_remain_ticket: Frame = vie_define_frame(self.filter_frame, 2,
                                                      row)
        remain_ticket_label: Label = vie_define_label(frame_remain_ticket,
                                                      "country_dep", 10, 2, row,
                                                      True)

        self.spinbox_remain_tickets: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=2, row=row + 1, width=10)

        row += 2

        self.btn_submit: Button = vie_define_button(self.filter_frame, lambda:
        print("filter"), "filter", 1, row, False, width=10)

        row += 1

        self.container: Frame = vie_define_frame(root, 0, row)

        self.btn_greeting: Button = vie_define_button(self.container,
                                                      lambda: print(
                                                          "greeting"), "greeting",
                                                      col=0, row=row + 1)
        self.btn_greeting.config(padx=10)
        self.btn_profil: Button = vie_define_button(self.container,
                                                    lambda: print(
                                                        "profil"), "profil",
                                                    col=1, row=row + 1)

        self.btn_quit: Button = vie_define_button(self.container,
                                                  lambda: root.quit(), "quit",
                                                  col=2, row=row + 1)


if __name__ == "__main__":
    root = Tk()
    root.title("Search view")
    root.config(bg=COLOR_HEX)
    vue_search = Search(root)
    root.mainloop()
