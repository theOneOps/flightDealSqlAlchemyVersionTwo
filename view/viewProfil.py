from typing import Union, TypedDict

from view.widgets_functions import *


class myDict(TypedDict):
    parent: Union[
        Widget, None]
    id_vol: str
    country_dep: str
    country_arr: str
    price: str
    type_seat: str
    Action: bool
    row: int


class Profil:

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

            if not (l_print["Action"]):
                label_title: Label = vie_define_label(l_print["parent"],
                                                      "Action",
                                                      8,
                                                      col,
                                                      l_print["row"],
                                                      False)
                label_title.config(padx=10)
                col += 1

            if l_print["Action"]:
                button_Action: Button = vie_define_button(l_print["parent"],
                                                          lambda: print(
                                                              "cancel"),
                                                          "Cancel",
                                                          col, l_print["row"]
                                                          )

        row: int = 0
        create_title_Value({
            "parent": self.title_frame,
            "id_vol": "id_vol",
            "country_dep": "country_dep",
            "country_arr": "country_arr",
            "type_seat": "type_seat",
            "price": "price",
            "Action": False,
            "row": row,
        })
        row += 1

        create_title_Value({"parent": self.title_frame,
                            "id_vol": 1,
                            "country_dep": "france",
                            "country_arr": "canada",
                            "type_seat": "eco",
                            "price": 123000.,
                            "Action": True,
                            "row": 1}
                           )
        row += 1

        self.filter_frame: LabelFrame = vie_define_lb_frame(root, 0, row,
                                                            columnspan=True)

        values = ("premium", "eco")

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
                                                    "country_arr", 10, 1, row,
                                                    True)

        self.spinbox_country_arr: Spinbox = vie_define_combobox_2(
            self.filter_frame,
            values=values,
            col=1, row=row + 1, width=10)

        values = (1, 2)

        row += 2

        self.btn_submit: Button = vie_define_button(self.filter_frame, lambda:
        print("filter"), "filter", 0, row, True, width=10)

        row += 1

        self.container: Frame = vie_define_frame(root, 0, row)

        self.btn_greeting: Button = vie_define_button(self.container,
                                                    lambda: print(
                                                        "greeting"), "greeting",
                                                    col=0, row=row + 1)
        self.btn_greeting.config(padx=10)

        self.btn_search: Button = vie_define_button(self.container,
                                                    lambda: print(
                                                        "search"), "search",
                                                    col=1, row=row + 1)

        self.btn_quit: Button = vie_define_button(self.container,
                                                  lambda: root.quit(), "quit",
                                                  col=2, row=row + 1)


# if __name__ == "__main__":
    # root = Tk()
    # root.title("Profil view")
    # root.config(bg=COLOR_HEX)
    # vue_search = Profil(root)
    # root.mainloop()