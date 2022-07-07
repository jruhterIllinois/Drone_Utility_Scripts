import os
import time
import ftplib as FTP

parent_fldr = '/UAV_FIELDSEASON_2022/'
ftp_address = 'ftp.box.com'
drive_loc = ''

#Entering FTP Username and Passwd
while(True):
    user = input("Enter your FTP username: ")
    user_passwd = input("Enter your FTP password: ")
    if(user != None and user_passwd != None and ("@illinois.edu" in user)):
        break
    print("Must input valid username or password. Please try again.")

#Entering the Field ID
while(True):
    field_id = input("Enter the field flown: MSA, MSIN, MSICS, 4ROW: ")
    if(field_id == "MSA" or field_id == "MSIN" or field_id == "MSICS" or field_id == "4ROW"):
        break
    print("Must input valid field. Please try again.")

#Entering the Altitude
while(True):
    altitude = input("Enter the flight altitude (in meters): 10, 20, 30, 40: ")
    if(altitude == "10" or altitude == "20" or altitude == "30" or altitude == "40"):
        break
    print("Must input valid altitude. Please try again.")
    
#Entering the Date
while(True):
    input_date = input("Enter the date flown as MMDDYYYY: ")
    if(len(input_date) == 8 and input_date.isdigit()):
        break
    print("Must input valid date. Make sure you have no spaces or dashes. Please try again.")

#Entering the Type
while(True):
    ftype = input("Enter flight type Multispec (M) / Thermal (T): ")
    if(ftype == "M" or ftype == "T"):
        break
    print("Invalid input. Please try again.")

#Thermal (T)
if(ftype == "T"):
    print("Not yet functional. Aborting...")
    exit()
    
#Multispec (M)
session = FTP.FTP(ftp_address,user,user_passwd)

#Determining the destination file path (M)
if(ftype == "M"):
    if(field_id == "MSA"):
        subfolder = 'MSA'
    if(field_id == "MSIN"):
        subfolder = 'MSI/MSI N'
    if(field_id == "MSICS"):
        subfolder = 'MSI/MSI_C+S'
    if(field_id == "4ROW"):
        subfolder = '4Row'

#Generating the new subfolders (M)
    session.cwd(parent_fldr + subfolder)
    new_path_red = parent_fldr + subfolder + '/' + field_id + '_' + altitude + 'M_' + input_date + '_RED'
    new_path_blue = parent_fldr + subfolder + '/' + field_id + '_' + altitude + 'M_' + input_date + '_BLUE'
    session.mkd(new_path_red)
    session.mkd(new_path_blue)
    
#Walking the drive's folders (M)
    for subdir, dirs, files in os.walk(drive_loc):
        red_count = 1
        blue_count = 1
        print("Looking into ", subdir)
        for filename in files:
            if filename.endswith(".tif"):
                if(int(filename[9]) <= 5):
                    session.cwd(new_path_red)
                    renamed_file = filename.rename(filename, 'R' + red_count + '.tif')
                    session.storbinary('STOR ' + renamed_file, open(renamed_file, 'rb'))
                    print("Uploaded: " + renamed_file)
                    red_count += 1
                if(int(filename[9]) >= 6):
                    session.cwd(new_path_blue)
                    renamed_file = filename.rename(filename, 'B' + blue_count + '.tif')
                    session.storbinary('STOR ' + renamed_file, open(renamed_file, 'rb'))
                    print("Uploaded: " + renamed_file)
                    blue_count += 1
                    
print("Uploads Complete!")
session.quit()
exit()