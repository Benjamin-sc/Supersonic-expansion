# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:37:05 2022

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
import pandas as pd
from scipy import interpolate
import PIL.Image  
from PIL import ImageTk, Image                                                              # Avoid namespace issues
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2


class SchlierenTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- frames ----------------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        self.container    = LabelFrame(self,text = "Schlieren analysis", bg="white", fg="red", font='25')            # Create LOAD container

        # Place containers
        self.container.place(relwidth=0.9,relheight=0.9, relx=0.05, rely=0.05)                                          # Place the LOAD container
        
        # Frames in load container
        
        self.frame1 = LabelFrame(self.container,text = "1) Schlieren imaging of a supersonic jet", bg="white", fg="black", font='15')
        self.frame2 = LabelFrame(self.container,text = "2) Load video and images", bg="white", fg="black", font='15')
        self.frame3 = LabelFrame(self.container,text = "3) Quantification", bg="white", fg="black", font='15')
        
        
        # Place Frames in tab 2 container
        self.frame1.place(relwidth=0.5,relheight=0.60, relx=0.02, rely=0.05)
        self.frame2.place(relwidth=0.5,relheight=0.30, relx=0.02, rely=0.65)
        self.frame3.place(relwidth=0.43,relheight=0.9, relx=0.55, rely=0.05)
        
        # instance variable
        
        self.checksave = tk.IntVar()
        self.I1                = None                                           # Image 1
        self.IM_thresholded_loop = None    
        self.IM_density       = None                                      
        self.I1_ar             = None                                           # Image 1 in array format
        self.I1_ar_con         = None                                           # Image 1 in array format converted in intensity and µm
        self.Gray_value        = None
        self.Gray_value_interp = None
        self.r                 = None
        self.angle_deg         = None
        self.angle_deg_interp  = None
        self.chkLconstant      = tk.IntVar()                                    # Checkbox for conical nozzle
        self.chkLvariable     = tk.IntVar()                                    # Checkbox for conical nozzle
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # --------------------------- W I D G E T S ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # // == // ============= \\ == \\
        # // == // == L O A D == \\ == \\
        # // == // ============= \\ == \\
            
        # ===== frame1 =====
        
        # Load illustrative image
        self.labelImage_schlieren= Label(self.frame1)

        self.schlieren_image = PIL.Image.open("schlieren.jpg")
        
        schlieren_image = self.schlieren_image.resize((463, 338), Image.ANTIALIAS)
        schlieren_image = ImageTk.PhotoImage(schlieren_image)
        self.labelImage_schlieren.configure(image=schlieren_image, justify = CENTER)
        self.labelImage_schlieren.image = schlieren_image
        
        self.buttonQuestion1= Button(self.frame1, width= 4)
        self.buttonQuestion1.configure(text="?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question1)
        
        # ===== frame 2 =====
        
        self.buttonLoad= Button(self.frame2)
        self.buttonLoad.configure(text="Load and play (gray)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Load_gray)
        self.buttonLoad2= Button(self.frame2)
        self.buttonLoad2.configure(text="Load and play (RGB)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Load_RGB)
        self.buttonbackground= Button(self.frame2)
        self.buttonbackground.configure(text="Background substraction",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.backgound_substraction)
        
        self.spinboxTreshold = Spinbox(self.frame2)
        self.spinboxTreshold.insert(END, 15)
        
        self.spinboxHistory = Spinbox(self.frame2)
        self.spinboxHistory.insert(END, 500)
        
        
        
        self.buttonQuestion2= Button(self.frame2, width= 6)
        self.buttonQuestion2.configure(text="Treshold?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question2)
        
        self.buttonQuestion3= Button(self.frame2, width= 6)
        self.buttonQuestion3.configure(text="History?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question3)
        
        self.checkSave = Checkbutton(self.frame2)
        self.checkSave.configure(text = "save",
                                       variable = self.checksave)
        
        # ===== frame 3 =====
        
        self.buttonLoadQuantification= Button(self.frame3)
        self.buttonLoadQuantification.configure(text="Load and plot initial image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Load_quantification)
        
        self.buttonCalibration= Button(self.frame3)
        self.buttonCalibration.configure(text="Load and plot calibration",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Plot_calibration)
        
        self.spinboxTresholdQuantification = Spinbox(self.frame3)
        self.spinboxTresholdQuantification.insert(END, 2)
        
        self.buttonQuestion4= Button(self.frame3, width= 10)
        self.buttonQuestion4.configure(text="Treshold?",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question4)
        
        self.spinboxLenQualibratonExcel = Spinbox(self.frame3)
        self.spinboxLenQualibratonExcel.insert(END, 176)
        
        self.buttonQuestion5= Button(self.frame3, width= 16)
        self.buttonQuestion5.configure(text="Number data point",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question5)
        
        self.buttonDeflection= Button(self.frame3)
        self.buttonDeflection.configure(text="Compute and plot deflection image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Compute_deflection)
        
        self.labelImage_density= Label(self.frame3)

        self.density_image = PIL.Image.open("Density_formula.png")
        
        density_image = self.density_image.resize((350, 150), Image.ANTIALIAS)
        density_image = ImageTk.PhotoImage(density_image)
        self.labelImage_density.configure(image=density_image, justify = CENTER)
        self.labelImage_density.image = density_image
        
        
        self.spinboxk = Spinbox(self.frame3)
        self.spinboxk.insert(END, 0.000223)
        
        self.buttonQuestion6= Button(self.frame3, width= 10)
        self.buttonQuestion6.configure(text="k constant [m3/kg]",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question6)
        
        self.spinboxf = Spinbox(self.frame3)
        self.spinboxf.insert(END, 5.10)
        
        self.buttonQuestion7= Button(self.frame3, width= 10)
        self.buttonQuestion7.configure(text="Distance between object and cutoff",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question7)
        
        self.spinboxdref = Spinbox(self.frame3)
        self.spinboxdref.insert(END, 1.225)
        
        self.buttonQuestion8= Button(self.frame3, width= 10)
        self.buttonQuestion8.configure(text="Density at reference point [kg/m3]",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question8)
        
        self.buttonQuestion9= Button(self.frame3, width= 10)
        self.buttonQuestion9.configure(text="Pixel resolution [m]",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question9)
        
        self.spinboxpixelresolution = Spinbox(self.frame3)
        self.spinboxpixelresolution.insert(END, 0.000217)
        
        self.checkLconstant = Checkbutton(self.frame3)
        self.checkLconstant.configure(text = "L constant",
                                       variable = self.chkLconstant)
        
        self.checkLvariable = Checkbutton(self.frame3)
        self.checkLvariable.configure(text = "L variable",
                                       variable = self.chkLvariable)
        
        self.spinboxL = Spinbox(self.frame3)
        self.spinboxL.insert(END, 0.01)
        
        self.buttonDensity= Button(self.frame3)
        self.buttonDensity.configure(text="Compute and plot density image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Compute_density)
        
        
        
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        # ----------------------------- L A Y O U T ---------------------------
        # ---------------------------------------------------------------------
        # ---------------------------------------------------------------------
        
        # (frame1)
        
        self.labelImage_schlieren.grid(column = 0, row = 0, sticky = "NESW")
        self.buttonQuestion1.grid(column = 1, row = 0, columnspan = 2,sticky = "EW")
        
        # (frame2)
        
        
        self.buttonLoad.grid(column = 0, row = 0, columnspan = 2,sticky = "EW")
        self.buttonLoad2.grid(column = 0, row = 1, columnspan = 2,sticky = "EW")
        self.buttonbackground.grid(column = 0, row = 2, columnspan = 2,sticky = "EW")
        
        self.spinboxTreshold.grid(column = 2, row = 2, columnspan = 2,sticky = "EW")
        self.spinboxHistory.grid(column = 2, row = 3, columnspan = 2,sticky = "EW")
        self.buttonQuestion2.grid(column = 3, row = 2,sticky = "EW")
        self.buttonQuestion3.grid(column = 3, row = 3,sticky = "EW")
        self.checkSave.grid(column = 4, row = 2, rowspan = 2,sticky = "NESW")
        
        # (frame3)
        
        self.buttonLoadQuantification.grid(column = 0, row = 0,sticky = "EW")
        self.buttonCalibration.grid(column = 0, row = 1,sticky = "EW")
        self.spinboxTresholdQuantification.grid(column = 1, row = 2,sticky = "EW")
        self.buttonQuestion4.grid(column = 2, row = 2,sticky = "EW")
        self.spinboxLenQualibratonExcel.grid(column = 1, row = 1,sticky = "EW")
        self.buttonQuestion5.grid(column = 2, row = 1,sticky = "EW")
        self.buttonDeflection.grid(column = 0, row = 2,sticky = "EW")
        self.labelImage_density.grid(column = 0, row = 3,columnspan = 3, sticky = "NESW")
        self.buttonQuestion6.grid(column = 0, row = 4,sticky = "EW")
        self.spinboxk.grid(column = 1, row = 4,sticky = "EW")
        self.buttonQuestion7.grid(column = 0, row = 5,sticky = "EW")
        self.spinboxf.grid(column = 1, row = 5,sticky = "EW")
        self.buttonQuestion8.grid(column = 0, row = 6,sticky = "EW")
        self.spinboxdref.grid(column = 1, row = 6,sticky = "EW")
        self.buttonQuestion9.grid(column = 0, row = 7,sticky = "EW")
        self.spinboxpixelresolution.grid(column = 1, row = 7,sticky = "EW")
        self.checkLconstant.grid(column = 0, row = 8,sticky = "EW")
        self.checkLvariable.grid(column = 0, row = 9,sticky = "EW")
        self.spinboxL.grid(column = 1, row = 8,rowspan =2, sticky = "EW")
        self.buttonDensity.grid(column = 0, row = 10,sticky = "EW")
        
        
        
        
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------------- M E T H O D  --------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------  
        
        
    def Load_gray(self):

        print('hello')
        cap = cv2.VideoCapture('video_test.avi')
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Gray video', gray)
            
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
        
        
    def Load_RGB(self):

        print('hello')
        cap = cv2.VideoCapture('video_test.avi')
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            cv2.imshow('RGB video', frame)
            
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
        
        
    def Load_quantification(self):


        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/Article à publier/Article Champagne",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.jpg;*.png;*.bmp"),
                                                    ("JPG Files", "*.jpg"),
                                                    ("PNG Files", "*.png"),
                                                    ("BMP Files", "*.bmp")))
#        file_path = filedialog.askopenfilename(initialdir = "C:/Users/Josh/Documents/YouTube_Files/DIY_BOS/",
#                                               title = "Select Image 1",
#                                               filetypes = (("All Files", "*.jpg;*.png;*.tif;*.tiff;*.bmp"),
#                                                            ("JPG Files", "*.jpg"),
#                                                            ("PNG Files", "*.png"),
#                                                            ("TIF Files", "*.tif;*.tiff"),
#                                                            ("BMP Files", "*.bmp")))
        
        
        self.I1 = PIL.Image.open(file_path)                                     # Open the image
        self.I1Orig = self.I1                                                   # Save original image for plotting
        self.I1_ar = (np.array(self.I1))                            # Convert image to array
        plt.imshow(self.I1_ar)
        plt.colorbar()
        
        
    def backgound_substraction(self):
        
        treshold = int(self.spinboxTreshold.get())
        history = int(self.spinboxHistory.get())
        
        cap = cv2.VideoCapture('video_test.avi')
        fgbg = cv2.createBackgroundSubtractorMOG2(history = history, varThreshold = treshold,detectShadows=False)
        
        if self.checksave.get()==1:
            ret, frame = cap.read()
            size = frame[0].shape[1], frame[0].shape[0]
            out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (size))

        while True:
    
            ret, frame = cap.read()
    
            if frame is None:
                break
    
            fgmask = fgbg.apply(frame)
            cv2.imshow('frame',fgmask)
            if self.checksave.get()==1:
                out.write(fgmask)

    
            keyboard = cv2.waitKey(30)                                          # we use the waitKey() after imshow() function to pause each frame in the video
            if keyboard =='q':
                break
    
        cap.release()
        if self.checksave.get()==1:
            out.release()
        cv2.destroyAllWindows()
        
    def Plot_calibration(self):
        
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/Article à publier/Article Champagne",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.xlsx"),
                                                    ("XLSX Files", "*.xlsx")))


        df = pd.read_excel(file_path)  
        arr = df.to_numpy()

              
        Data_len = int(self.spinboxLenQualibratonExcel.get())

        self.Gray_value, self.r, self.angle_deg = arr[1:Data_len, 2], arr[1:Data_len, 3], arr[1:Data_len, 5]
        x = np.arange(0, len(self.Gray_value),1)
        
        #interpolation of calibration curve
        
        f = interpolate.interp1d(x, self.Gray_value)
        xnew = np.arange(0, len(self.Gray_value)-1,0.5)
        self.Gray_value_interp = f(xnew)   # use interpolation function returned by `interp1d`


        z = interpolate.interp1d(x, self.angle_deg)
        xnew = np.arange(0, len(self.angle_deg)-1,0.5)
        self.angle_deg_interp = z(xnew)   # use interpolation function returned by `interp1d`
        
        
        
                                            
        # plotting the calibration line
        plt.plot(x, self.Gray_value, 'o', xnew, self.Gray_value_interp, '-')
      
        # putting labels
        plt.xlabel('Distance (pixels)', fontsize=14)
        plt.ylabel('Intensity', fontsize=14)
      
        # function to show plot
        
        plt.show()
        
        
    def Compute_deflection(self):
        
        if self.I1_ar is None:
            messagebox.showinfo ("warning","Before, you need to load the initial image")
        elif self.r is None:
            messagebox.showinfo ("warning","Before, you need to load the Calibration data")
        elif self.Gray_value is None:
            messagebox.showinfo ("warning","Before, you need to load the Calibration data")
        else:
            print('hello')
            treshold = int(self.spinboxTresholdQuantification.get())
            
            
            self.IM_thresholded_loop = np.zeros((len(self.I1_ar[:,1]),len(self.I1_ar[1]))); #allocate space for thresholded image

            for i in np.arange(0,len(self.I1_ar[:,1])):                                             #loop over all rows and columns
                for j in np.arange(0,len(self.I1_ar[1])):

                    pixel=self.I1_ar[i,j]                                        #get pixel value

                    for k in np.arange(0,len(self.Gray_value_interp)):                            # check pixel value and assign new value
                        if abs(pixel-self.Gray_value_interp[k])<=treshold:
                            new_pixel=self.angle_deg_interp[k]
                            
                            break
                        else: 
                            new_pixel = 0

                    print(new_pixel)
                    self.IM_thresholded_loop[i,j] =new_pixel               # save new pixel value in thresholded image
                    
            plt.imshow(self.IM_thresholded_loop, cmap='RdBu')
            plt.colorbar()
            
    def Compute_density(self):
        
        f = float(self.spinboxf.get())
        dref = float(self.spinboxdref.get())
        k = float(self.spinboxk.get())
        pixel_resolution = float(self.spinboxpixelresolution.get())
        
        
        
        if self.chkLconstant.get() and self.chkLvariable.get():
            messagebox.showinfo ("warning","L cannot be constant and variable. Select an option")
        elif self.chkLconstant.get()==0 and self.chkLvariable.get()==0:
            messagebox.showinfo ("warning","Please inform if L is considered constant or not")
        elif self.chkLconstant.get()==0 and self.chkLvariable.get():
            L = 0
            print('L variable')
        elif self.chkLconstant.get() and self.chkLvariable.get()==0:
            L = float(self.spinboxL.get())
            print(L)
            
            self.IM_density = np.zeros((len(self.IM_thresholded_loop[:,1]),len(self.IM_thresholded_loop[1]))); #allocate space for thresholded image

            for i in np.arange(0,len(self.IM_thresholded_loop[:,1])):                                             #loop over all rows and columns
                for j in np.arange(0,len(self.IM_thresholded_loop[1])):

                    self.IM_density[i,j]=self.IM_thresholded_loop[i,j]*pixel_resolution/(k*L) + dref                                        #get pixel value

                    
            plt.imshow(self.IM_density, cmap='RdBu')
            plt.colorbar()
        
    # ===== Method: Questions =====
    # ================================
        
        
    def Question1(self):
        messagebox.showinfo ("information :","")
        
    def Question2(self):
        messagebox.showinfo ("information :","")
        
    def Question3(self):
        messagebox.showinfo ("information :","how many previous frames are used for building the background model. So basically if an item is standing at a fixed position for as many frames as the history size, then it will disappear in the background.")
    
    def Question4(self):
        messagebox.showinfo ("information :","This threshold value is used in the loop that replace the pixel gray value by an deflection value from the calibration curve. If the pixel intensity difference between the image and any pixel intensity from the clibration curve is smaller than this treshold value, the pixel from the image is replace by the deflection value ")
        
    def Question5(self):
        messagebox.showinfo ("information :","Indicates the number of data point of you calibration curve")
        
    def Question6(self):
        messagebox.showinfo ("information :","Constant from Gladstone-Dale law that make the link between the refractive index and the density")
        
    def Question7(self):
        messagebox.showinfo ("information :","Schlieren system distance between the studied object and the cutoff")
    
    def Question8(self):
            messagebox.showinfo ("information :","Flow density at a reference point (e.g. surrounding air)")
            
    def Question9(self):
            messagebox.showinfo ("information :","Distance in m between two pixels")