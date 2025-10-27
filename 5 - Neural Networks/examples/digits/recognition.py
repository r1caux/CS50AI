"""
Load a trained handwriting.keras model and recognize digits drawn with pygame.
Press:
  - Left mouse button to draw
  - Right mouse button to clear
  - Enter/Return to predict
"""

import sys
import pygame
import numpy as np
import tensorflow as tf

# Load model
MODEL_PATH = sys.argv[1] if len(sys.argv) > 1 else "handwriting.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 280, 280
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw a digit (Enter = predict, Right-click = clear)")

# Drawing loop
drawing = True
screen.fill(WHITE)
pygame.display.update()

while drawing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False

        # Draw black circles with left mouse button
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, BLACK, pos, 12)

        # Clear with right button
        if pygame.mouse.get_pressed()[2]:
            screen.fill(WHITE)

        # Press Enter to predict
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Convert screen to 28x28 grayscale array
            raw_str = pygame.surfarray.array3d(screen)
            gray = np.dot(raw_str[..., :3], [0.2989, 0.5870, 0.1140])
            gray = np.rot90(gray, k=3)
            gray = np.fliplr(gray)
            gray = pygame.surfarray.make_surface(gray)
            img_array = pygame.surfarray.array3d(gray)
            img_array = np.dot(img_array[..., :3], [0.2989, 0.5870, 0.1140])
            img = pygame.surfarray.array3d(screen)
            img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
            img = np.rot90(img, k=3)
            img = np.fliplr(img)
            img = np.array(img, dtype="float32") / 255.0

            # Resize to 28x28 and invert colors
            img = tf.image.resize(img[..., np.newaxis], (28, 28))
            img = 1 - img  # because white background → 0

            # Predict
            pred = model.predict(img[np.newaxis, ...], verbose=0)
            digit = np.argmax(pred[0])
            print(f"🧮 Predicted digit: {digit}")

    pygame.display.update()

pygame.quit()
