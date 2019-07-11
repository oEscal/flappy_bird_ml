import numpy as np
from utils import sigmoid


class IntelligentBird:
	def __init__(self, window_width, window_height):
		self.first_connection_col = np.random.rand(2, 1)

		self.window_width = window_width
		self.window_height = window_height

		# for the genetic algorithm
		self.punctuation = 0

	def set_connection_col(self, vector):
		self.first_connection_col = np.array(vector)

	def decision(self, vertical_dist, horizontal_dist):
		input = np.array([
			sigmoid(vertical_dist/self.window_height),
			sigmoid(horizontal_dist/self.window_width)
		])

		return np.matmul(input, self.first_connection_col)[0] > 0.5

	def set_punctuation(self, punt):
		self.punctuation = punt
