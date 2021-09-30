import random
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import tensorflow as tf
from PIL import Image, ImageDraw, ImageOps
from PIL import ImageFont



def difference_matrix(blurry_image , real_image):
    all_differences = []
    blurry_image1 = np.array(blurry_image)
    real_image1 = np.array(real_image)
    diff_matrix = blurry_image1 - real_image1
    d1iff_matrix = -1*diff_matrix
    x =471
    y = 471
    for i in range(0,len(diff_matrix)-y, y):
        for j in range(0, len(diff_matrix[i]) - x , x):
            all_differences.append(diff_matrix[i : i+y , j:j+x])
    all_differences = np.array(all_differences)
    return all_differences 
    
def blurry_matrix(blurry_image):
    all_blurry = []
    blurry_image1 = np.array(blurry_image)
    x =250
    y = 250
    for i in range(0,len(blurry_image1)-y, int(y)):
        for j in range(0, len(blurry_image1[i]) - x , int(x)):
            all_blurry.append(blurry_image1[i : i+y , j:j+x])
    all_blurry = np.array(all_blurry)
    return all_blurry    
def comparison(matrix1 , matrix2):
    difference = matrix1 - matrix2
    difference = np.absolute(difference)
    result = np.sum(difference)
    return result
    
def deblur(blurry_image , all_blurry_matrix , all_real_matrix):
    blurry_image1 = np.array(blurry_image)
    print(blurry_image1)
    x = 28
    y = 28
    for i in range(0,len(blurry_image1)-y, y):
        for j in range(0, len(blurry_image1[i]) - x , x):
            closest = 100000000
            closest_array = []
            best_index = 0
            score = 0
            for z in range(len(all_blurry_matrix)):
                score = comparison(blurry_image1[i : i+y , j:j+x], all_blurry_matrix[z])
                if (score < closest):
                    closest = score
                    #print("new highest : ")
                    #print(closest)
                    best_index = z
                    print(best_index)
            for t in range(i , i+y):
                for k in range(j , j+x):
                    blurry_image1[t][k] = all_real_matrix[best_index][t-i][k-j]
            plt.imshow(blurry_image1 , cmap = 'gray')
            plt.show()
            
    return blurry_image1  
    
def normalize(img):
    """
    Linear histogram normalization
    """
    arr = np.array(img, dtype=float)

    arr = (arr - arr.min()) * (255 / arr[:, :50].min())
    arr[arr > 255] = 255
    arr[arr < 0] = 0

    return arr#Image.fromarray(arr.astype('uint8'), 'L')    
    






