import tkinter
from tkinter import filedialog
from tkinter import *
from statistics import mode
import time
import tkintermapview
import os
import piexif
import glob
import shutil
import math
import BreakItTillYaMakeIt as btmi

class GUI:

    def __init__(self):
        # create tkinter window
        self.root_tk = tkinter.Tk()
        self.root_tk.geometry(f"{1400}x{900}")
        self.root_tk.title("map_view_polygon_example.py")

        self.root_tk.uploadFrame = Frame(self.root_tk)
        self.root_tk.uploadFrame.grid(column=1, row=0)
        self.root_tk.userFrame = Frame(self.root_tk)
        self.root_tk.userFrame.grid(column=0, row=0)

        self.root_tk.infoFrame = Frame(self.root_tk.userFrame)
        self.root_tk.infoFrame.pack(padx=10, pady=10)
        self.dirSelect = 'Choose a Directory'

        self.root_tk.controlFrame = Frame(self.root_tk.userFrame)
        self.root_tk.controlFrame.pack(padx=1, pady=5)

        self.root_tk.FlightEstFrame = Frame(self.root_tk.userFrame)
        self.root_tk.FlightEstFrame.pack(padx=1, pady=5)
        
### create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.root_tk.userFrame, width=1000, height=700, corner_radius=0)
        self.map_widget.pack(padx=10, pady=30)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(40.0664379,-88.1968861, marker=False)


        self.root_tk.dirDisplayMessage = Text(self.root_tk.infoFrame , height = 1, width = 40, bg = 'white', fg = 'black',state='normal')
        self.root_tk.dirDisplayMessage.insert(END, self.dirSelect)
        self.root_tk.dirDisplayMessage.grid(row=0, column=0)

        self.root_tk.button2 = Button(self.root_tk.infoFrame ,text="Select Flight", command=self.browse_button, height=1, width=20)
        self.root_tk.button2.grid(row=0, column=1)

        self.root_tk.button3 = Button(self.root_tk.infoFrame ,text="Start GPS Search", command=self.collectGpsPoint, height=1, width=20, fg = 'red' )
        self.root_tk.button3.grid(row=0, column=2)
        

        self.root_tk.targetLocMessage = Text(self.root_tk.controlFrame , height = 1, width = 40, bg = 'white', fg = 'black', state='disabled')
        self.root_tk.targetLocMessage.insert(END, 'test')
        self.root_tk.targetLocMessage.grid(row=0, column=0)

        self.root_tk.button4 = Button(self.root_tk.controlFrame ,text="Select File", command=self.browse_conf, height=1, width=20, fg = 'black' )
        self.root_tk.button4.grid(row=0, column=2)

        self.root_tk.confDisplayMessage = Text(self.root_tk.controlFrame , height = 1, width = 60, bg = 'white', fg = 'black')
        self.root_tk.confDisplayMessage.insert(END, 'Choose a Field Configuration File')
        self.root_tk.confDisplayMessage.grid(row=0, column=0)

        self.root_tk.AltEst = Text(self.root_tk.FlightEstFrame, height = 1, width = 8, bg = 'white', fg = 'black')
        self.root_tk.AltEst.insert(END, 'NaN')
        self.root_tk.AltEst.grid(row=0, column=0)

        self.root_tk.AltLabel = Label(self.root_tk.FlightEstFrame, text='Estimated Alt', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.AltLabel.grid(row=0, column=1)

        self.root_tk.cameraEst = Text(self.root_tk.FlightEstFrame, height = 1, width = 8, bg = 'white', fg = 'black')
        self.root_tk.cameraEst.insert(END, 'NaN')
        self.root_tk.cameraEst.grid(row=0, column=2)

        self.root_tk.cameraEstLabel = Label(self.root_tk.FlightEstFrame, text='Estimated Camera', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.cameraEstLabel.grid(row=0, column=3)




### upload frames widgets:

        self.root_tk.uploadBoxFrameLabel = Label(self.root_tk.uploadFrame , text='Upload Criteria', relief=FLAT, height = 1, width = 39, bg='white', fg='black')
        self.root_tk.uploadBoxFrameLabel.pack(padx=30, pady=0)


        self.root_tk.uB_frame = Frame(self.root_tk.uploadFrame)
        self.root_tk.uB_frame.pack(padx=40, pady=5)


        self.root_tk.uB_fieldLab = Label(self.root_tk.uB_frame, text='Field Name:', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.uB_fieldLab.grid(row=0, column=0)

        self.root_tk.uB_field_entry = Text(self.root_tk.uB_frame, height = 1, width = 20, bg = 'white', fg = 'black')
        self.root_tk.uB_field_entry.insert(END, 'NaN')
        self.root_tk.uB_field_entry.grid(row=0, column=1)


        self.root_tk.uB_DateLab = Label(self.root_tk.uB_frame, text='Date:', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.uB_DateLab.grid(row=1, column=0)

        self.root_tk.uB_Date_entry = Text(self.root_tk.uB_frame, height = 1, width = 20, bg = 'white', fg = 'black')
        self.root_tk.uB_Date_entry.insert(END, 'NaN')
        self.root_tk.uB_Date_entry.grid(row=1, column=1)

        self.root_tk.uB_usernameLab = Label(self.root_tk.uB_frame, text='Box Username:', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.uB_usernameLab.grid(row=2, column=0)

        self.root_tk.uB_usernameLab_entry = Text(self.root_tk.uB_frame, height = 1, width = 20, bg = 'white', fg = 'black')
        self.root_tk.uB_usernameLab_entry.insert(END, 'NaN')
        self.root_tk.uB_usernameLab_entry.grid(row=2, column=1)       
        
        self.root_tk.uB_passwordLab = Label(self.root_tk.uB_frame, text='Box Password:', relief=RAISED, height = 1, width = 15, bg='white', fg='black')
        self.root_tk.uB_passwordLab.grid(row=3, column=0)

        self.root_tk.uB_passwordLab_entry = Text(self.root_tk.uB_frame, height = 1, width = 20, bg = 'white', fg = 'black')
        self.root_tk.uB_passwordLab_entry.insert(END, 'NaN')
        self.root_tk.uB_passwordLab_entry.grid(row=3, column=1)

        self.root_tk.uB_AltSliderLab = Label(self.root_tk.uB_frame, text='Select Altitude:', relief=RAISED, height = 3, width = 15, bg='white', fg='black')
        self.root_tk.uB_AltSliderLab.grid(row=4, column=0)
        
        self.root_tk.uB_AltSlider = Scale(self.root_tk.uB_frame, from_=0, to=100,tickinterval=25, length= 160, orient=HORIZONTAL, bg = 'white', fg = 'black')
        self.root_tk.uB_AltSlider.grid(row=4, column=1)

        self.root_tk.uB_TypeLab = Label(self.root_tk.uB_frame, text='Flight Type:', relief=RAISED, height = 2, width = 15, bg='white', fg='black')
        self.root_tk.uB_TypeLab.grid(row=5, column=0)

        self.root_tk.uB_var = StringVar()
        self.root_tk.uB_Type_entry0 = Radiobutton(self.root_tk.uB_frame, text='Multispectral', variable = self.root_tk.uB_var, value = 'M')
        self.root_tk.uB_Type_entry1 = Radiobutton(self.root_tk.uB_frame, text='Thermal', variable = self.root_tk.uB_var, value = 'T')
        self.root_tk.uB_Type_entry0.grid(row=5, column=1)
        self.root_tk.uB_Type_entry1.grid(row=6, column=1)

        self.root_tk.button5 = Button(self.root_tk.uB_frame ,text="Upload", command=self.upload2Box, height=2, width=15, fg = 'black' )
        self.root_tk.button5.grid(row=6, column=0)       

        

        self.root_tk.mainloop()


    def upload2Box(self):
        
        btmi.uploadToBox(self)     
        

    def browse_button(self):
    # Allow user to select a directory and store it in global var
    # called folder_path
    
        self.dirSelect = filedialog.askdirectory()
        self.root_tk.dirDisplayMessage.delete("1.0", END)
        self.root_tk.dirDisplayMessage.insert(END, self.dirSelect)
        
    def load_conf_points(self):
        self.siteName =[]
        self.lat1 = []
        self.lat2 = []
        self.long1 = []
        self.long2 = []
        conf_fd = open(self.confSelect,'r')
        lines_in = conf_fd.readlines()
        for line in lines_in:
            words = line.split()
            if words:           
                if(words[0] == 'Name'):
                    self.siteName.append(words[2])
                elif(words[0] == 'Lat1'):
                    self.lat1.append(words[2])
                elif(words[0] == 'Lat2'):
                    self.lat2.append(words[2])
                elif(words[0] == 'Long1'):
                    self.long1.append(words[2])
                elif(words[0] == 'Long2'):
                    self.long2.append(words[2])
                else:
                    print('Did not recognize conf')
                    
        i=0
        for entries in self.siteName:
            self.map_widget.set_polygon([(float(self.lat1[i]), float(self.long1[i])),
                                        (float(self.lat1[i]),   float(self.long2[i])),
                                        (float(self.lat2[i]),   float(self.long2[i])),
                                        (float(self.lat2[i]),   float(self.long1[i]))], name=entries, fill_color='')
            i=i+1
        
        

    def browse_conf(self):
    # Allow user to select a directory and store it in global var
    # called folder_path
    
        self.confSelect = filedialog.askopenfilename()
        self.root_tk.confDisplayMessage.delete("1.0", END)
        self.root_tk.confDisplayMessage.insert(END, self.confSelect)
        self.load_conf_points()

    def mapPoint(self):
    #    print('Mapping Point ', self.breite, ' ', self.lange)
        self.map_widget.set_marker(self.breite, self.lange, text=self.mapName, text_color="green",
                                 marker_color_circle="black", marker_color_outside="gray40", font=("Helvetica Bold", 24))



    def collectGpsPoint(self):

      
        lbreite = []
        llange  = []
        altEst = []
        fileCounter = 0
        for subdir, dirs, files in os.walk(self.dirSelect):
                 
            for filename in files:
                
                if filename.endswith(".tif") and fileCounter < 800:
                    if len(filename)<15 and filename[9] == '1' or filename[9] == '6' and filename.startswith('I'):
                        
                        fileCounter = fileCounter + 1
                        exif_dict = piexif.load(str(subdir)+'/'+filename)
                        breite = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]

                        lange = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]

                        gpstime = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] #File Date
                        fileAltIn = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude]

                        altEst.append(math.floor(fileAltIn[0]/fileAltIn[1]))


        #Convert to Decimal
                        breite = breite[0][0] / breite[0][1] + breite[1][0] / (breite[1][1] * 60) + breite[2][0] / (breite[2][1] * 3600) #lat
                        lange =  lange[0][0] / lange[0][1] + lange[1][0] / (lange[1][1] * 60) + lange[2][0] / (lange[2][1] * 3600) #long

                        llange.append(-1*lange)
                        lbreite.append(math.floor(breite*100000000)/100000000)

                        if(filename[9] == '1'):
                            self.cameraEst = 'Red'
                        else:
                            self.cameraEst = 'Blue'
                        
                        
                        
        
                        
                    #    self.mapPoint()
                   #     print('Found one at', self.lange, self.breite)
                   #     time.sleep(3)

                   
        self.altEst =  mode(altEst) - 220    
        self.root_tk.AltEst.delete("1.0", END)
        self.root_tk.AltEst.insert(END, self.altEst)

        self.root_tk.cameraEst.delete("1.0", END)
        self.root_tk.cameraEst.insert(END, self.cameraEst)
        
                   
        for i in range(1,20):
            self.breite = lbreite[i*20]
            self.lange = llange[i*20]
            self.mapName = str(i*20)
            self.mapPoint()


        
     #   print(llange)



GUI()
