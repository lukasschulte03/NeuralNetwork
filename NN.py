# -------------------------------------------------------------------------------------------------------------------------#
# libraries used

import pygame
import numpy as np
import tensorflow as tf
from tensorflow import keras

# -------------------------------------------------------------------------------------------------------------------------#
# loading the model to use it later

model = keras.models.load_model('num_guesser.model')

# -------------------------------------------------------------------------------------------------------------------------#
# global variables

width = 560
height = 560
rez = 20

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Number Guesser')

num_arr = np.zeros(shape=(28, 28), dtype=np.float)

# -------------------------------------------------------------------------------------------------------------------------#
# returns the arguments required to draw a rect
# at a given place


def get_rect_pos():
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    return (x - (x % rez), y - (y % rez), rez, rez)

# -------------------------------------------------------------------------------------------------------------------------#
# returns the indices of the position in the grid


def get_grid_pos():
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    return x // rez, y // rez

# -------------------------------------------------------------------------------------------------------------------------#
# drawing the grid lines


def draw_grid():
    for i in range(1, int(width / rez)):
        pygame.draw.line(display, (255, 255, 255),
                         (i * rez, 0), (i * rez, width))

    for j in range(1, int(height / rez)):
        pygame.draw.line(display, (255, 255, 255),
                         (0, j * rez), (height, j * rez))

# -------------------------------------------------------------------------------------------------------------------------#
# main loop


def main():
    run = True
    while run:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(display, (255, 255, 255), get_rect_pos())
                num_arr[get_grid_pos()[1]][get_grid_pos()[0]] = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    # reshaping the input array to get the prediction
                    num_arr.shape = (1, 784)
                    prediction = model.predict(num_arr)
                    num_guessed = list(prediction[0]).index(max(prediction[0]))
                    confidence = round(max(prediction[0]) * 100, 2)
                    print('\n')

                    print(
                        f'number guessed: {num_guessed}; confidence = {confidence}%')

                    print('\n')
                    print('----------------Stats----------------')
                    print('\n')

                    # getiing the labels and their respective confidence scores
                    for index, result in enumerate(prediction[0]):
                        print(
                            f'label {index}: % confidence = {round(result * 100, 2)}%\n')

                    print('\n')

        pygame.display.flip()


# -------------------------------------------------------------------------------------------------------------------------#
# calling the main function
if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------------------------------------------------------#