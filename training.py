import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

MNIST = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = MNIST.load_data()

x_train = x_train.reshape(-1, 20, 20, 1)
x_test = x_test.reshape(-1, 20, 20, 1)

# training the model.

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Rescaling(1/255),
    tf.keras.layers.RandomTranslation(0.1, 0.1),
    tf.keras.layers.RandomRotation(0.08),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax"),
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=10 ,validation_data=(x_test, y_test))
model.save("handwritten.keras") 

model.complie(optimizer = "adam", loss="sparse_categorical_croseentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))
model.save("digits.keras")

model = tf.keras.models.load_model("handwritten.keras")
loss, accuracy = model.evaluate(x_test, y_test)
print(loss)
print(accuracy)