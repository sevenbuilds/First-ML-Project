import cv2
import numpy as np 
import tensorflow as tf

model = tf.keras.models.load_model("handwritten.keras")

# def predict_image(image):
#     image_array = np.frombuffer(image, dtype=np.uint8)
#     img = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

#     if img is None:
#         raise ValueError("invalid image")

#     img = cv2.resize(img, dsize=(28, 28))
#     img = 255 - img
#     img = np.expand_dims(img, axis=0)
#     cv2.imwrite("processed_image.png", img[0])
#     prediction = model.predict(img, verbose=0)
#     digit = int(np.argmax(prediction[0]))
#     accuracy = float(np.max(prediction[0]))

#     return digit, accuracy

def predict_image(image):
    image_array = np.frombuffer(image, dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Invalid Image")
    img = 255 - img
    _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    coordinates = cv2.findNonZero(img)

    if coordinates is None:
        raise ValueError("No digit detected")
    
    x, y, w, h = cv2.boundingRect(coordinates)
    digit = img[y:y+h, x:x+w]
    size = max(w, h)
    square = np.zeros((size, size), dtype=np.uint8)

    x_offset = (size - w) // 2
    y_offset = (size - h) // 2

    square[y_offset:y_offset + h, x_offset:x_offset + w] = digit
    interpolation = cv2.INTER_AREA if size > 20 else cv2.INTER_LINEAR
    digit = cv2.resize(square, (20,20), interpolation=interpolation)
    digit = cv2.GaussianBlur(digit, (3, 3), 0)
    processed = np.zeros((28, 28), dtype=np.uint8)
    processed[4:24, 4:24] = digit
    processed = np.expand_dims(processed, axis=0)
    cv2.imwrite("processed_img.png", processed[0])
    prediction = model.predict(processed, verbose=0)
    digit_number = int(np.argmax(prediction[0]))
    accuracy = float(np.max(prediction[0]))

    return digit_number, accuracy

