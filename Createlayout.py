# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:48:53 2022

@author: tomasetti
"""

# Import some tkinter things for GUI stuff
import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import Button, Entry, Label, Checkbutton, Scale, Spinbox, LabelFrame
from tkinter import Frame, CENTER, END, LEFT, W
from tkinter import filedialog
from tkinter import messagebox




from ClustersizeTab_class import *
from ShockwaveTab_class import *
from SchlierenTab_class import *


class CreateLayout:
    def __init__(self, window):
        self.window = window

        tab_control = ttk.Notebook(window)

        clustersize_tab = ClustersizeTab(tab_control)
        shockwave_tab = ShockwaveTab(tab_control)
        schlieren_tab = SchlierenTab(tab_control)

        tab_control.add(clustersize_tab, text="Average cluster size determination")
        tab_control.add(shockwave_tab, text="Circular nozzle shock waves")
        tab_control.add(schlieren_tab, text="Schlieren analysis")
        
        tab_control.pack(expand=1, fill="both")



root = Tk()
root.wm_title("Supersonic expansion")                                        # Set window title
#root.iconbitmap("icon.ico")                                                     # Set icon bitmap
root.geometry("1300x800")
#root.configure(bg="#263D42")
createLayout = CreateLayout(root)                                                   # Instantiate the class GUI_BOS
root.mainloop()