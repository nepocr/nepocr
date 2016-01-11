'''
imageLoad.py

Usage: For loading images from the directory and the subdirectories within the directory. For training, 
each directory within the root directory acts as a class.
Thus,
Folder_Name -> Label for training data in the format [coreIndex_AttachmentIndex]

Files inside Folder_Name -> Training data

'''

import numpy as np
import os
import matplotlib.image as mpimg

#Convert to grayscale using the dot product method. The grayscale vector [0.299,0.587,0.144] are computed values
def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])

#Use Matplotlib to read the image and slice to first thirty values. Returns numpy array
def loadImageFromFile(fileName):
    img = mpimg.imread(fileName)[:30]
    return img

#Go inside the rootDir and extract folder name as the label and files inside the folder as training set
def getImageFromRoot(rootDir):
    #get list of dirs in rootDirs for getting the label
    dirs = [f for f in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, f))]
    
    #some inits X->training data, y-> labels, y_indi -> indices for labels
    X = [] 
    y = []
    y_indi = []

    for individualDir in dirs:
        indiDirFull = os.path.join(rootDir, individualDir)
        files = [f for f in os.listdir(indiDirFull) if os.path.isfile(
            os.path.join(indiDirFull, f))]
            
        #only work with .jpeg files
        for indFile in files:
            if(indFile[-5:] == '.jpeg'):
                
                X.append(loadImageFromFile(os.path.join(indiDirFull, indFile)))

                indices = individualDir.split("_")
                coreIndex = int(indices[0])
                attchIndex = int(indices[1])

                outVec = np.zeros(len(dirs))

                ind3612 = 12 * coreIndex + attchIndex
                outVec[ind3612] = 1

                y_indi.append(ind3612)
                y.append(outVec)

    y = np.asarray(y)
    y_indi = np.asarray(y_indi)
    X = np.asarray(X)

    return y, X, y_indi
