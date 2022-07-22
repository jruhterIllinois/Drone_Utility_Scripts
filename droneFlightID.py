import tkinter
from tkinter import filedialog
from tkinter import *
import time
import tkintermapview
import os
import piexif
import glob
import shutil
import math




class GUI:

    def __init__(self):
        # create tkinter window
        self.root_tk = tkinter.Tk()
        self.root_tk.geometry(f"{1000}x{700}")
        self.root_tk.title("map_view_polygon_example.py")



        self.root_tk.infoFrame = Frame(self.root_tk)
        self.root_tk.infoFrame.pack(padx=10, pady=10)
        self.dirSelect = 'No Dir Selected'

        self.root_tk.controlFrame = Frame(self.root_tk)
        self.root_tk.controlFrame.pack(padx=1, pady=5)

### create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.root_tk, width=1000, height=700, corner_radius=0)
        self.map_widget.pack(padx=10, pady=30)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(40.0664379,-88.1968861, marker=False)


        self.root_tk.dirDisplayMessage = Text(self.root_tk.infoFrame , height = 1, width = 40, bg = 'white', fg = 'black')
        self.root_tk.dirDisplayMessage.insert(END, self.dirSelect)
        self.root_tk.dirDisplayMessage.grid(row=0, column=0)

        self.root_tk.button2 = Button(self.root_tk.infoFrame ,text="Browse for Flight Dir", command=self.browse_button, height=1, width=20)
        self.root_tk.button2.grid(row=0, column=1)

        self.root_tk.button3 = Button(self.root_tk.infoFrame ,text="Start GPS Search", command=self.collectGpsPoint, height=1, width=20, fg = 'red' )
        self.root_tk.button3.grid(row=0, column=2)
        

        self.root_tk.targetLocMessage = Text(self.root_tk.controlFrame , height = 1, width = 40, bg = 'white', fg = 'black')
        self.root_tk.targetLocMessage.insert(END, 'test')
        self.root_tk.targetLocMessage.grid(row=0, column=0)

        self.root_tk.button4 = Button(self.root_tk.controlFrame ,text="Load Field File", command=self.browse_conf, height=1, width=20, fg = 'black' )
        self.root_tk.button4.grid(row=0, column=2)

        self.root_tk.confDisplayMessage = Text(self.root_tk.controlFrame , height = 1, width = 60, bg = 'white', fg = 'black')
        self.root_tk.confDisplayMessage.insert(END, self.dirSelect)
        self.root_tk.confDisplayMessage.grid(row=0, column=0)   

        self.root_tk.mainloop()
        

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
        fileCounter = 0
        for subdir, dirs, files in os.walk(self.dirSelect):
                 
            for filename in files:
                
                if filename.endswith(".tif") and fileCounter < 500:
                    if len(filename)<15 and filename[9] == '1' or filename[9] == '6' and filename.startswith('I'):
                        
                        fileCounter = fileCounter + 1
                        exif_dict = piexif.load(str(subdir)+'/'+filename)
                        breite = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]

                        lange = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]

                        gpstime = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] #File Date
                        alt = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] #alt


        #Convert to Decimal
                        breite = breite[0][0] / breite[0][1] + breite[1][0] / (breite[1][1] * 60) + breite[2][0] / (breite[2][1] * 3600) #lat
                        lange =  lange[0][0] / lange[0][1] + lange[1][0] / (lange[1][1] * 60) + lange[2][0] / (lange[2][1] * 3600) #long

                        llange.append(-1*lange)
                        lbreite.append(math.floor(breite*100000000)/100000000)
                        
                        
        
                        
                    #    self.mapPoint()
                   #     print('Found one at', self.lange, self.breite)
                   #     time.sleep(3)
                
                   
        for i in range(1,20):
            self.breite = lbreite[i*20]
            self.lange = llange[i*20]
            self.mapName = str(i*20)
            self.mapPoint()


        
     #   print(llange)



GUI()



