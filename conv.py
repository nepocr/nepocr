import os
from imageLoad import *
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.models import model_from_json
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support


model = Sequential()

# Gloabal Vars

# input image dimensions
img_rows, img_cols = 30, 30
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
nb_pool = 2
# convolution kernel size
nb_conv = 3
# batch size
batch_size = 128


print("Initialized...")

if os.path.isfile("weights.h5"):
    print("Loading Model from Saved File...")
    model = model_from_json(open('architecture.json').read())
    model.load_weights("weights.h5")

    print("Loading Test Images...")
    y, X, y_indi = getImageFromRoot('images_test')
    X = X / 255
    X = X.reshape(X.shape[0], 1, img_rows, img_cols)
    print("X.shape:", X.shape)
    y_pred = model.predict_classes(X, batch_size=batch_size, verbose=1)
    print("Precision_recall_fscore_support: ", precision_recall_fscore_support(y_indi, y_pred, average='macro'))

    print("Building Confusion Matrix...")
    matrix = confusion_matrix(y_indi, y_pred)

    smallMatrix = np.zeros((36, 36))
    for i in range(1, 432):
        for j in range(1, 432):
            smallMatrix[i//12, j//12] = smallMatrix[i//12, j//12] + matrix[i, j]


    print("Errors: ", (y_indi != y_pred).sum(), "/", len(y_indi))
    np.savetxt("confusion_test.txt", matrix, delimiter=',')
    np.savetxt("confusion_test_small.txt", smallMatrix, delimiter=',')
    print("Done...")

else:
    print("Loading Images...")
    # loading data
    y, X, y_indi = getImageFromRoot('images')
    print("X.shape:", X.shape)

    nb_classes = y.shape[1]
    print("Total classes:", nb_classes)
    nb_epoch = 15

    # Shuffling
    perm = np.random.permutation(np.size(X, 0))

    # separation of testing and training
    ratio = 0.8
    trainPerm = ratio * np.size(X, 0)

    X_train = X[perm[:trainPerm], :]
    y_train = y[perm[:trainPerm], :]

    X_test = X[perm[trainPerm:], :]
    y_test = y[perm[trainPerm:], :]

    y_test_indi = y_indi[perm[trainPerm:]]

    # print(X_train.shape)

    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)

    print("X_train.reshape:", X_train.shape)

    X_train = X_train / 255
    X_test = X_test / 255

    print("Building Model...")

    model.add(Convolution2D(nb_filters, nb_conv, nb_conv,
                            border_mode='full',
                            input_shape=(1, img_rows, img_cols)))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adadelta')

    print("Training...")

    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              show_accuracy=True, verbose=1, validation_data=(X_test, y_test))

    print("Training Comleted...")

    print("Testing...")
    y_pred = model.predict_classes(X_test, batch_size=batch_size, verbose=1)
    print("Precision_recall_fscore_support: ", precision_recall_fscore_support(y_test_indi, y_pred, average='macro'))
    print("Building Confusion Matrix...")
    matrix = confusion_matrix(y_test_indi, y_pred)
    # print(matrix)
    np.savetxt("confusion.txt", matrix, delimiter=',')
    print("Done...")
    print("Errors: ", (y_test_indi != y_pred).sum(), "/", len(y_test_indi))

    print("Saving Model to File...")

    # Saving
    json_string = model.to_json()
    open('architecture.json', 'w').write(json_string)
    model.save_weights("weights.h5")
    print("Saved Model to File...")


# Classification
# Load Test Data From Folder

# print("Testing 'images_test' Folder...")

# # unicodes
# convUnicode = "क ख ग घ ड. च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श स ष ह क्ष त्र ज्ञ"
# unicodeSplit = convUnicode.split()

# files = [f for f in os.listdir("images_test") if os.path.isfile(os.path.join("images_test", f))]
# for indFile in files:
#     if(indFile[-5:] == '.jpeg'):
#         X_t = loadImageFromFile(os.path.join("images_test", indFile))
#         X_t = X_t.reshape(1, 1, img_rows, img_cols)
#         selIndex = model.predict_classes(X_t, batch_size=batch_size, verbose=0)[0]
#         print("Selected ", unicodeSplit[selIndex], "for", indFile.split('.')[0])
