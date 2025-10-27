"""
Train a convolutional neural network to recognize handwritten digits
(using the MNIST dataset) and save the model as handwriting.keras
"""

import tensorflow as tf

# Load MNIST data (60 000 train + 10 000 test)
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalize and add channel dimension -> (n, 28, 28, 1)
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0
X_train = X_train[..., tf.newaxis]
X_test = X_test[..., tf.newaxis]

# Build CNN model (modern Keras 3 style)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

# Compile & train
model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1, verbose=2)

# Evaluate
model.evaluate(X_test, y_test, verbose=1)

# Save in new .keras format
model.save("handwriting.keras")

print("✅ Model saved as handwriting.keras")
