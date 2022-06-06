import os
import ftplib as FTP
import time


flghtImgInfoFile = '/Users/jruhter/Desktop/Output.txt'



flghtImgInfo = open(flghtImgInfoFile,'r')
flghtLines = flghtImgInfo.readlines()
file_paths = []
parentFLDR = []
file_date = []


folder_id = '/UAV_FIELDSEASON_2022/'

MSI_N_20_M = 'MSI/MSI N/20M'
MSI_N_20_BLUE = 'MSI/MSI N/20M/Blue'
MSI_N_20_RED = 'MSI/MSI N/20M/Red'

MSI_N_40_M = 'MSI/MSI N/40M'
MSI_N_40_BLUE = 'MSI/MSI N/40M/Blue'
MSI_N_40_RED = 'MSI/MSI N/40M/Red'


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
                parentFLDR.append(folder_id+MSI_N_40_BLUE)       
            else :             
                parentFLDR.append(folder_id+MSI_N_40_RED)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_N_20_BLUE)        
            else :             
                parentFLDR.append(folder_id+MSI_N_20_RED)
        else:
            parentFLDR.append(folder_id+MSI_N_20_RED)
    elif(imgInfo[6] == '1'):
        if(float(imgInfo[3]) > 260.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_40_BLUE)       
            else :             
                parentFLDR.append(folder_id+MSA_40_RED)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSA_20_BLUE)        
            else :             
                parentFLDR.append(folder_id+MSA_20_RED)
        else:
            parentFLDR.append(folder_id+MSA_20_RED)
    else:
        if(float(imgInfo[3]) > 260.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_CS_40M_BLUE)       
            else :             
                parentFLDR.append(folder_id+MSI_CS_40M_RED)             
        elif(float(imgInfo[3]) >240.0):
            if(imgInfo[5] == '0'):          
                parentFLDR.append(folder_id+MSI_CS_20M_BLUE)        
            else :             
                parentFLDR.append(folder_id+MSI_CS_20M_RED)
        else:
            parentFLDR.append(folder_id+MSI_CS_20M_RED)
    
user = ''
ftp_address = 'ftp.box.com'
user_passwd = ''

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
    

#print(f'File "{new_file.name}" uploaded to Box with file ID {new_file.id}')







