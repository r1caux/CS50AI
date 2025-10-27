""" Using tensorflow neural network to identify counterfeit banknotes """

import csv
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Read data in from file
with open("banknotes.csv") as f:
    reader = csv.reader(f)
    next(reader)

    data = []
    for row in reader:
        data.append({
            "evidence": [float(cell) for cell in row[:4]],
            "label": 1 if row[4] == "0" else 0
        })
# Separate data into training and testing groups
evidence = [row["evidence"] for row in data]
labels = [row["label"] for row in data]

# Convert to NumPy before fitting
evidence = np.asarray(evidence, dtype="float32")
labels = np.asarray(labels, dtype="float32").reshape(-1, 1)

X_training, X_testing, y_training, y_testing = train_test_split(
    evidence, labels, test_size=0.4
)

# Create a neural network (use explicit Input for Keras 3)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])
print("Training shape:", X_training.shape, y_training.shape)
print("Testing shape:", X_testing.shape, y_testing.shape)
# Train neural network
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
model.fit(X_training, y_training, epochs=20, verbose=1, batch_size=1)

# Evaluate how well model performs
model.evaluate(X_testing, y_testing, verbose=1, batch_size=1)
