import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf


mnist =  tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# training the model.

# model = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(28, 28, 1)),
#     tf.keras.layers.Rescaling(1/255),
#     tf.keras.layers.RandomTranslation(0.1, 0.1),
#     tf.keras.layers.RandomRotation(0.08),
#     tf.keras.layers.RandomZoom(0.1),
#     tf.keras.layers.Conv2D(32, 3, activation="relu"),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Conv2D(64, 3, activation="relu"),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dropout(0.3),
#     tf.keras.layers.Dense(128, activation="relu"),
#     tf.keras.layers.Dense(10, activation="softmax"),
# ])

# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# model.fit(x_train, y_train, epochs=10 ,validation_data=(x_test, y_test))
# model.save("handwritten.keras")

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

