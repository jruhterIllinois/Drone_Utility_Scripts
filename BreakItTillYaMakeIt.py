import os
import time
import ftplib as FTP

#Constants
parent_fldr = '/UAV_FIELDSEASON_2022/'
ftp_address = 'ftp.box.com'

def uploadToBox(var):

    #Variables
    drive_loc = ''
    user = var.root_tk.uB_root_tk.uB_usernameLab_entry.get()
    user_passwd = var.root_tk.uB_passwordLab_entry.get()
    ftype = "M"
    altitude = var.root_tk.uB_AltSlider.get()
    print(user, user_passwd)

    #Starting Session
    session = FTP.FTP(ftp_address,user,user_passwd)

    #Determining the destination file path
    if(field_id == "MSA"):
        subfolder = 'MSA'
    if(field_id == "MSIN"):
        subfolder = 'MSI/MSI N'
    if(field_id == "MSICS"):
        subfolder = 'MSI/MSI_C+S'
    if(field_id == "4ROW"):
        subfolder = '4Row'

    #Generating the new subfolders
    if(ftype == "M"):
        session.cwd(parent_fldr + subfolder)
        new_path_red = parent_fldr + subfolder + '/' + field_id + '_' + altitude + 'M_' + input_date + '_RED'
        new_path_blue = parent_fldr + subfolder + '/' + field_id + '_' + altitude + 'M_' + input_date + '_BLUE'
        session.mkd(new_path_red)
        session.mkd(new_path_blue)
    if(ftype == "T"):
        session.cwd(parent_fldr + subfolder)
        new_path_thermal = parent_fldr + subfolder + '/' + field_id + '_' + altitude + 'M_' + input_date + '_THERMAL'
        session.mkd(new_path_thermal)

    #Thermal (T)

    #Walking the drive's folders (T)
    if(ftype == "T"):
        for root, subdir, files in os.walk(drive_loc):
            for filename in files:
                if filename.endswith(".TFC"):
                    os.chdir(root)
                    try:
                        stream = open(filename, 'rb')
                        session.cwd(new_path_thermal)
                        session.storbinary('STOR ' + filename, stream)
                        print("Uploaded: " + filename)
                        stream.close()
                    except:
                        print("File Upload Failed: " + filename)
    print("Uploads Complete!")
    session.quit()
        
    #Multispec (M)
        
    #Walking the drive's folders (M)
    if(ftype == "M"):
        for root, subdir, files in os.walk(drive_loc):
            for filename in files:
                if filename.endswith(".tif"):
                    os.chdir(root)
                    try:
                        stream = open(filename, 'rb')
                        if(int(filename[9]) <= 5):
                            session.cwd(new_path_red)
                            session.storbinary('STOR ' + filename, stream)
                            print("Uploaded: " + filename)

                        if(int(filename[9]) >= 6):
                            session.cwd(new_path_blue)
                            session.storbinary('STOR ' + filename, open(filename, 'rb'))
                            print("Uploaded: " + filename)
                        stream.close()
                    except:
                        print("File Upload Failed: " + filename)
    print("Uploads Complete!")
    session.quit()

def StartFTP():

#Entering FTP Username and Passwd
    while(True):
        user = input("Enter your FTP username: ")
        user_passwd = input("Enter your FTP password: ")
        if(user != None and user_passwd != None and ("@illinois.edu" in user)):
            break
        print("Must input valid username or password. Please try again.")


def SetField():
    
 #Entering the Field ID
    while(True):
        field_id = input("Enter the field flown: MSA, MSIN, MSICS, 4ROW: ")
        if(field_id == "MSA" or field_id == "MSIN" or field_id == "MSICS" or field_id == "4ROW"):
            break
        print("Must input valid field. Please try again.")

def SetAltitude():
    
#Entering the Altitude
    while(True):
        altitude = input("Enter the flight altitude (in meters): 10, 20, 30, 40: ")
        if(altitude == "10" or altitude == "20" or altitude == "30" or altitude == "40"):
            break
        print("Must input valid altitude. Please try again.")

def SetDate():
    
#Entering the Date
    while(True):
        input_date = input("Enter the date flown as MMDDYYYY: ")
        if(len(input_date) == 8 and input_date.isdigit()):
            break
        print("Must input valid date. Make sure you have no spaces or dashes. Please try again.")


def SetFlightType():

#Entering the Type
    while(True):
        ftype = input("Enter flight type Multispec (M) / Thermal (T): ")
        if(ftype == "M" or ftype == "T"):
            break
        print("Invalid input. Please try again.")

