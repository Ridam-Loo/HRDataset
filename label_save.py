#Save Images in new folder based on Image 
import sys

import csv
from csv import reader

import shutil


def hexSave (line,n=2):
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
 
def copyDirectory(src, dest):
    #from https://www.pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

if __name__ == "__main__":

    #python3 dImg.py <csv_filename> <folder_name> <new_folder> <label code> 
    '''
    csv_filename : csv file containgin human label data or machine generated (from Google Open Images)
    folder_name  : folder containing the full dataset 
    new_folder   : new place to save the images (the name of the label, ex: kitchens)
    label code   : Open images generated code for the label you wish to extract (see https://storage.googleapis.com/openimages/v6/oidv6-class-descriptions.csv)
    '''
    label_csv_filename = sys.argv[1]
    folderName =  sys.argv[2]
    newFolder = sys.argv[3]
    label_name = sys.argv[4]

    #keep track of number of images 
    imgCounter= 0 


    with open(label_csv_filename+".csv".format(label_csv_filename), 'r', encoding="ISO-8859-1") as csv_file:
    
        for indx,line in enumerate(reader(csv_file)):
            if line [2]== label_name and line [3]== 0 :
                location = hexSave(line[0], n=2)
                #save it 
                copyDirectory(folderName + '/' + location, newFolder + '/' + location)

            else:
                pass 









