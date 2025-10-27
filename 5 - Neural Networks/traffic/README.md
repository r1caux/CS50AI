Experimentation process
I tested different versions of a convolutional neural network to classify the images. I started with a simple model that had one convolutional layer and one pooling layer. It trained quickly but gave low accuracy and struggled to recognize signs properly.

I then built a deeper model with more convolutional layers, batch normalization, and dropout. This version performed much better. Normalizing the image data also helped the model train more smoothly. I tried different numbers of filters, pool sizes, and dense layer sizes.

The best results came from using two convolutional blocks followed by one dense layer with 256 units and a dropout of 0.5. The final model trained well and reached good accuracy. Simpler models underfit, and larger ones didn t add much improvement. Overall, a balanced model with normalization and dropout worked best.