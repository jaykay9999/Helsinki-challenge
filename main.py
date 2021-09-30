from PIL import Image
#import numpy as np
import sys
import argparse
import os
import fnmatch



# take 3 arguments : input folder output folder and blur level, loop over image files in input folder and 
#copy them to output folder with .png extension


input_folder = ""
output_folder = ""
level_blur = ""

pattern = '*.tif'
n = len(sys.argv)
#if n ==3:
input_folder = str(sys.argv[1])
output_folder = str(sys.argv[2])
level_blur = int(sys.argv[3])



listOfFiles = os.listdir(input_folder)

if not os.path.exists(output_folder):
	os.makedirs(output_folder)

for filename in listOfFiles:
	# might be later a function to split :
	extract_filename = filename.split(".")
	print(extract_filename[0]) # take the filename without the .tif extension

	#ex_f = str(extract_filename[0]) # convert the previous line from type list to type string

	if fnmatch.fnmatch(filename,pattern): # we do not want to have the text files
		original = Image.open(input_folder+'/'+filename) # load image
		original.save(output_folder + '/' + extract_filename[0] + '.png', format="png") #save it to the output folder

