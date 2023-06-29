# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import numpy as np
import pandas as pd
import pathlib
import imageio
import time

start_time = time.time()

# Exploring dataset
base_dir = "C:\\Neha\\kaggle Projects\\Medical Image Classification\\chest_xray\\"

train_pneumonia_dir = base_dir+'train/PNEUMONIA/'
train_normal_dir=base_dir+'train/NORMAL/'

test_pneumonia_dir = base_dir+'test/PNEUMONIA/'
test_normal_dir = base_dir+'test/NORMAL/'

val_normal_dir= base_dir+'val/NORMAL/'
val_pnrumonia_dir= base_dir+'val/PNEUMONIA/'

train_pn = [train_pneumonia_dir+"{}".format(i) for i in os.listdir(train_pneumonia_dir) ]
train_normal = [train_normal_dir+"{}".format(i) for i in os.listdir(train_normal_dir) ]

test_normal = [test_normal_dir+"{}".format(i) for i in os.listdir(test_normal_dir)]
test_pn = [test_pneumonia_dir+"{}".format(i) for i in os.listdir(test_pneumonia_dir)]

val_pn= [val_pnrumonia_dir+"{}".format(i) for i in os.listdir(val_pnrumonia_dir) ]
val_normal= [val_normal_dir+"{}".format(i) for i in os.listdir(val_normal_dir) ]

print ("Total images:",len(train_pn+train_normal+test_normal+test_pn+val_pn+val_normal))
print ("Total pneumonia images:",len(train_pn+test_pn+val_pn))
print ("Total Nomral images:",len(train_normal+test_normal+val_normal))

##############################
# Dataset Splitting (train 80% , test 15% and validation 5% )

# Gathering all pneumina and normal chest X-ray in two python list
pn = train_pn + test_pn + val_pn
normal = train_normal + test_normal + val_normal

# Spliting dataset in train set,test set and validation set.

train_imgs = pn[:3418]+ normal[:1224]  # 80% of 4273 Pneumonia and normal chest X-ray are 3418 and 1224 respectively.
test_imgs = pn[3418:4059]+ normal[1224:1502]
val_imgs = pn[4059:] + normal[1502:]

print("Total Train Images %s containing %s pneumonia and %s normal images"
      % (len(train_imgs),len(pn[:3418]),len(normal[:1224])))
print("Total Test Images %s containing %s pneumonia and %s normal images"
      % (len(test_imgs),len(pn[3418:4059]),len(normal[1224:1502])))
print("Total validation Images %s containing %s pneumonia and %s normal images"
      % (len(val_imgs),len(pn[4059:]),len(normal[1502:])))



import random

random.shuffle(train_imgs)
random.shuffle(test_imgs)
random.shuffle(val_imgs)

print(test_imgs[5])

import cv2

img_size = 224


def preprocess_image(image_list):
    X = []  # images
    y = []  # labels (0 for Normal or 1 for Pneumonia)
    count = 0

    for image in image_list:

        try:

            img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

            img = cv2.resize(img, (img_size, img_size), interpolation=cv2.INTER_CUBIC)

            # convert image to 2D to 3D
            img = np.dstack([img, img, img])

            # convrt greyscale image to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Normalalize Image
            img = img.astype(np.float32) / 255.

            count = count + 1

            X.append(img)


        except:
            continue
        # get the labels
        if 'NORMAL' in image:
            y.append(0)

        elif 'IM' in image:
            y.append(0)

        elif 'virus' or 'bacteria' in image:
            y.append(1)

    return X, y


X, y = preprocess_image(train_imgs)

# Check all the images getting labels or not
arr = y
uniqueValues, occurCount = np.unique(arr, return_counts=True)

print("Unique Values : ", uniqueValues)
print("Occurrence Count : ", occurCount)

# Display some images from train set
# Feel free to show more image by changing the values

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20, 5))
k = 1
for i in range(4):
    a = fig.add_subplot(1, 4, k)
    if (y[i] == 0):
        a.set_title('Normal')
    else:
        a.set_title('Pneumonia')

    plt.imshow(X[i])
    k = k + 1;

# get the labels for test set

P, t = preprocess_image(test_imgs)

arr = t
uniqueValues, occurCount = np.unique(arr, return_counts=True)

print("Unique Values : ", uniqueValues)
print("Occurrence Count : ", occurCount)

# now displaying some images from test set
# Feel free to show more image by changing the values

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20, 5))
k = 1
for i in range(4):
    a = fig.add_subplot(1, 4, k)
    if (t[i] == 0):
        a.set_title('Normal')
    else:
        a.set_title('Pneumonia')

    plt.imshow(P[i])
    k = k + 1;

# get the labels for validation set

K, m = preprocess_image(val_imgs)

arr = m

# Get a tuple of unique values & their frequency in numpy array
uniqueValues, occurCount = np.unique(arr, return_counts=True)

print("Unique Values : ", uniqueValues)
print("Occurrence Count : ", occurCount)

