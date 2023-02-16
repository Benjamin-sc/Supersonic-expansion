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
import time


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
        
        self.I1                = None                                           # Image 1
        self.cap                = None                                           # Image 1
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
        self.buttonbackground.configure(text="Background substraction (saved as output_BGS.avi)",
                                        bg = "green",
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
        
        self.buttonTimer= Button(self.frame2)
        self.buttonTimer.configure(text="Add timer (saved as output_Timer.avi)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.add_timer)
        
        self.spinboxFrameSec = Spinbox(self.frame2)
        self.spinboxFrameSec.insert(END, 20000)
        
        self.spinboxOutFrameSec = Spinbox(self.frame2)
        self.spinboxOutFrameSec.insert(END, 10)
        
        
        
        self.buttonQuestion10= Button(self.frame2, width= 6)
        self.buttonQuestion10.configure(text="Real Frames/s",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question10)
        
        self.buttonQuestion11= Button(self.frame2, width= 6)
        self.buttonQuestion11.configure(text="Out Frames/sec",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question11)
        
        # ===== frame 3 =====
        
        self.buttonLoadQuantification= Button(self.frame3)
        self.buttonLoadQuantification.configure(text="Load and plot initial image",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Load_quantification)
        
        self.buttonCalibration= Button(self.frame3)
        self.buttonCalibration.configure(text="Load and plot calibration (excel)",
                                        bg = "Steel Blue",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Plot_calibration)
        
        
        self.spinboxGrayValueColumnExcel = Spinbox(self.frame3)
        self.spinboxGrayValueColumnExcel.insert(END, 1)
        self.spinboxrColumnExcel = Spinbox(self.frame3)
        self.spinboxrColumnExcel.insert(END, 2)
        self.spinboxAngleColumnExcel = Spinbox(self.frame3)
        self.spinboxAngleColumnExcel.insert(END, 4)
        self.spinboxLenQualibratonExcel = Spinbox(self.frame3)
        self.spinboxLenQualibratonExcel.insert(END, 176)
        
        self.buttonQuestion4a= Button(self.frame3, width= 20)
        self.buttonQuestion4a.configure(text="Gray values column",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question4a)
        
        self.buttonQuestion4b= Button(self.frame3, width= 20)
        self.buttonQuestion4b.configure(text="r values column",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question4b)
        
        self.buttonQuestion4c= Button(self.frame3, width= 20)
        self.buttonQuestion4c.configure(text="Angle column",
                                        bg = "grey",
                                        fg = "White",
                                        activeforeground = "White",
                                        activebackground = "Black",
                                        command = self.Question4c)
        
        self.buttonQuestion5= Button(self.frame3, width= 20)
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
        self.buttonbackground.grid(column = 0, row = 2, columnspan = 2,rowspan = 2,sticky = "NESW")
        self.buttonTimer.grid(column = 0, row = 4, columnspan = 2,rowspan = 2,sticky = "NESW")
        
        self.spinboxTreshold.grid(column = 2, row = 2, columnspan = 2,sticky = "EW")
        self.spinboxHistory.grid(column = 2, row = 3, columnspan = 2,sticky = "EW")
        self.buttonQuestion2.grid(column = 3, row = 2,sticky = "EW")
        self.buttonQuestion3.grid(column = 3, row = 3,sticky = "EW")
        
        self.spinboxFrameSec.grid(column = 2, row = 4, columnspan = 2,sticky = "EW")
        self.spinboxOutFrameSec.grid(column = 2, row = 5, columnspan = 2,sticky = "EW")
        self.buttonQuestion10.grid(column = 3, row = 4,sticky = "EW")
        self.buttonQuestion11.grid(column = 3, row = 5,sticky = "EW")
        
        # (frame3)
        
        self.buttonLoadQuantification.grid(column = 0, row = 0,sticky = "EW")
        self.buttonCalibration.grid(column = 0, row = 1,sticky = "EW")

        
        self.spinboxGrayValueColumnExcel.grid(column = 1, row = 1,sticky = "EW")
        self.spinboxrColumnExcel.grid(column = 1, row = 2,sticky = "EW")
        self.spinboxAngleColumnExcel.grid(column = 1, row = 3,sticky = "EW")
        self.spinboxLenQualibratonExcel.grid(column = 1, row = 4,sticky = "EW")
        
        self.buttonQuestion4a.grid(column = 2, row = 1,sticky = "EW")
        self.buttonQuestion4b.grid(column = 2, row = 2,sticky = "EW")
        self.buttonQuestion4c.grid(column = 2, row = 3,sticky = "EW")
        self.buttonQuestion5.grid(column = 2, row = 4,sticky = "EW")
        
        
        
        self.buttonDeflection.grid(column = 0, row = 5,sticky = "EW")
        self.labelImage_density.grid(column = 0, row = 6,columnspan = 3, sticky = "NESW")
        self.buttonQuestion6.grid(column = 0, row = 7,sticky = "EW")
        self.spinboxk.grid(column = 1, row = 7,sticky = "EW")
        self.buttonQuestion7.grid(column = 0, row = 8,sticky = "EW")
        self.spinboxf.grid(column = 1, row = 8,sticky = "EW")
        self.buttonQuestion8.grid(column = 0, row = 9,sticky = "EW")
        self.spinboxdref.grid(column = 1, row = 9,sticky = "EW")
        self.buttonQuestion9.grid(column = 0, row = 10,sticky = "EW")
        self.spinboxpixelresolution.grid(column = 1, row = 10,sticky = "EW")
        self.checkLconstant.grid(column = 0, row = 11,sticky = "EW")
        self.checkLvariable.grid(column = 0, row = 12,sticky = "EW")
        self.spinboxL.grid(column = 1, row = 11,rowspan =2, sticky = "EW")
        self.buttonDensity.grid(column = 0, row = 13,sticky = "EW")
        
        
        
        
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------
    # ----------------------------- M E T H O D  --------------------------
    # ---------------------------------------------------------------------
    # ---------------------------------------------------------------------  
        
        
    def Load_gray(self):

        file_path_load_gray = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/python projects/Argon cluster size determination/Tab by class ",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.avi;*.mp4;*.jpg"),
                                                    ("JPG Files", "*.jpg")))
        self.cap = cv2.VideoCapture(file_path_load_gray)
        
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Gray video', gray)
            
            
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()
        
        
    def Load_RGB(self):

        file_path_load_RGB = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/python projects/Argon cluster size determination/Tab by class ",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.avi;*.mp4;*.jpg"),
                                                    ("JPG Files", "*.jpg")))


        cap = cv2.VideoCapture(file_path_load_RGB)
        
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
        plt.imshow(self.I1_ar,cmap='gray')
        plt.colorbar()
        
        
    def backgound_substraction(self):
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/python projects/Argon cluster size determination/Tab by class ",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.avi;*.mp4;*.jpg"),
                                                    ("JPG Files", "*.jpg")))
        cap = cv2.VideoCapture(file_path)
        
        
        treshold = int(self.spinboxTreshold.get())
        history = int(self.spinboxHistory.get())
        
        
        fgbg = cv2.createBackgroundSubtractorMOG2(history = history, varThreshold = treshold,detectShadows=False)
        
        ret, frame = cap.read()
        x = frame.shape[1]
        y = frame.shape[0]

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter('output_BGS.avi',fourcc, 10, (x,y),isColor=False)

        while (cap.isOpened()):
    
            ret, frame = cap.read()
    
            # if video finished or no Video Input
            if not ret:
                break
            
            fgmask = frame
    
            fgmask = fgbg.apply(frame)
            cv2.imshow('frame',fgmask)

            out.write(fgmask)

    
            # press 'Q' if you want to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        
    def add_timer(self):
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/python projects/Argon cluster size determination/Tab by class ",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.avi;*.mp4;*.jpg"),
                                                    ("JPG Files", "*.jpg")))
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        x = frame.shape[1]
        y = frame.shape[0]
        
        fps_out = int(self.spinboxOutFrameSec.get())
        fps_real = int(self.spinboxFrameSec.get())
        
        
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter('output.avi',fourcc, fps_out, (x,y))
        #out = cv2.VideoWriter('output.avi', -1, 20.0, (512,128))
          
        # used to record the time when we processed last frame
        prev_frame_time = 0
          
        # used to record the time at which we processed current frame
        new_frame_time = 0

        frame_count = -1
          
        # Reading the video file until finished
        while(cap.isOpened()):
          
            # Capture frame-by-frame
          
            ret, frame = cap.read()
          
            # if video finished or no Video Input
            if not ret:
                break
          
            # Our operations on the frame come here
            gray = frame
          
            # resizing the frame size according to our need
            #gray = cv2.resize(gray, (500, 300))
          
            # font which we will be using to display FPS
            font = cv2.FONT_ITALIC 
            # time when we finish processing for this frame
            new_frame_time = time.time()
            
            # count the frames
            frame_count  = frame_count + 1

          
            # Calculating the fps
          
            # fps will be number of frame processed in given time frame
            # since their will be most of time error of 0.001 second
            # we will be subtracting it to get more accurate result
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            
          
            # converting the fps into integer
            fps = int(fps)
            realtime = frame_count/fps_real*1000
            realtime = round(realtime,2)
          
            # converting the fps to string so that we can display it on frame
            # by using putText function
            realtime = str(realtime) + 'ms'
          
            # putting the FPS count on the frame
            cv2.putText(gray, realtime, (180, 30), font, 1, (255, 255, 255), 3, cv2.LINE_AA)
          
            # displaying the frame with fps
            cv2.imshow('frame', gray)
            
            # write the flipped frame
            out.write(gray)
          
            # press 'Q' if you want to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print(fps)
        # When everything done, release the capture
        cap.release()
        out.release()
        # Destroy the all windows now
        cv2.destroyAllWindows()
        
    def Plot_calibration(self):
        
        
        file_path = filedialog.askopenfilename(initialdir = "C:/Users/tomasetti/Documents/Article à publier/Article Champagne",
                                       title = "Select Image 1",
                                       filetypes = (("All Files", "*.xlsx"),
                                                    ("XLSX Files", "*.xlsx")))


        df = pd.read_excel(file_path)  
        arr = df.to_numpy()

        #Dimension of the data from the excel of the calibration      
        Data_len = int(self.spinboxLenQualibratonExcel.get())
        gray_value_column = int(self.spinboxGrayValueColumnExcel.get())
        gray_value_column = int(self.spinboxrColumnExcel.get())
        angle_column = int(self.spinboxAngleColumnExcel.get())

        self.Gray_value, self.r, self.angle_deg = arr[1:Data_len, gray_value_column], arr[1:Data_len, gray_value_column], arr[1:Data_len, angle_column]
        x = np.arange(0, len(self.Gray_value),1)
        
        #interpolation of calibration curve
        
        f = interpolate.interp1d(self.Gray_value, self.angle_deg)
                                            
        # plotting the calibration line
        plt.plot(self.Gray_value, self.angle_deg, 'o', self.Gray_value, f(self.Gray_value), '-')
      
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
           
            f = interpolate.interp1d(self.Gray_value, self.angle_deg)
            self.IM_thresholded_loop = np.zeros((len(self.I1_ar[:,1]),len(self.I1_ar[1]))); #allocate space for thresholded image

            for i in np.arange(0,len(self.I1_ar[:,1])):                                             #loop over all rows and columns
                for j in np.arange(0,len(self.I1_ar[1])):
                    
                    if np.min(self.Gray_value) <= self.I1_ar[i,j] <= np.max(self.Gray_value):
                        
                        self.IM_thresholded_loop[i,j]=f(self.I1_ar[i,j]) 
                    
                    elif self.I1_ar[i,j] <= np.min(self.Gray_value):
                        
                        self.IM_thresholded_loop[i,j] =f(np.min(self.Gray_value))
                        
                    elif self.I1_ar[i,j] >= np.max(self.Gray_value):
                            
                        self.IM_thresholded_loop[i,j] =f(np.max(self.Gray_value))
                        
                    
            plt.imshow(self.IM_thresholded_loop, cmap='gray_r')
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
        messagebox.showinfo ("information :","Schematic representation of a Schlieren imaging set up. This image is illustrative and you can put your own set-up image")
        
    def Question2(self):
        messagebox.showinfo ("information :","Gaussian Mixture-based Background/Foreground Segmentation: Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model. This parameter does not affect the background update.")
        
    def Question3(self):
        messagebox.showinfo ("information :","Gaussian Mixture-based Background/Foreground Segmentation: how many previous frames are used for building the background model. So basically if an item is standing at a fixed position for as many frames as the history size, then it will disappear in the background.")
    
    def Question4a(self):
        messagebox.showinfo ("information :","Excel column number of your gray values data")
    
    def Question4b(self):
        messagebox.showinfo ("information :","Excel column number of your r values")
    
    def Question4c(self):
        messagebox.showinfo ("information :","Excel column number of your deviation angle values.")
        
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
            
    def Question10(self):
            messagebox.showinfo ("information :","Real Frame/s of the initial video used to implement the timer")
            
    def Question11(self):
            messagebox.showinfo ("information :","Desired Frame/s of the final video")