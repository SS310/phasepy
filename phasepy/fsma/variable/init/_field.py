"""
Summary
-------

See Also
--------

"""

#********** Import major pakage or module **********
import numpy as np
import cv2

#********** Import orizinal module **********
from phasepy.fsma.variable.define._var import SimuVal, CellVal
from phasepy.fsma.variable.define._path import PathVal
from phasepy._const import MathConst
from phasepy._error import ValueErr

#********** Constant Value **********

class InitField():
	class Phase():
		@staticmethod
		def toward_center(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
			if path_val.phase_path == None:
				# Create random metal structure
				_Phase.rand(simu_val=simu_val, cell_val=cell_val)
				print("Random metal structure variable were successfully created. -> ", end="")
			else:
				# Extension of input file
				extension = path_val.magne_path.split(".")[-1]
				if extension == "png":
					# Create metal structure according to input file
					_Phase.input_img(path_val=path_val, simu_val=simu_val, cell_val=cell_val)
				elif extension == "npy":
					# Create metal structure according to input file
					_Phase.input_arr(path_val=path_val, simu_val=simu_val, cell_val=cell_val)
				else:
					raise ValueError("You can use only <png, npy> as input file.")

				print("Metal structure variable were successfully created according to < " + path_val.magne_path + " >.")

	class Magne():
		@staticmethod
		def toward_center(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
			if path_val.phase_path == None:
				# Create random magnetic moment
				_Magne.rand(simu_val=simu_val, cell_val=cell_val)
				print("Random magnetic moment variable were successfully created. -> ", end="")
			else:
				# Extension of input file
				extension = path_val.magne_path.split(".")[-1]
				if extension == "png":
					# Create magnetic moment according to input file
					_Magne.input_img(path_val=path_val, simu_val=simu_val, cell_val=cell_val)
				elif extension == "npy":
					# Create magnetic moment according to input file
					_Magne.input_arr(path_val=path_val, simu_val=simu_val, cell_val=cell_val)
				else:
					raise ValueError("You can use only <png, npy> as input file.")

				# Normalize random magnetic moment
				_Magne.norm(path_val=path_val, simu_val=simu_val, cell_val=cell_val)
				print("magnetic moment variable were successfully created according to < " + path_val.magne_path + " >.")

		


#********** Internal function **********

class _Phase():
	@staticmethod
	def rand(simu_val: SimuVal, cell_val: CellVal) -> None:
		for x in range(simu_val.xmax):
			for y in range(simu_val.ymax):
				# Set random value (0~1)
				cell_val.phase_f[x,y,0] = np.random.rand()
				cell_val.phase_f[x,y,1] = 1.0 - cell_val.phase_f[x,y,0]

	@staticmethod
	def input_img(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
		# Check input file size
		ValueErr.check_imgsize(img_path=path_val.phase_path, xmax=simu_val.xmax, ymax=simu_val.ymax)
		# Input file
		field = cv2.imread(path_val.phase_path)[:,:,0:2]
		# Change 0~255 to 0~1
		cell_val.phase_f = (field/MathConst.WHITE_NUM)

	@staticmethod
	def input_arr(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
		# Check input file size
		ValueErr.check_npysize(img_path=path_val.phase_path, xmax=simu_val.xmax, ymax=simu_val.ymax)
		# Input file
		cell_val.phase_f = np.load(path_val.phase_path)

class _Magne():
	@staticmethod
	def rand(simu_val: SimuVal, cell_val: CellVal) -> None:
		for x in range(simu_val.xmax):
			for y in range(simu_val.ymax):
				# Set random value (-1~1)
				cell_val.magne_f[x,y,0] = 1.0 - 2.0*np.random.rand()
				cell_val.magne_f[x,y,1] = 1.0 - 2.0*np.random.rand()
				cell_val.magne_f[x,y,2] = 1.0 - 2.0*np.random.rand()

	@staticmethod
	def input_img(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
		# Check input file size
		ValueErr.check_imgsize(img_path=path_val.magne_path, xmax=simu_val.xmax, ymax=simu_val.ymax)
		# Input file
		field = cv2.imread(path_val.magne_path)
		# Change 0~255 to -1~1
		cell_val.magne_f = (2.0*field/MathConst.WHITE_NUM) - 1.0

	@staticmethod
	def input_arr(path_val: PathVal, simu_val: SimuVal, cell_val: CellVal) -> None:
		# Check input file size
		ValueErr.check_npysize(img_path=path_val.magne_path, xmax=simu_val.xmax, ymax=simu_val.ymax)
		# Input file
		cell_val.magne_f = np.load(path_val.magne_path)

	@staticmethod
	def norm(simu_val: SimuVal, cell_val: CellVal) -> None:
		m_length: float
		for x in range(simu_val.xmax):
			for y in range(simu_val.ymax):
				# Length of each magnetic moment
				m_length = (cell_val.magne_f[x,y,0]**2
							+cell_val.magne_f[x,y,1]**2+cell_val.magne_f[x,y,2]**2)**0.5

				# To avoid division by zero
				if m_length == 0:
					cell_val.magne_f[x,y,0] = 1.0/3.0
					cell_val.magne_f[x,y,1] = 1.0/3.0
					cell_val.magne_f[x,y,2] = 1.0/3.0
				# Normalization
				else:
					cell_val.magne_f[x,y,0] = cell_val.magne_f[x,y,0]/m_length
					cell_val.magne_f[x,y,1] = cell_val.magne_f[x,y,1]/m_length
					cell_val.magne_f[x,y,2] = cell_val.magne_f[x,y,2]/m_length
