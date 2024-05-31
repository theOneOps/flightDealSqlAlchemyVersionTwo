## @file widgets_functions.py
## This file contains all the functions to create the widgets

"""!
@package view
@file widgets_functions.py
@desc This file contains all the functions to create the widgets
@brief This file contains all the functions to create the widgets
"""

from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

COLOR_HEX: str = "#255369"
FRAMEWIDTH: int = 100
FRAMEHEIGHT: int = 50
FRAMEPAD: int = 5


def vie_define_spinbox(
        frameparent: Frame,
        func,
        from_: int,
        to: int,
        col: int,
        row: int,
        value_var: IntVar,
        wrap_: bool = True,
) -> Spinbox:
    """
    @brief This function create a spinbox
    :param frameparent: the frame where the spinbox will be
    :param func: the function that will be called when the spinbox value change
    :param from_: the minimum value of the spinbox
    :param to: the maximum value of the spinbox
    :param col: the column where the spinbox will be
    :param row: the row where the spinbox will be
    :param value_var: the variable that will be changed when the spinbox value
    change
    :param wrap_: the spinbox will wrap around when the value is out of range
    :return: the spinbox
    """
    spin = Spinbox(
        frameparent,
        from_=from_,
        to=to,
        wrap=wrap_,
        width=5,
        command=func,
        textvariable=value_var,
    )
    spin.grid(column=col, row=row)
    return spin


def vie_define_combobox_2(frameParent: Frame, values: tuple[int], value_var:
StringVar, col: int = 0, row: int = 0, width: int = 5,
                          columnspan: bool = False) -> Combobox:
    spin: ttk.Combobox = ttk.Combobox(frameParent, values=values, width=width,
                                      textvariable=value_var, state='readonly')
    if columnspan:
        spin.grid(column=col, row=row, columnspan=2)
    else:
        spin.grid(column=col, row=row)
    return spin


def vie_define_frame(
        root: Tk | Frame,
        col: int,
        row: int,
        h: int = FRAMEHEIGHT,
        w: int = FRAMEWIDTH,
        pad: int = FRAMEPAD,
        columnspan: bool = False,
) -> Frame:
    """
    @brief This function create a frame
    :param root: root of the frame
    :param col: the column where the frame will be
    :param row: the row where the frame will be
    :param h: the height of the frame
    :param w: the width of the frame
    :param pad: the padding of the frame
    :param columnspan: a boolean to know if the frame will span on 2 columns
    :return: the frame
    """
    frame = Frame(root, height=h, width=w, bg=COLOR_HEX)
    frame.config(padx=pad, pady=pad)

    if columnspan:
        frame.grid(column=col, row=row, columnspan=2)
    else:
        frame.grid(column=col, row=row)
    return frame


def vie_define_lb_frame(
        root: Tk | Frame,
        col: int,
        row: int,
        h: int = FRAMEHEIGHT,
        w: int = FRAMEWIDTH,
        pad: int = FRAMEPAD,
        columnspan: bool = False,
) -> LabelFrame:
    """
    @brief This function create a label frame
    :param root: root of the label frame
    :param col: the column where the label frame will be
    :param row: the row where the label frame will be
    :param h: the height of the label frame
    :param w: the width of the label frame
    :param pad: the padding of the label frame
    :param columnspan: a boolean to know if the label frame will span on 2
    columns
    :return: the label frame
    """
    frame = LabelFrame(root, height=h, width=w, bg=COLOR_HEX)
    frame.config(padx=pad, pady=pad)

    if columnspan:
        frame.grid(column=col, row=row, columnspan=2)
    else:
        frame.grid(column=col, row=row)
    return frame


def vie_define_label(
        parent,
        text: str,
        font_size: int,
        col: int,
        row: int,
        columnspan: bool,
        bg: str = COLOR_HEX,
        fill: str = "white",
) -> Label:
    """
    @brief This function create a label
    :param bg: the background color of the label
    :param parent: the parent of the label
    :param text: the text of the label
    :param font_size: the size of the font of the label
    :param col: the column where the label will be
    :param row: the row where the label will be
    :param columnspan: a boolean to know if the label will span on 2 columns
    :param fill: the color of created text
    :return: the label
    """
    label = Label(
        parent, text=text, font=("Palatino", font_size + 3, "bold"), bg=bg,
        fg=fill
    )
    if columnspan:
        label.grid(column=col, row=row, columnspan=2)
    else:
        label.grid(column=col, row=row)
    return label


def vie_define_radio(
        parent: Frame, function, string: str, variable: IntVar, value: int,
        col: int,
        row: int
) -> Radiobutton:
    """
    @brief This function create a radio button
    :param parent: the parent of the radio button
    :param function: the function that will be called when the radio button is
    clicked
    :param string: the string that will be in the radio button
    :param variable:the variable that will be changed when the radio button is
    clicked
    :param value:the value of the radio button
    :param col:the column where the radio button will be
    :param row: the row where the radio button will be
    :return: the radio button
    """
    radio_btn: Radiobutton = Radiobutton(
        parent,
        text=string,
        variable=variable,
        value=value,
        bg=COLOR_HEX,
        font=("Palatino", 12, "bold"),
        fg="white",
        selectcolor="black",
        command=lambda: function(variable),
    )
    radio_btn.grid(column=col, row=row)
    return radio_btn


def vie_define_button(
        parent,
        function,
        string: str,
        col: int,
        row: int,
        columnspan: bool = False,
        width: int = 5,
        font: str = "Book Antiqua",
        font_size: int = 10,
        color: str = "black",
        anchor: str = "center",
        bg: str = "#f1f1f1",
) -> Button:
    """
    @brief This function create a button
    :param color: the color of the text in the button
    :param font_size: the size of the font of the button
    :param font: the font family of the button
    :param bg: the background color of the button
    :param parent: the parent of the button
    :param function: the function that will be called when the button
    is clicked
    :param string: the string that will be in the button
    :param col: the column where the button will be
    :param row: the row where the button will be
    :param columnspan: a boolean to know if the button will span on 2 columns
    :param width: the width of the current's button
    :param anchor: the anchor to position the text in the button
    :return: the button based on the parameters
    """
    btn: Button = Button(parent, text=string, command=function, width=width,
                         anchor=anchor, justify=CENTER, fg=color)
    btn.config(font=(font, font_size))

    if columnspan:
        btn.grid(column=col, row=row, columnspan=2, pady=20)
    else:
        btn.grid(column=col, row=row, pady=20)
    btn.config(bg=bg)
    return btn


def vie_define_entry(parent: Tk | Frame, width: int = 30, col: int = 0,
                     row: int = 0, columnspan: bool = False) -> Entry:
    entry = Entry(parent, width=width, justify=LEFT)
    if columnspan:
        entry.grid(column=col, row=row, columnspan=2, pady=20)
    else:
        entry.grid(column=col, row=row, pady=20)

    return entry
