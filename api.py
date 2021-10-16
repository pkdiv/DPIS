import os
import cv2
import math
import config
import operator
import argparse
import numpy as np
import tensorflow as tf
from neural_nets.neural_net_classification import NeuralNet_Classification


class Api:
    def __init__(self):
        p=''
        self.CATEGORIES = ['A', 'L', 'R', 'T', 'W']
        self.checkpoint_dir = os.path.join(config.datadir, 'models')
        self.HEIGHT = 512
        self.WIDTH = 512
        self.nn = NeuralNet_Classification(self.HEIGHT, self.WIDTH, len(self.CATEGORIES))
        self.latest = tf.train.latest_checkpoint(os.path.join(config.datadir, 'models'))
        self.nn.load_weights(self.latest)

    def call(self, file):
        image = self._get_file(file)
        output = self._get_model_output(image)
        name, extension = file.split('.')
        save_path = name+'.'+extension
        return output

    def _get_model_output(self, image):
        prediction = self.nn.predict(image)
        p = max(enumerate(prediction), key=operator.itemgetter(1))
        return self.CATEGORIES[p[0]]

    def _get_file(self, file_name):
        img_array = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
        return img_array
