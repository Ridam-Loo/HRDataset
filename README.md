# HRDataset

#### High Resolution Dataset, set up and relevant functions. ####

To download the images, type: $ python download-images-from-csv.py <csv_filename> <folder_name>

Assuming csv_filename has at least the following format:

Column 1: ImageID
Column 3: Original URL
Column 9: Image resolution

Additional features:

* Download images with URL code and then changed name to be imageID once fully downloaded to avoid partial downloads
* Creates a new file called “missing_files.csv” where it stores every file that was not available for download
* Creates new csv file with information for images that have been downloaded in current directory under the name ‘Downloaded_files.csv’
* Checks MD5 sum against meta data in open AI
* Download in hex-tree format (see the example)
    * Ex: if the imade ID is 9f04bfa9a7c30a8b, the path will be $ FOLDER_NAME/8b/0a/c3/a7/a9/bf/04/9f/9f04bfa9a7c30a8b/9f04bfa9a7c30a8b.jpg
