from PIL import Image
from population import population
from dna import deblur
import random
#import numpy as np
import sys
import argparse
import os
import fnmatch
import cv2

real_image = cv2.imread(r'/home/ahmed/Downloads/Helsinki-challenge-main/focusStep_6_timesR_size_30_sample_0001.tif')

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



def draw(pop):
	k = 1
	while(k == 1):
		#natural selection to fill mating pool
		pop.natural_selection()

		#generate new population
		pop.generate()

		#calculate fitness of each individual
		pop.calc_fitness()

		#evaluate population
		pop.evaluate()

		if(pop.is_finished()):
			k = 2
		if(pop.get_generations() == 5):
			k=2

		display_info(pop)
		
		
def display_info(pop):
    answer = pop.get_best()
    print("best kernel is : ")
    print(answer.get_filter())
    print("with fitness : ")
    print(answer.get_fitness())
    print("with bias : ")
    print(answer.get_bias())
    print("total generations : ")
    print(pop.get_generations())




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
		
		popmax = 10
		mutation_rate = 0.01
		pop = population(original , real_image, popmax , mutation_rate)
		
		draw(pop)
		final_dna = pop.get.best()
		my_filter = np.array(final_dna.get_filter())
		my_bias = np.array(final_dna.get_bias())
		deblurred_image = deblur(my_filter ,my_bias, original)
		original = Image.fromarray(deblurred_image.astype('uint8'), 'L')
		#plt.imshow(deblurred_image , cmap = 'gray')
		#plt.show()
		
		
		original.save(output_folder + '/' + extract_filename[0] + '.png', format="png") #save it to the output folder

