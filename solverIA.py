import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Model, Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
from tensorflow.keras.utils import to_categorical
from progress.bar import IncrementalBar

class solver_sudoku:

    def __init__(self, path ='training_2'):
        self.path = path  #path of pretrain weights
        self.solver = self.loadModel()

    def loadModel(self):
        """
        Load the model
        """
        input_shape = (9, 9, 10)

        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=input_shape))
        model.add(Dropout(0.4))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Flatten())

        grid = Input(shape=input_shape)  # inputs
        features = model(grid)  # commons features

        # define one Dense layer for each of the digit we want to predict
        digit_placeholders = [
            Dense(9, activation='softmax')(features)
            for i in range(81)
        ]

        solver = Model(grid, digit_placeholders)  # build the whole model
        solver.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        latest = tf.train.latest_checkpoint(self.path)
        solver.load_weights(latest)
        return solver

    def solve(self,grids):
        """
        Solve the sudoku
        """
        grids = grids.copy()
        size = (grids == 0).sum((1, 2)).max()
        bar = IncrementalBar('Processing', max=size)
        for _ in range((grids == 0).sum((1, 2)).max()):
            preds = np.array(self.solver.predict(to_categorical(grids)))  # get predictions
            probs = preds.max(2).T  # get highest probability for each 81 digit to predict
            values = preds.argmax(2).T + 1  # get corresponding values
            zeros = (grids == 0).reshape((grids.shape[0], 81))  # get blank positions
            for grid, prob, value, zero in zip(grids, probs, values, zeros):
                if any(zero):  # don't try to fill already completed grid
                    where = np.where(zero)[0]  # focus on blanks only
                    confidence_position = where[prob[zero].argmax()]  # best score FOR A ZERO VALUE (confident blank)
                    confidence_value = value[confidence_position]  # get corresponding value
                    grid.flat[confidence_position] = confidence_value  # fill digit inplace
            bar.next()
        bar.finish()
        return grids
