import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf
import pathlib

from tensorflow import keras
from keras import layers
from keras.layers import Dropout
from keras.models import Sequential
import h5py
from pathlib import Path
import imghdr
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_absolute_error



data_dir = "/Users/direnceran/Desktop/Projeler/Fotograflar"




image_extensions = [".png", ".jpg", "webp"]  # add there all your images file extensions

img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png", "webp"]
for filepath in Path(data_dir).rglob("*"):
    if filepath.suffix.lower() in image_extensions:
        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")


batch_size = 32
img_height = 180
img_width = 180

train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)


plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")


for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

num_classes = len(class_names)

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, (3, 3), activation='relu', padding='same', name='block1_conv1'),
  layers.Conv2D(16, (3, 3), activation='relu', padding='same', name='block1_conv2'),
  layers.MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool'),
  layers.Conv2D(32, (3, 3), activation='relu', padding='same', name='block2_conv1'),
  layers.Conv2D(32, (3, 3), activation='relu', padding='same', name='block2_conv2'),
  layers.MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool'),
  layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='block3_conv1'),
  layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='block3_conv2'),
  layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='block3_conv3'),
  layers.MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool'),
  layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='block4_conv1'),
  layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='block4_conv2'),
  layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='block4_conv3'),
  layers.MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool'),
  layers.Flatten(),
  layers.Dense(1024, activation='relu'),
  layers.Dense(1024, activation='relu'),
  layers.Dropout(0.2),
  layers.Dense(units=21, activation='softmax'),


])



model.compile(optimizer='RMSprop',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

epochs=10
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)
model.save('final_modelsonn.h5')


acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


