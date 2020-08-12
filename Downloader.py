
## Assuming a csv file has Google Open Images Metadata from
## Image Names are in urls 

import sys
import urllib.request #to save file

import os.path
from os import path
import os,shutil

import csv
from csv import reader

import hashlib

import time #used for delay 

import base64 #used to check md5

#-----------------------------------------------

def checkSum(image):
    '''
    The following function takes in the image file passed and finds the MD5 sum, then converts it to base64
    '''
    md5_hash = hashlib.md5()
    with open(image,"rb") as f:
    # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        hashbrown= md5_hash.hexdigest()

        return base64.b64encode(bytes.fromhex(hashbrown)) #convert to base 64, returns in bytes

def hexSave (line,n):
    '''
    the following function creates a sting which represents the file path
    line : name of the file 
    n : seperation between characters
    hexSave("9f04bfa9a7c30a8b", 2)
    >>>8b/0a/c3/a7/a9/bf/04/9f/9f04bfa9a7c30a8b
    '''
    foo=[line[i:i+n] for i in range(0, len(line), n)]
    foo.reverse()
    newfoo = [item + '/' for item in foo]
    listToStr = ''.join(map(str, newfoo)) 
    final = listToStr + line+ '/' 

    return final


#-----------------------------------------------

#python3 dImg.py <csv_filename> <folder_name> 
csv_filename = sys.argv[1]
folderName =  sys.argv[2]

with open(csv_filename+".csv".format(csv_filename), 'r', encoding="ISO-8859-1") as csv_file:
    skipped_image = 0 
    unavailible_images = 0
    wrong_res_img = 0
    donwloaded_total = 0 

    sucess =[] # nested list to put all downloaded metadata
    missing=[] #nested list containing all missing images 

    time_dict ={}
    #reader = csv.reader( (line.replace('\0','') for line in csv_file) )

    for indx,line in enumerate(reader(csv_file)):
      
        #create a new file with information for sucessfully downloaded images
        with open('downloaded_files.csv', 'w', newline='') as f_out :
            writer = csv.writer(f_out)
            writer.writerow(["ImageID", "Subset", "OriginalURL", "OriginalLandingURL","License", "AuthorProfile", "Author", "Title", "OriginalSize", "OriginalMD5","Thumbnail300KURL", "Rotation"])
            writer.writerows(sucess)

         #create a file to keep track of all the missing files 
        with open('missing_files.csv', 'w',newline='') as f1 :
            writer = csv.writer(f1)
            writer.writerow(["ImageID", "Subset", "OriginalURL", "OriginalLandingURL","License", "AuthorProfile", "Author", "Title", "OriginalSize", "OriginalMD5","Thumbnail300KURL", "Rotation"])
            writer.writerows(missing)

        location = hexSave(line[0],2)

        if os.path.isfile( folderName+"/" + location + line[0]+'.jpg' ) or os.path.isfile( folderName+"/" + "INCOMPLETE"+ line[2].split('/')[-1]+'.jpg' ) :
            #print ("Image already exists for {0}".format(line[0]))
            skipped_image += 1
        else:
            if line[0] != '' and indx != 0 and int(line[8])>= 1048576: #appropriate resolution
                try:
                    #time log
                    start_time = time.time()

                    imgName="INCOMPLETE"+ line[2].split('/')[-1]
                    urllib.request.urlretrieve(line[2], folderName+"/" + imgName)


                    #CHECK MD5 sum ----------------------
                    #correct sum 
                    originalMD5 = line[9]
                    md5_returned=checkSum(folderName+"/" + imgName)
                    
                    #decode retruned MD5 from byte to convert it to a string
                    if originalMD5 == md5_returned.decode('utf-8'):
                    
                        print("----")
                        
                        # rename it now that we have checked 
                        # Purpose: ensure partially saved files aren't included 

                        location = hexSave(line[0],2) #get path where image should be saved
                    
                        os.makedirs(folderName+'/'+ location,0o755) #create the actual directory 

                        #newimgName = line[0]+".jpg" #name of the image
                    
                        os.rename(folderName+"/" + imgName,folderName+"/" + location + line[0]+'.jpg') #NOT WORKINGGGGG
                        #shutil.move(folderName+"/" + imgName,folderName+"/" + location +'.jpg')
                        print ("Image saved for {0}".format(line[0]))


                        end_time = time.time()


                        #to keep track of stats (downloaded files, then time)
                        donwloaded_total +=1 
                        sucess.append(line[:])
                        
                        time_one_pic= end_time-start_time
                        print("Image {0}".format(line[0]), "took", time_one_pic,"seconds to download")

                        time_dict[line[0]]= time_one_pic
                        print("Total images downloaded:", donwloaded_total)
                    
                        time.sleep(0.5) #ADDED DELAY 


                    else: #if MD5 sum does not match
                        print("oh no!Wrong MD5 Sum")
                        print("Actual MD5: ",md5_returned.decode('utf-8'))
                        print("Given MD5: ",originalMD5)

                except:
                    #print("Image unavailable for {0}".format(line[0]))
                    unavailible_images += 1
                    missing.append(line[:])
                        
            else:
                #print ("Image wrong resolution: {0}".format(line[0]))
                wrong_res_img += 1


#--------------------------------------------------------------

#"sanity" check tally 
print("------------------ DOWNLOAD COMPLETED ----------------------")    

print("Unavailable images:", unavailible_images)
print("Images of the wrong resolution:", wrong_res_img)
print("Images skipped:", skipped_image)
print("Total number of downloaded images:", donwloaded_total)