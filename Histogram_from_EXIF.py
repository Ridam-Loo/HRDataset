#Make histogram based on ISO shutter speed data 

import os 
import sys
from PIL import Image

from PIL import Image
from PIL.ExifTags import TAGS 
from PIL import Image, ExifTags

import numpy as np; np.random.seed(19680801)
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.collections
import matplotlib.cm


def getEXIFdata (imagename):

    '''
    returns Tuple (minimum param, maximium param) for each picture 
    also prints the dictionary containing the data 
    '''
    try:
        img = Image.open(imagename)
        img_exif = img.getexif()
        #print(type(img_exif))
        # <class 'PIL.Image.Exif'>

        exifAttrs = set(["Model", "Make", "ExifImageWidth", "ExifImageHeight", "FocalLength", 'ISOSpeedRatings', "DateTime"])
        exif = {}

        if img_exif is None:
            print("Sorry, image has no exif data.")

        elif img_exif:
            img_exif_dict = dict(img_exif)
            #print(img_exif_dict)
            # { ... 42035: 'FUJIFILM', 42036: 'XF23mmF2 R WR', 42037: '75A14188' ... }
            for key, val in img_exif_dict.items():
                decodedAttr = TAGS.get(key, key)
                if decodedAttr in exifAttrs: exif[decodedAttr] = val
        
        output = {} #create a dictinoary containing relevant exif information

        if 'FocalLength' in exif: 
            #output['FocalLength'] = float(exif['FocalLength'][0])/float(exif['FocalLength'][1])
            output['FocalLength'] = exif['FocalLength']

        if ('Make' in exif):
            output['Make']=exif['Make']
        
        if ('Model' in exif):
            output['Model']=exif['Model']

        if ('DateTimeDigitized' in exif):
            output['DateTimeDigitized']=exif['DateTimeDigitized']

        if ('DateTime' in exif):
            output['DateTime']=exif['DateTime']

        if ('ISOSpeedRatings' in exif):
            output['ISOSpeedRatings']=exif['ISOSpeedRatings']


        if ('GPSInfo' in exif):
            output['GPSInfo']=exif['GPSInfo']

        return output 


   
    except ValueError as err:
        print(err)
        print("Error on image: ", imagename)
  
    except:
        pass
                
                #if key in ExifTags.TAGS:
                    #print(f"{ExifTags.TAGS[key]}:{repr(val)}")

                    # ExifVersion:b'0230'
                    # ...
                    # FocalLength:(2300, 100)
                    # ColorSpace:1
                    # FocalLengthIn35mmFilm:35
                    # ...
                    # Model:'X-T2'
                    # Make:'FUJIFILM'
                    # ...
                    # DateTime:'2019:12:01 21:30:07'
                    # ...


def polyhist(data, name,nbins=50, colors=True):
    n, bins = np.histogram(data, nbins)
    # get the corners of the rectangles for the histogram
    left = np.array(bins[:-1])
    right = np.array(bins[1:])
    bottom = np.zeros(len(left))
    top = bottom + n
    # we need a (numrects x numsides x 2) numpy array to be used as 
    # vertices for the PolyCollection
    XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

    c=None
    if colors:
        c = matplotlib.cm.RdYlBu(n/n.max())
    pc = matplotlib.collections.PolyCollection(XY, facecolors=c)

    fig, ax = plt.subplots()
    ax.add_collection(pc)

    plt.ylim(0, 10000000) #limit on resolution
    # update the view limits
    ax.set_xlim(left[0], right[-1])
    ax.set_ylim(bottom.min(), top.max())

    fig.savefig(name)

if __name__ == "__main__":
    # python isoHisto.py <fiilename>
    path =  sys.argv[1]
    data_ISO =[] #you can change this to any exif data item this code is for ISO specifically 
    

    for root, dirs, files in os.walk(path): #go through directory and sub directory 
        for file in files:
            if file.endswith( ".png" ) or file.endswith( ".jpg" ):
                try:
                    path_file = os.path.join(root,file)
                    dictOut = getEXIFdata(path_file) #get the data for that image 
                    #print(dictOut)
                    for key,value in dictOut.items():
                        if key == 'ISOSpeedRatings':
                            data_ISO.append(value)

                except:
                    pass

    polyhist(data_ISO, name="ISO_data_histogram.png",nbins=50)


#print(data_ISO)
