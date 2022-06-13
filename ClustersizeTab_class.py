# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:48:29 2022

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


class ClustersizeTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- frames ----------------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------


        self.containerLoad    = LabelFrame(self,text = "Average cluster size formed by gas expansion", bg="white", fg="red", font='25')            # Create LOAD container

        # Place containers
        self.containerLoad.place(relwidth=0.9,relheight=0.9, relx=0.05, rely=0.05)                                          # Place the LOAD container
        
        # Frames in load container
        
        self.frame1 = LabelFrame(self.containerLoad,text = "1) Equivalent critical-section diameter (d_eq)", bg="white", fg="black", font='15')
        self.frame2 = LabelFrame(self.containerLoad,text = "2) Gas properties", bg="white", fg="black", font='15')
        self.frame3 = LabelFrame(self.containerLoad,text = "3) Hagena parameter ", bg="white", fg="black", font='15')
        self.frame4 = LabelFrame(self.containerLoad,text = "4) Result ", bg="white", fg="black", font='15')
        
        # Place Frames in load container
        self.frame1.place(relwidth=0.5,relheight=0.3, relx=0.02, rely=0.05)
        self.frame2.place(relwidth=0.24,relheight=0.55, relx=0.02, rely=0.4)
        self.frame3.place(relwidth=0.25,relheight=0.55, relx=0.27, rely=0.4)
        self.frame4.place(relwidth=0.43,relheight=0.90, relx=0.55, rely=0.05)
        
        # Place subFrames in frame1
        self.subframe1 = LabelFrame(self.frame1,text = "", bg="white", fg="black", font='15')
        self.subframe1.place(relwidth=0.35,relheight=0.8, relx=0.6, rely=0.05)
        # Place subFrames in frame3
        self.subframe3 = LabelFrame(self.frame3,text = "", bg="white", fg="black", font='15')
        self.subframe3.place(relwidth=0.95,relheight=0.3, relx=0.02, rely=0.65)
        
        
        # Instance variables
        self.deq                = None                                           # equivalent diameter
        self.a                  = None
        self.b                  = None
        self.chksonic           = tk.IntVar()                                    # Checkbox for sonic nozzle
        self.chkconical         = tk.IntVar()                                    # Checkbox for conical nozzle
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- W I D G E T S ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # // == // ============= \\ == \\
        # // == // == L O A D == \\ == \\
        # // == // ============= \\ == \\
        
        # ===== tab 1 frame1 =====
        self.checksonic = Checkbutton(self.frame1)
        self.checksonic.configure(text = "Sonic nozzle",
                                       variable = self.chksonic)
        self.checkconical = Checkbutton(self.frame1)
        self.checkconical.configure(text = "Conical nozzle",
                                       variable = self.chkconical)
        self.spinboxDiameter = Spinbox(self.frame1)
        self.LabelDiameter= Label(self.frame1)
        self.LabelDiameter.configure(text="Nozzle critical-section diameter (µm)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        
        self.spinboxAngle = Spinbox(self.frame1)
        self.LabelAngle= Label(self.frame1)
        self.LabelAngle.configure(text="half cone angle (°)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.buttondeq = Button(self.frame1)
        self.buttondeq.configure(text="Compute d_eq",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.deq_compute)
        # Load illustrative image
        self.labelImage= Label(self.subframe1)

        self.Angle_image = PIL.Image.open("equivalent_diameter.png")
        
        Angle_image = self.Angle_image.resize((197, 120), Image.ANTIALIAS)
        Angle_image = ImageTk.PhotoImage(Angle_image)
        self.labelImage.configure(image=Angle_image, justify = CENTER)
        self.labelImage.image = Angle_image
        
        # ===== tab 1 frame2 =====
        # ===== The tree for molecule library =====
        self.tree = ttk.Treeview(self.frame2)
        # Define columns of the tree
        self.tree['columns'] = ("a", "b")
        # Formate my colums
        self.tree.column("#0", width=120, minwidth=25)
        self.tree.column("a", anchor=CENTER, width=65)
        self.tree.column("b", anchor=CENTER, width=65)

        #create Headings
        self.tree.heading("#0", text= "Molecules library", anchor= W)
        self.tree.heading("a", text= "Mass", anchor= CENTER)
        self.tree.heading("b", text= "K constant", anchor= CENTER)

        # add data in the tree
        self.tree.insert(parent='', index='end', iid=0, text="Rare gases", values=("", "","", ""))
        self.tree.insert(parent='', index='end', iid=1, text="Other", values=("", "","", ""))

        #add child
        self.tree.insert(parent='', index='end', iid=3, text="Xe", values=(131, 5500))
        self.tree.move('3', '0', '0')
        self.tree.insert(parent='', index='end', iid=4, text="Ar", values=(40, 1646))
        self.tree.move('4', '0', '0')
        self.tree.insert(parent='', index='end', iid=5, text="Ne", values=(20, 185 ))
        self.tree.move('5', '0', '0')
        self.tree.insert(parent='', index='end', iid=6, text="He", values=(4, 3.85 ))
        self.tree.move('6', '0', '0')
        self.tree.insert(parent='', index='end', iid=7, text="N2", values=(28, 528))
        self.tree.move('7', '1', '0')
        # handle the selection of the item in the tree
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        
        # ===== tab 1 frame3 =====
        self.labelSpace1= Label(self.frame3,text="",bg = "white", fg="white")
        self.labelSpace2= Label(self.frame3,text="",bg = "white", fg="white")
        self.spinboxTemperature = Spinbox(self.frame3)
        self.LabelTemperature= Label(self.frame3)
        self.LabelTemperature.configure(text="Stagnation temperature (K)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        
        self.spinboxPressure = Spinbox(self.frame3)
        self.LabelPressure= Label(self.frame3)
        self.LabelPressure.configure(text="Stagnation pressure (mbar)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",)
        self.buttonHagena = Button(self.frame3)
        self.buttonHagena.configure(text="Compute Hagena parameter:",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.hagena_compute)
        self.blankHagena = Entry(self.frame3)
        self.buttonClustersize = Button(self.frame3)
        self.buttonClustersize.configure(text="Compute Average cluster size",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.clustersize_compute)
        self.blankClustersize = Entry(self.frame3)
        
        

        # Load equation image
        self.labelImage2= Label(self.subframe3)

        self.Equations_image = PIL.Image.open("Hagena equations.png")
        
        Equations_image = self.Equations_image.resize((260, 85), Image.ANTIALIAS)
        Equations_image = ImageTk.PhotoImage(Equations_image)
        self.labelImage2.configure(image=Equations_image, justify = CENTER)
        self.labelImage2.image = Equations_image
        
        
         # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # ----------------------------- L A Y O U T ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # TAB1 (frame1)
        self.checksonic.grid(column = 0, row = 0, sticky = "EW")
        self.checkconical.grid(column = 0, row = 1, sticky = "EW")
        self.LabelDiameter.grid(column = 0, row = 2, sticky = "EW")
        self.spinboxDiameter.grid(column = 1, row = 2, sticky = "EW")
        self.LabelAngle.grid(column = 0, row = 3, sticky = "EW")
        self.spinboxAngle.grid(column = 1, row = 3, sticky = "EW")
        self.buttondeq.grid(column = 0, row = 4, columnspan = 2,sticky = "EW")
        self.labelImage.grid(column = 2, row = 0,rowspan = 3, sticky = "NESW")
        # TAB1 (frame2)
        self.tree.grid(column = 0, row = 14, columnspan = 3, sticky = "EW")
        # TAB1 (frame3)
        self.LabelTemperature.grid(column = 0, row = 0, sticky = "EW")
        self.spinboxTemperature.grid(column = 1, row = 0, sticky = "EW")
        self.LabelPressure.grid(column = 0, row = 1, sticky = "EW")
        self.spinboxPressure.grid(column = 1, row = 1, sticky = "EW")
        self.labelSpace1.grid(column = 0, row = 2, sticky = "EW")
        self.buttonHagena.grid(column = 0, row = 3, columnspan = 2,sticky = "EW")
        self.blankHagena.grid(column = 1, row = 4,sticky = "EW")
        self.labelSpace2.grid(column = 0, row = 5, sticky = "EW")
        self.buttonClustersize.grid(column = 0, row = 6, columnspan = 2,sticky = "EW")
        self.blankClustersize.grid(column = 1, row = 7,sticky = "EW")
        self.labelImage2.grid(column = 0, row = 0, sticky = "NESW")
        
        # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------------- M E T H O D TAB1 ----------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    
    
    # ===== Method: molecule selection in the tree =====
    # ==================================================
    
    def item_selected(self,event):

        item = self.tree.selection()[0]
        self.a = float(self.tree.item(item)['values'][0])
        self.b = float(self.tree.item(item)['values'][1])

    

    # ===== Method: deq compute =====
    # ================================

    def deq_compute(self):
        
        if (self.chksonic.get()) and self.chkconical.get()==0:
            self.deq = float(self.spinboxDiameter.get())
            print(self.deq)
        elif self.chksonic.get()==0 and self.chkconical.get():
            alpha = float(self.spinboxAngle.get())
            d = float(self.spinboxDiameter.get())
            self.deq = 0.74*d/np.tan(alpha*np.pi/180)
            print(self.deq)
        elif self.chksonic.get() and self.chkconical.get():
            messagebox.showinfo ("warning","Please select only one nozzle type")
        
    # ===== Method: Hagena compute =====
    # ================================

    def hagena_compute(self):
        try:
            T = float(self.spinboxTemperature.get())
            P = float(self.spinboxPressure.get())
        except: 
            messagebox.showinfo ("warning","Enter temperature and pressure conditions")
        
        try:
            K = float(self.b)
        except: 
            messagebox.showinfo ("warning","Select the injected gas")

 
        Hagena = K*P*(self.deq)**0.85/T**2.28
        self.blankHagena.insert(0, Hagena)
        
    # ===== Method: cluster size compute =====
    # ================================

    def clustersize_compute(self):
        T = float(self.spinboxTemperature.get())
        P = float(self.spinboxPressure.get())
        K = self.b
        Hagena = K*P*(self.deq)**0.85/T**2.28
        
        
        
        if 0 < Hagena < 1000:
            
            t1 = np.arange(0, 350, 50)
            y1 = 38.4*(t1/1000)**1.64
            t2 = np.arange(350, 1800, 50)
            y2 = 38.4*(t2/1000)**1.64
            t3 = np.arange(1800, 2000, 100)
            y3 = 38.4*(t3/1000)**1.64
            clustersize = 38.4*(Hagena/1000)**1.64
            self.blankClustersize.insert(0, clustersize)
            
        elif 1000 < Hagena < 7300:
            t1 = np.arange(0, 1000, 100)
            y1 = 33*(t1/1000)**2.35
            t2 = np.arange(1000, 7300, 100)
            y2 = 33*(t2/1000)**2.35
            t3 = np.arange(7300, 10000, 100)
            y3 = 33*(t3/1000)**2.35
            clustersize = 33*(Hagena/1000)**2.35
            self.blankClustersize.insert(0, clustersize)
        
        elif 7300 < Hagena:
            
            t1 = np.arange(0, 2100, 100)
            y1 = 78*(t1/1000)**1.84
            t2 = np.arange(2100, 14000, 100)
            y2 = 78*(t2/1000)**1.84
            t3 = np.arange(14000, 16000, 100)
            y3 = 78*(t3/1000)**1.84
            clustersize = 78*(Hagena/1000)**1.84
            self.blankClustersize.insert(0, clustersize)
            

        
        figure = plt.figure(figsize = (5,5), dpi = 90)
        figure.add_subplot(111).plot(t1,y1,'r',t2,y2,'g',t3,y3,'r', Hagena, clustersize, 'bs')
        plt.xlabel('Hagena parameter')
        plt.ylabel('<N>')
        chart = FigureCanvasTkAgg(figure, self.frame4)
        chart.get_tk_widget().grid(column = 0, row = 0)
        