# now displaying some images from validation set
# Feel free to show more image by changing the values

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20, 5))
k = 1
for i in range(4):
    a = fig.add_subplot(1, 4, k)
    if (m[i] == 0):
        a.set_title('Normal')
    else:
        a.set_title('Pneumonia')

    plt.imshow(K[i])
    k = k + 1;

# get the labels for validation set

K, m = preprocess_image(val_imgs)

arr = m

# Get a tuple of unique values & their frequency in numpy array
uniqueValues, occurCount = np.unique(arr, return_counts=True)

print("Unique Values : ", uniqueValues)
print("Occurrence Count : ", occurCount)

import seaborn as sns


df=pd.DataFrame()
df['Train']=y
df['Test']=pd.Series(t)
df['Val']=pd.Series(m)



fig, ax =plt.subplots(1,3,figsize=(15,7))
sns.countplot(df['Train'], ax=ax[0])
ax[0].set(ylim=(0, 3500))


sns.countplot(df['Test'], ax=ax[1])
ax[1].set(ylim=(0, 3500))

sns.countplot(df['Val'], ax=ax[2])
ax[2].set(ylim=(0, 3500))

fig.show()


# image imbalance

from sklearn.utils import class_weight


class_weights = class_weight.compute_class_weight(class_weight ='balanced', classes = np.unique(y), y =y)# here, y contains train set label

class_weights = dict(enumerate(class_weights))
print(class_weights)

import seaborn as sns
import gc

train_imgs = train_pn[:3875]+ train_normal[:1341]
del train_imgs
gc.collect()

X_train = np.array(X)
y_train = np.array(y)
X_test = np.array(P)
y_test = np.array(t)
X_val = np.array(K)
y_val = np.array(m)

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)
print(X_val.shape)
print(y_val.shape)

# clear memory
del X
del y
gc.collect()

#get the length of the train and validation data
ntrain = len(X_train)
nval = len(X_val)

batch_size = 32

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rotation_range=7,
                                   width_shift_range=0.05,
                                   height_shift_range=0.05,
                                   shear_range=0.2,
                                   zoom_range=0.45,
                                   horizontal_flip=True)

val_datagen = ImageDataGenerator(zoom_range=0.45)

#Create the image generators
train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)

# Set image Size
img_size =224

from keras import layers
from keras import models
from keras import optimizers
from keras.applications import *
from keras.layers import Dense, GlobalAveragePooling2D
## from keras.preprocessing.image import img_to_array, load_img
#from tensorflow.keras.utils import img_to_array

from keras.models import Model
from keras import backend as K

# Create the base pre-trained model
# Weights should be none becuase we don't need to train with any pre-trained weights here

base_model = MobileNet(weights=None, include_top=False,input_shape=(img_size, img_size, 3))

x = base_model.output

# Add a global spatial average pooling layer
x = GlobalAveragePooling2D()(x)

# Add a logistic layer
predictions = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=predictions)
# Compile model
model.compile(optimizer='adam', loss = 'binary_crossentropy',
                           metrics = ['binary_accuracy', 'mae'])


# We train for 64 epochs
history = model.fit_generator(train_generator,
                              steps_per_epoch=ntrain // batch_size,
                              epochs=64,
                              validation_data=val_generator,
                              validation_steps=nval // batch_size,
                              class_weight =class_weights,
)

# Lets plot the train and val curve
# Get the details form the history object
acc = history.history['binary_accuracy']
val_acc = history.history['val_binary_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

#Train and validation accuracy
plt.plot(epochs, acc, 'b', label='Training accurarcy')
plt.plot(epochs, val_acc, 'r', label='Validation accurarcy')
plt.title('Training and Validation accurarcy')
plt.legend()

plt.figure()
#Train and validation loss
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()

plt.show()

from sklearn.metrics import accuracy_score, confusion_matrix

preds = model.predict(X_test)

acc = accuracy_score(y_test, np.round(preds))*100
cm = confusion_matrix(y_test, np.round(preds))

tn, fp, fn, tp = cm.ravel()

print('CONFUSION MATRIX ------------------')
print(cm)

print('\n============TEST METRICS=============')
precision = tp/(tp+fp)*100
recall = tp/(tp+fn)*100
print('Accuracy: {}%'.format(acc))
print('Precision: {}%'.format(precision))
print('Recall: {}%'.format(recall))
print('F1-score: {}'.format(2*precision*recall/(precision+recall)))

print('\nTRAIN METRIC ----------------------')
print('Train acc: {}'.format(np.round((history.history['binary_accuracy'][-1])*100, 2)))

import seaborn as sns
sns.heatmap(cm, annot=True, fmt="d",)

from sklearn.metrics import roc_curve,roc_auc_score
from sklearn.metrics import auc

fpr , tpr , thresholds = roc_curve ( y_test , preds)
auc_keras = auc(fpr, tpr)
print("AUC Score:",auc_keras)
plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % auc_keras)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

end_time = time.time()

total_time = end_time - start_time
print("total_time: ",total_time)



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
