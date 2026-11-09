import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf

mnist =  tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

model = tf.keras.models.load_model("handwritten.keras")
loss, accuracy = model.evaluate(x_test, y_test)
print(loss)
print(accuracy)

digit_number = 1
while os.path.isfile(f"samples/Untitled_{digit_number}.png"):
    try:
        img = cv2.imread(f"samples/Untitled_{digit_number}.png")[:,:,0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"This digit is probably a {np.argmax(prediction)}")
        plt.imshow(img[0], cmap=plt.cm.binary)
        plt.show()
        print(img.shape)
        print(img[0].shape)
    except Exception as e:
        print(e)
    finally: 
        digit_number += 1


        