import os
import time
import glob
import ftplib as FTP
import shutil
import matplotlib.pyplot as plt
import piexif
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

og_dir = os.getcwd()

high_msi_n_lon = -88.1958
low_msi_n_lon = -88.1968
low_msi_n_lat = 40.06732
high_msi_n_lat = 40.06795

high_msa_n_lon = -88.1949
low_msa_n_lon = -88.1961
low_msa_n_lat = 40.0672
high_msa_n_lat = 40.0684

high_msiCS_n_lon = -88.1954
low_msiCS_n_lon = -88.1971
low_msiCS_n_lat = 40.0665
high_msiCS_n_lat = 40.0673

rmt_dir = '/Volumes/NO NAME'
output_path = og_dir+'/Output.txt'
fileOut = open(output_path, 'w+')

lat = []
long = []

#Entering FTP Username and Passwd
user = input("Enter your FTP username:")
user_passwd = input("Enter your FTP password:")
if(user == None || user_passwd == None) {
    print("Must input username or password. Aborting program...")
    exit()
}

for subdir, dirs, files in os.walk(rmt_dir):
    
    print("Looking into", subdir )
        
    for filename in files:
        
        if filename.endswith(".tif"):
            if len(filename)<15 and filename[9] == '1' or filename[9] == '6' and filename.startswith('I'):               
    #Read tiff file into a pillow image obj
    #Read in any existing exif data to a dict
                exif_dict = piexif.load(str(subdir)+'/'+filename)
                breite = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]

                lange = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]

                gpstime = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] #File Date
                alt = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] #alt
    #Convert to Decimal
                breite = breite[0][0] / breite[0][1] + breite[1][0] / (breite[1][1] * 60) + breite[2][0] / (breite[2][1] * 3600) #lat
                lange =  lange[0][0] / lange[0][1] + lange[1][0] / (lange[1][1] * 60) + lange[2][0] / (lange[2][1] * 3600) #long

                lange = -1*lange
            
                fileOut.write(str(subdir)+'/'+filename+',')
                fileOut.write(str(breite)+',')
                fileOut.write(str(lange)+',')
                fileOut.write(str(alt[0]/alt[1])+',')
                fileOut.write(str(gpstime)+',')
                fileOut.write(str(filename[9])+',')

                if lange > low_msi_n_lon and lange < high_msi_n_lon:
                   if breite > low_msi_n_lat and breite < high_msi_n_lat:
                        fileOut.write('0')                      
                elif lange > low_msa_n_lon and lange < high_msa_n_lon:
                    if breite > low_msa_n_lat and breite < high_msa_n_lat:
                        fileOut.write('1')
                else :
                    if breite > low_msiCS_n_lat and breite < high_msiCS_n_lat:
                        fileOut.write('2')
                fileOut.write('\n')         

print('Writing File')
fileOut.close()

time.sleep(3);
print('Starting Upload Script ...')

flghtImgInfoFile = '/Users/jruhter/Desktop/Output.txt'

flghtImgInfo = open(flghtImgInfoFile,'r')
flghtLines = flghtImgInfo.readlines()
file_paths = []
parentFLDR = []
file_date = []

folder_id = '/UAV_FIELDSEASON_2022/'

MSI_N_20_M = 'MSI/MSI N/20M'
MSI_N_20M_BLUE = 'MSI/MSI N/20M/Blue'
MSI_N_20M_RED = 'MSI/MSI N/20M/Red'

MSI_N_40M = 'MSI/MSI N/40M'
MSI_N_40M_BLUE = 'MSI/MSI N/40M/Blue'
MSI_N_40M_RED = 'MSI/MSI N/40M/Red'


MSI_CS_20M = 'MSI/MSI_C+S/20 M'
MSI_CS_20M_BLUE = 'MSI/MSI_C+S/20 M/BLUE'
MSI_CS_20M_RED = 'MSI/MSI_C+S/20 M/RED'

