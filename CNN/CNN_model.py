import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import numpy as np
import yaml
import cv2

def get_data(path):
    f = open(path)
    list = f.readlines()
    num_list = []
    for i in list:
        tuplestr_list = []
        tuple_list = []
        num = []
        temp = i.split('[')[1].split(']')[0]
        # print(temp)
        tuplestr_list = temp.split(',')
        # print(tuplestr_list)
        for m in range(0, len(tuplestr_list), 2):
            o1 = 0
            o2 = 0
            o1 = int(tuplestr_list[m].split('(')[1])
            o2 = int(tuplestr_list[m + 1].split(')')[0])
            num.append((o1, o2))
        num_list.append(num)
    # print(num_list[0])
    x_max = 0
    x_min = 600
    y_max = 0
    y_min = 600
    img_list = []
    for num in range(len(num_list)):
        for i in num_list[num]:
            if i[0] > x_max:
                x_max = i[0]
            if i[0] < x_min and i[0] != 0:
                x_min = i[0]
            if i[1] > y_max:
                y_max = i[1]
            if i[1] < y_min and i[1] != 0:
                y_min = i[1]
        x = x_max - x_min + 1
        y = y_max - y_min + 1
        img = np.zeros(shape=[x, y])
        # print(img.shape)
        for i in num_list[num]:
            if i[0] != 0 and i[1] != 0:
                # print(i[0])
                # print(i[1])
                # print(x_min)
                # print(y_min)
                img[i[0] - x_min, i[1] - y_min] = 255
        img1 = cv2.resize(img,(200,200))
        # print(img)
        img_list.append(img1)
    return img_list

def cnn_train(x_train,y_train,x_test,y_test):
    # (x_train, y_train),(x_test, y_test) = mnist.load_data()
    # print(x_train.shape)
    # print(x_test.shape)
    # print(x_train)
    # print(y_train)
    x_train = x_train.reshape(x_train.shape[0],200,200,1).astype('float32')
    x_test = x_test.reshape(x_test.shape[0],200,200,1).astype('float32')
    # print(x_train.shape)
    # x_train = x_train/255
    # x_test = x_test/255

    # num_classes = len(np.unique(y_train))
    y_train = keras.utils.to_categorical(y_train, num_classes = 4)
    y_test = keras.utils.to_categorical(y_test, num_classes = 4)
    #
    # (x_train, x_valid) = x_train[5000:], x_train[:5000]
    # (y_train, y_valid) = y_train[5000:], y_train[:5000]
    #
    # print('x_train shape:', x_train.shape)
    #
    # print(x_train.shape[0], 'train examples')
    # print(x_valid.shape[0], 'valid examples')
    # print(x_test.shape[0], 'test examples')


    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu', input_shape=(200,200,1)))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(filters=32, kernel_size=(3,3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(filters=64, kernel_size=(3,3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(500, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(4, activation='softmax'))

    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])


    checkpoint = ModelCheckpoint(filepath='MLP.weights.best.hdf5', verbose=1, save_best_only=True)
    hist = model.fit(x_train, y_train, batch_size=16, epochs=10, validation_data=(x_test, y_test))

    # model.load_weights('MLP.weights.best.hdf5')

    score = model.evaluate(x_test, y_test, verbose=0)
    print('\n', 'Test accuracy:', score[1])

    yaml_string = model.to_yaml()
    with open('graph.yml', 'w') as outfile:
        outfile.write(yaml.dump(yaml_string, default_flow_style=True))
    model.save_weights('graph.h5')

if __name__ == '__main__':
    data_list = np.empty([0,200,200])
    label_list = []
    arrow_list = get_data('arrow.txt')
    arc_list = get_data('arc.txt')
    line_list = get_data('line.txt')
    rectangle_list = get_data('rectangle.txt')
    for i in arrow_list:
        temp = np.append(data_list,i)
        dim = data_list.shape
        data_list = temp.reshape(dim[0] + 1,dim[1],dim[2])
        label_list.append(0)
    for i in arc_list:
        temp = np.append(data_list, i)
        dim = data_list.shape
        data_list = temp.reshape(dim[0] + 1, dim[1], dim[2])
        label_list.append(1)
    for i in line_list:
        temp = np.append(data_list, i)
        dim = data_list.shape
        data_list = temp.reshape(dim[0] + 1, dim[1], dim[2])
        label_list.append(2)
    for i in rectangle_list:
        temp = np.append(data_list, i)
        dim = data_list.shape
        data_list = temp.reshape(dim[0] + 1, dim[1], dim[2])
        label_list.append(3)
    # print(data_list)
    # data_list = np.array(data_list)
    # label_list = np.array(label_list)
    print(data_list.shape)
    # print(label_list.shape)
    x_train, x_test, y_train, y_test = train_test_split(data_list, label_list, test_size=0.1)
    cnn_train(x_train,y_train,x_test,y_test)





