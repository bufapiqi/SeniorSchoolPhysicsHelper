import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint
import numpy as np
import yaml


(x_train, y_train),(x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(x_test.shape)
print(x_train)
print(y_train)
x_train = x_train.reshape(x_train.shape[0],28,28,1).astype('float32')
x_test = x_test.reshape(x_test.shape[0],28,28,1).astype('float32')
print(x_train)
x_train = x_train/255
x_test = x_test/255


# num_classes = len(np.unique(y_train))
# y_train = keras.utils.to_categorical(y_train, num_classes)
# y_test = keras.utils.to_categorical(y_test, num_classes)
#
# (x_train, x_valid) = x_train[5000:], x_train[:5000]
# (y_train, y_valid) = y_train[5000:], y_train[:5000]
#
# print('x_train shape:', x_train.shape)
#
# print(x_train.shape[0], 'train examples')
# print(x_valid.shape[0], 'valid examples')
# print(x_test.shape[0], 'test examples')
#
#
# model = Sequential()
# model.add(Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu', input_shape=(28,28,1)))
# model.add(MaxPooling2D(pool_size=2))
# model.add(Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu'))
# model.add(MaxPooling2D(pool_size=2))
# model.add(Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu'))
# model.add(MaxPooling2D(pool_size=2))
# model.add(Dropout(0.3))
# model.add(Flatten())
# model.add(Dense(500, activation='relu'))
# model.add(Dropout(0.4))
# model.add(Dense(num_classes, activation='softmax'))
#
# model.summary()
# model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#
#
# checkpoint = ModelCheckpoint(filepath='MLP.weights.best.hdf5', verbose=1, save_best_only=True)
# hist = model.fit(x_train, y_train, batch_size=32, epochs=5, validation_data=(x_valid, y_valid))
#
# # model.load_weights('MLP.weights.best.hdf5')
#
# score = model.evaluate(x_test, y_test, verbose=0)
# print('\n', 'Test accuracy:', score[1])
#
# yaml_string = model.to_yaml()
# with open('cnn.yml', 'w') as outfile:
#     outfile.write(yaml.dump(yaml_string, default_flow_style=True))
# model.save_weights('cnn.h5')







