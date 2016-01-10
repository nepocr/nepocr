import numpy as np
import os
import matplotlib.image as mpimg


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.144])


def loadImageFromFile(fileName):
    # print fileName;
    # toRet=[]
    img = mpimg.imread(fileName)[:30]

    # img=img.flatten()
    # print(np.shape(img))
    return img
    # gray = rgb2gray(img)

    # plt.imshow(gray, cmap = plt.get_cmap('gray'))
    # plt.show()


def getImageFromRoot(rootDir):
    dirs = [f for f in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, f))]
    X = []
    y = []
    y_indi = []

    # core_classes = max([int(core.split("_")[0]) for core in dirs]) + 1
    # attch_classes = max([int(core.split("_")[1]) for core in dirs]) + 1

    for individualDir in dirs:
        indiDirFull = os.path.join(rootDir, individualDir)
        files = [f for f in os.listdir(indiDirFull) if os.path.isfile(
            os.path.join(indiDirFull, f))]
        for indFile in files:
            if(indFile[-5:] == '.jpeg'):
                # print indFile
                X.append(loadImageFromFile(os.path.join(indiDirFull, indFile)))

                indices = individualDir.split("_")
                coreIndex = int(indices[0])
                attchIndex = int(indices[1])

                outVec = np.zeros(len(dirs))
                # print(coreIndex)
                ind3612 = 12 * coreIndex + attchIndex
                outVec[ind3612] = 1
                # outVec[coreIndex] = 1
                # outVec[core_classes + attchIndex] = 1

                # print (outVec)
                y_indi.append(ind3612)
                y.append(outVec)

    y = np.asarray(y)
    y_indi = np.asarray(y_indi)
    X = np.asarray(X)

    return y, X, y_indi
