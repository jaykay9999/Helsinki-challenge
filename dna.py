
import random
import numpy as np
import cv2



def new_weight():

    weight = random.randint(0,5)
    return weight

def new_bias():
    bias = random.randint(-10,10)
    return bias




def deblur(my_filter , my_bias , blurry_image):

    all_blurry = []
    #all_blurry.append(blurry_image1[300 : 600 , 250:2100])
    blurry_image1 = np.array(blurry_image)
    blurry_image2 = []
    x =33
    y = 33
    for i in range(len(blurry_image1)-y):
        blurry_image2x = []
        #print(str((i/(len(blurry_image1)-y))*100) +" %" )
        for j in range(len(blurry_image1[i])-x):
            all_blurry = blurry_image[i : i+y , j:j+x]
            all_blurry = np.array(all_blurry)
            all_blurry = all_blurry + np.array(my_bias)
            pixel_arr = np.multiply(all_blurry , my_filter)
            summer = sum(sum(pixel_arr))
            pixel = int(summer  / (sum(sum(my_filter))))
            blurry_image2x.append(pixel)
        blurry_image2.append(np.array(blurry_image2x))
    
    return np.array(blurry_image2)


def crop_image(x , y , image):
    d = int(x/2)
    f = int(y/2)

    b = np.array(image)
    x_axis , y_axis = b.shape

    crop_img = image[f: x_axis-f-1, d : y_axis-d-1]
    return np.array(crop_img)




def comparison(matrix1 , matrix2):
    difference = matrix1 - matrix2
    difference = np.square(difference)
    result = np.sum(difference)
    return result




class dna(object):
    def __init__(self , blurry_image , real_image):  
        self.genes = []
        self.bias = []
        self.fitness = 0
        self.blurry_image = blurry_image
        self.real_image = real_image
        for i in range (33):
            genes_x = []
            bias_x = []
            for j in range(33):
                genes_x.append(new_weight())
                bias_x.append(new_bias())
            self.genes.append(genes_x)
            self.bias.append(bias_x)
    

    def calc_fitness(self):

        fitness = 0 

        deblurred_image = deblur(np.array(self.genes) ,self.bias, self.blurry_image)
        #my_filter = np.array(self.genes)
        #my_filter_sum = np.sum(my_filter)
        #my_filter = my_filter/my_filter_sum
        #deblurred_image = cv2.filter2D(np.array(self.blurry_image) , -1 , my_filter)
        compared_real_image =  crop_image(33 , 33 , self.real_image)
        result = comparison(deblurred_image , compared_real_image)
        #print(result)
        fitness = 1 / result

        self.fitness =  fitness



    def crossover(self , partner):
        child = dna(self.blurry_image , self.real_image)
        midpoint = random.randint(1,33)
        for i in range(0 , 32):
            if(i > midpoint):
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child


    def mutate(self , mutation_rate):
        for i in range(33):
            for j in range (33):
                k = random.random()
                if(k < mutation_rate):
                    self.genes[i][j] = new_weight()

    def get_filter(self):
        return self.genes

    def get_bias(self):
        return self.bias

    def get_fitness(self):
        return self.fitness


    
#q = dna(all_blurry_train[0] , all_real_train[0] )
#q.calc_fitness()
#print(q.fitness)
#print(q.genes)
#v = dna(all_blurry_train[0] ,  all_real_train[0])
#print(v.genes)
#c = q.crossover(v)
#print(c.genes)
#c.mutate(0.5)
#print(c.genes)