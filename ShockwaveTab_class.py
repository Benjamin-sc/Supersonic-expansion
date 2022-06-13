# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:14:58 2022

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

# Import stuff for computations and plotting
import numpy as np
import PIL.Image  
from PIL import ImageTk, Image                                                              # Avoid namespace issues
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ShockwaveTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- frames ----------------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        self.containertab2    = LabelFrame(self,text = "Circular nozzle shockwave", bg="white", fg="red", font='25')            # Create LOAD container

        # Place containers
        self.containertab2.place(relwidth=0.9,relheight=0.9, relx=0.05, rely=0.05)                                          # Place the LOAD container
        
        # Frames in load container
        
        self.frame1tab2 = LabelFrame(self.containertab2,text = "1) Axially symmetric supersonic jet", bg="white", fg="black", font='15')
        self.frame2tab2 = LabelFrame(self.containertab2,text = "2) Conditions", bg="white", fg="black", font='15')
        self.frame3tab2 = LabelFrame(self.containertab2,text = "3) Result", bg="white", fg="black", font='15')
        
        
        # Place Frames in tab 2 container
        self.frame1tab2.place(relwidth=0.5,relheight=0.60, relx=0.02, rely=0.05)
        self.frame2tab2.place(relwidth=0.5,relheight=0.30, relx=0.02, rely=0.65)
        self.frame3tab2.place(relwidth=0.43,relheight=0.9, relx=0.55, rely=0.05)
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- W I D G E T S ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # // == // ============= \\ == \\
        # // == // == L O A D == \\ == \\
        # // == // ============= \\ == \\
            
        # ===== tab 2 frame1 =====
        
        # Load illustrative image
        self.labelImage_ShockWaves= Label(self.frame1tab2)

        self.ShockWaves_image = PIL.Image.open("shock_waves.png")
        
        ShockWaves_image = self.ShockWaves_image.resize((463, 338), Image.ANTIALIAS)
        ShockWaves_image = ImageTk.PhotoImage(ShockWaves_image)
        self.labelImage_ShockWaves.configure(image=ShockWaves_image, justify = CENTER)
        self.labelImage_ShockWaves.image = ShockWaves_image
        
        self.buttonQuestion1= Button(self.frame1tab2, width= 4)
        self.buttonQuestion1.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question1)
        
        # ===== tab 2 frame2 =====
        
        self.spinboxD = Spinbox(self.frame2tab2)
        self.LabelD= Label(self.frame2tab2)
        self.LabelD.configure(text="Nozzle diameter (mm)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        
        self.spinboxP0 = Spinbox(self.frame2tab2)
        self.LabelP0= Label(self.frame2tab2)
        self.LabelP0.configure(text="P0 (mbar)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.spinboxPb = Spinbox(self.frame2tab2)
        self.LabelPb= Label(self.frame2tab2)
        self.LabelPb.configure(text="Pb (mbar)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.buttonX_M = Button(self.frame2tab2)
        self.buttonX_M.configure(text="Compute X_M (cm)):",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.shockwave_compute)
        self.blankX_M = Entry(self.frame2tab2)
        

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # ----------------------------- L A Y O U T ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # TAB2 (frame1)
        
        self.labelImage_ShockWaves.grid(column = 0, row = 0, sticky = "NESW")
        self.buttonQuestion1.grid(column = 1, row = 0, columnspan = 2,sticky = "EW")
        
        # TAB2 (frame2)
        
        self.LabelD.grid(column = 0, row = 0, sticky = "EW")
        self.spinboxD.grid(column = 1, row = 0, sticky = "EW")
        self.LabelP0.grid(column = 0, row = 1, sticky = "EW")
        self.spinboxP0.grid(column = 1, row = 1, sticky = "EW")
        self.LabelPb.grid(column = 0, row = 2, sticky = "EW")
        self.spinboxPb.grid(column = 1, row = 2, sticky = "EW")
        self.buttonX_M.grid(column = 0, row = 3, columnspan = 2,sticky = "EW")
        self.blankX_M.grid(column = 1, row = 4,sticky = "EW")
        
        # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------------- M E T H O D TAB2 ----------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------   
    
    def shockwave_compute(self):
        D = float(self.spinboxD.get())
        P0 = float(self.spinboxP0.get())
        Pb = float(self.spinboxPb.get())
        
        X_M = 0.67/10*D*(P0/Pb)**(1/2)
        
        self.blankX_M.insert(0, X_M)

            
        ratioP1 = np.arange(0, 15, 5)
        X_M1 = 0.67/10*D*(ratioP1)**(1/2)
        ratioP2 = np.arange(15, 17000, 50)
        X_M2 = 0.67/10*D*(ratioP2)**(1/2)
        ratioP3 = np.arange(17000, 20000, 5)
        X_M3 = 0.67/10*D*(ratioP3)**(1/2)

    
        figure = plt.figure(figsize = (5,5), dpi = 90)
        figure.add_subplot(111).plot(ratioP1,X_M1,'r',ratioP2,X_M2,'g',ratioP3,X_M3,'r', P0/Pb, X_M, 'bs')
        plt.xlabel('Pb')
        plt.ylabel('X_M (cm)')
        chart = FigureCanvasTkAgg(figure, self.frame3tab2)
        chart.get_tk_widget().grid(column = 0, row = 0)
    
    # ===== Method: Questions =====
    # ================================
        
        
    def Question1(self):
        messagebox.showinfo ("information :","In the case of an underexpanded jet, the interactions of the molecules in the supersonic expanding gas with the residual molecules in the background gas give rise to two types of shock waves surrounding the gas jet, as illustrated the Figure for the particular case of an axially symmetric jet produced with a circular nozzle. \n" 
                             "The Mach disk is a shock wave perpendicular to the direction of the flow with a nearly flat form which is located at X_M from the exit of the nozzle. \n"
                             "This distance can be approximated for a circular nozzle by the empirical Equation X_M = 0.67 D (P_0/P_b)^(1/2)")
        