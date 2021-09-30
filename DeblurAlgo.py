import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import tensorflow as tf
from PIL import Image, ImageDraw, ImageOps
from PIL import ImageFont
from keras import models, layers
from functions import*

DATADIR = "/home/ahmed/Downloads/HDC2021_step6/step6/Times"
CATEGORIES = ["CAM01" , "CAM02"]

all_real_train = []
all_blurry_train = []
all_real_test = []
all_blurry_test = []
for category in CATEGORIES:
    path = os.path.join(DATADIR , category)
    print(len(os.listdir(path)))
    counter = 0
    division = 40
    for img in os.listdir(path):  
        if (counter < division):
            
            if(counter < 36 ):
                if(img.endswith(".tif")):
                    img_array = cv2.imread(os.path.join(path ,img), cv2.IMREAD_GRAYSCALE)
                    img_array = normalize(img_array)
                    if(category == "CAM01"):                        
                        all_real_train.append(img_array)
                    if(category == "CAM02"):
                        all_blurry_train.append(img_array)
            else:
                if(img.endswith(".tif")):
                    img_array = cv2.imread(os.path.join(path ,img), cv2.IMREAD_GRAYSCALE)
                    img_array = normalize(img_array)                    
                    if(category == "CAM01"):
                        all_real_test.append(img_array)
                    if(category == "CAM02"):
                        all_blurry_test.append(img_array)
        counter+=1
            #plt.imshow(img_array , cmap = 'gray')
            #plt.show()
            
all_real_train = np.array(all_real_train)
all_blurry_train = np.array(all_blurry_train)
all_real_test = np.array(all_real_test)
all_blurry_test = np.array(all_blurry_test)   


blur_image = []
real_image = []
for i in range(1040):
    blur_image_x = []
    real_image_x = []
    for j in range(720):
        blur_image_x.append(random.randint(0,255))
        real_image_x.append(random.randint(0,255))
    blur_image.append(blur_image_x)
    real_image.append(real_image_x)    
    
all_real_matrix = []
all_blurry_matrix = []

for i in range(len(all_blurry_train)):  
    temp_real = blurry_matrix(all_real_train[i])
    temp_blurry = blurry_matrix(all_blurry_train[i])
    for j in range(len(temp_real)):
        all_real_matrix.append(temp_real[j])
        all_blurry_matrix.append(temp_blurry[j])

all_real_matrix_test = []
all_blurry_matrix_test = []

for i in range(len(all_blurry_test)):  
    temp_real1 = blurry_matrix(all_real_test[i])
    temp_blurry1 = blurry_matrix(all_blurry_test[i])
    for j in range(len(temp_real)):
        all_real_matrix_test.append(temp_real1[j])
        all_blurry_matrix_test.append(temp_blurry1[j]    
        
        
all_real_matrix = ((np.array(all_real_matrix))/255)
all_blurry_matrix = ((np.array(all_blurry_matrix))/255)
all_real_matrix_test = ((np.array(all_real_matrix_test))/255)
all_blurry_matrix_test = ((np.array(all_blurry_matrix_test))/255) 

model = tf.keras.models.Sequential()

#encode
model.add(layers.Conv2D(64, (15, 15), strides =1, padding = 'same', input_shape = (250, 250, 1)))
model.add(layers.Conv2D(64, (1, 1), strides = 1, padding = 'same'))
model.add(layers.Conv2D(64, (1, 1), strides = 1, padding = 'same'))

#latent
#model.add(layers.Conv2D(8, (19, 19), strides = 1, padding = 'same'))
#decode
model.add(layers.Conv2D(64, (1, 1), strides = 1, padding = 'same'))
model.add(layers.Conv2D(64, (1, 1), strides = 1, padding = 'same'))
model.add(layers.Conv2D(64, (1, 1),strides = 1, padding = 'same'))
model.add(layers.Conv2D(64, (1, 1), strides = 1, activation = 'sigmoid', padding = 'same'))
model.summary()

model.compile(loss = 'mse', optimizer = 'adam')
model.fit(all_blurry_matrix.reshape(-1, 250, 250, 1) , 
all_real_matrix.reshape(-1, 250, 250, 1) , epochs =3, batch_size = 10, validation_data = (all_blurry_matrix_test.reshape(-1, 250, 250, 1) ,                    
all_real_matrix_test.reshape(-1, 250, 250, 1)))


preds = model.predict(all_blurry_matrix_test.reshape(-1, 250, 250, 1))
preds = preds.reshape(-1, 250, 250)
print(preds)

for i in range(len(preds)):
    #plt.imshow(all_blurry_matrix_test[i] , cmap = 'gray')
    #print("blurry image " + str(i))
    #plt.show()
    plt.imshow(preds[i] , cmap = 'gray')
    print("prediction " + str(i))
    plt.show()