MSI_CS_40M = 'MSI/MSI_C+S/40 M'
MSI_CS_40M_BLUE = 'MSI/MSI_C+S/40 M/BLUE'
MSI_CS_40M_RED = 'MSI/MSI_C+S/40 M/RED'

MSA_20M = 'MSA/MSA 20m'
MSA_20M_BLUE = 'MSA/MSA 20m/MULTISPEC/BLUE'
MSA_20M_RED = 'MSA/MSA 20m/MULTISPEC/RED'

MSA_40M = 'MSA/MSA 40m'
MSA_40M_BLUE = 'MSA/MSA 40m/Blue'
MSA_40M_RED = 'MSA/MSA 40m/Red'

for line in flghtLines:
    imgInfo = line.split(",")
    file_paths.append(imgInfo[0])
    file_date.append(imgInfo[4][2:12])
    if(imgInfo[6] == '0'):
        if(float(imgInfo[3]) > 260.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_N_40M_REDS)       
            else :             
                parentFLDR.append(folder_id+MSI_N_40M_BLUE)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_N_20M_RED)        
            else :             
                parentFLDR.append(folder_id+MSI_N_20M_BLUE)
        else:
            parentFLDR.append(folder_id+MSI_N_20_RED)
    elif(imgInfo[6] == '1'):
        if(float(imgInfo[3]) > 260.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_40M_RED)       
            else :             
                parentFLDR.append(folder_id+MSA_40M_BLUE)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_20M_RED)        
            else :             
                parentFLDR.append(folder_id+MSA_20M_BLUE)
        else:
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_20M_RED)        
            else :             
                parentFLDR.append(folder_id+MSA_20M_BLUE)
    else:
        if(float(imgInfo[3]) > 260.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_CS_40M_RED)       
            else :             
                parentFLDR.append(folder_id+MSI_CS_40M_BLUE)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_CS_20M_RED)        
            else :             
                parentFLDR.append(folder_id+MSI_CS_20M_BLUE)
        else:
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_20M_RED)        
            else :             
                parentFLDR.append(folder_id+MSA_20M_BLUE)

ftp_address = 'ftp.box.com'
session = FTP.FTP(ftp_address,user,user_passwd)

cwd = os.getcwd()

indx = 0
fIdx = 0

for copyFolder in parentFLDR:
    print(copyFolder, '  ', file_paths[indx], ' ' , file_date[indx])
    items = session.nlst(copyFolder)
    fIdx = 0
    print('Searching ',copyFolder, 'items ', items) 
    for item in items:
        if item == str(file_date[indx]) and fIdx == 0:
            subfolder = item
            print('Found Item in ', copyFolder)
            fIdx = 1
        elif item == str(file_date[indx]) and fIdx == 1:
            subfolder = item
            
    if(fIdx == 0):
        print('Creating SubFolder ', str(file_date[indx]))
        session.mkd(copyFolder+'/'+str(file_date[indx]))
        subfolder = str(file_date[indx])
    else: 
        print('Folder Already Exist ')

    print('Uploading ', file_paths[indx], 'to ',  copyFolder+'/'+subfolder)
    
    for camerIdx in range(0, 5):
        session.cwd(copyFolder+'/'+subfolder)
        nmIdx = file_paths[indx].find('IMG')
        file2upload = file_paths[indx][0:nmIdx+8] + '_'+str(int(file_paths[indx][nmIdx+9])+camerIdx) + '.tif'
        lfile_name = file_paths[indx][nmIdx:nmIdx+8] + '_'+str(int(file_paths[indx][nmIdx+9])+camerIdx) + '.tif'
        print('Index ', camerIdx, 'File to upload', file_paths[indx], ' ', file2upload, 'Name :', lfile_name)
        stream = open(file2upload, 'rb')
        file_name_up = lfile_name

        uploadedFile = 0
        while(uploadedFile == 0):
            try:
                str_clb = session.storbinary('STOR  '+file_name_up,stream)
                uploadedFile = 1
            except:
                print('Failed to Upload Retry')
                time.sleep(1)
                uploadedFile = 0
                
            
        stream.close()
  
    
    indx = indx +1

print('Upload Complete')
