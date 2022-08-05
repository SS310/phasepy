"""
Summary
-------
Module on Errors

See Also
--------

"""

#********** Import major pakage or module **********
import cv2
import numpy as np

#********** Import original module **********


#********** Constant Value **********
class ValueErr():
	@staticmethod
	def check_imgsize(img_path: str, ymax: int, xmax: int) -> None:
		data: np.ndarray = cv2.imread(img_path)
		if not ((ymax == data.shape[0]) and (xmax == data.shape[1])):
			raise ValueError("Your input image size is incorrect.")

	@staticmethod
	def check_npysize(npy_path: str, ymax: int, xmax: int) -> None:
		data: np.ndarray = np.load(npy_path)
		if not ((ymax == data.shape[0]) and (xmax == data.shape[1])):
			raise ValueError("Your input image size is incorrect.")

	@staticmethod
	def check_extension(filenam: str, correct_extension: list):
		counter = 0
		file_extension = filenam.split(".")[-1]
		for ext in correct_extension:
			if ext == file_extension:
				counter = 1
		if counter == 0:
			raise ValueError("< " + file_extension + " > is incorrect. (< " + str(correct_extension) + " > is correct)")