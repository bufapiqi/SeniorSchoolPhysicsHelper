import yaml
from keras.models import model_from_yaml
import numpy as np
import cv2

def load_cnn_model():
    global cnn_model
    try:
        cnn_model
    except:
        print('loading cnn model......')
        with open('cnn.yml', 'r') as f:
            yaml_string = yaml.load(f)
        cnn_model = model_from_yaml(yaml_string)

        print('loading weights......')
        cnn_model.load_weights('cnn.h5')
        cnn_model.compile(loss='categorical_crossentropy',
                      optimizer='sgd', metrics=['accuracy'])
    return cnn_model

def identify():
    cnn_model = load_cnn_model()
    num = [(393, 132), (395, 130), (409, 126), (427, 126), (443, 131), (466, 144), (478, 155), (483, 160), (484, 166), (483, 177), (479, 189), (469, 205), (448, 224), (416, 236), (370, 247), (346, 250), (339, 252), (339, 252), (341, 253), (351, 255), (382, 261), (431, 275), (468, 292), (477, 302), (481, 311), (482, 320), (481, 326), (477, 334), (448, 354), (352, 390), (279, 410), (252, 415), (252, 415), (252, 415), (252, 415), (0, 0)]
    img = np.empty((600,600))
    print(img.shape)
    img[1,2] = 255
    for i in num:
        img[i[0],i[1]] = 255
        print(i[0])
        print(i[1])
    print(img)
    cv2.imshow("img",img)
    cv2.waitKey()
    # vector = cnn_model.predict(num)
    # print("vector, ",vector)

if __name__ == '__main__':
    identify()