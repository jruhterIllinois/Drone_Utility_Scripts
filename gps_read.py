import os
import glob
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
#rmt_dir = '/Users/jruhter/Documents/testetes'

#child_dir = next(os.walk(rmt_dir))[1]

output_path = og_dir+'/Output.txt'
fileOut = open(output_path, 'w+')
#print(fileOut)

lat = []
long = []

#for filename in sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime):

for subdir, dirs, files in os.walk(rmt_dir):
    
    print("Looking into", subdir )
        
    for filename in files:


        
        if filename.endswith(".tif"):
            if len(filename)<15 and filename[9] == '1' or filename[9] == '6' and filename.startswith('I'):
            #    print(filename)                
    #read tiff file into a pillow image obj
       #         print('Openning ', str(subdir), '/',filename)
                
          #      im = Image.open(str(subdir)+'/'+filename)

    #readin any existing exif data to a dict
          #   print(filename)
                exif_dict = piexif.load(str(subdir)+'/'+filename)
                breite = exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]

                lange = exif_dict['GPS'][piexif.GPSIFD.GPSLongitude]

                gpstime = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] #File Date
                alt = exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] #alt


#Convert to Decimal
                breite = breite[0][0] / breite[0][1] + breite[1][0] / (breite[1][1] * 60) + breite[2][0] / (breite[2][1] * 3600) #lat
                lange =  lange[0][0] / lange[0][1] + lange[1][0] / (lange[1][1] * 60) + lange[2][0] / (lange[2][1] * 3600) #long

                lange = -1*lange
          #      lat.append(breite)
           #     long.append(lange)         
                fileOut.write(str(subdir)+'/'+filename+',')
                fileOut.write(str(breite)+',')
                fileOut.write(str(lange)+',')
                fileOut.write(str(alt[0]/alt[1])+',')
                fileOut.write(str(gpstime)+',')
                fileOut.write(str(filename[9])+',')
                

                 



                if lange > low_msi_n_lon and lange < high_msi_n_lon:
                   if breite > low_msi_n_lat and breite < high_msi_n_lat:
                       #  print('Found MSI N')
                        fileOut.write('0')                      
                elif lange > low_msa_n_lon and lange < high_msa_n_lon:
                    if breite > low_msa_n_lat and breite < high_msa_n_lat:
                       #  print('Found MSI N')
                        fileOut.write('1')
                else :
                    if breite > low_msiCS_n_lat and breite < high_msiCS_n_lat:
                       #  print('Found MSI N')
                        fileOut.write('2')

                        
                         
                 
                fileOut.write('\n')         

#plt.scatter(long, lat)
#plt.show()

print('Writing File')
fileOut.close()

# https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif.html

         #    fileString = filename.split('_')
         #   indexNumStr = fileString[2].split('.')
         #   newFileName = str(indexNumStr[0]) + '_' + str(fileString[1]) +'.tif'
         #  print(newFileName)
# shutil.copy(filename, newFileName)
         



