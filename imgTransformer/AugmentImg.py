import cv2
import numpy as np
from operator import itemgetter
import random

class TransformImg():

	def __init__(self):
		pass

	def flip_horizontal(self,img):
		img = cv2.flip(img,1)
		h,w = img.shape[0],img.shape[1]
		return img

	def flip_vertical(self,img):
		img = cv2.flip(img,0)
		h,w = img.shape[0],img.shape[1]
		return img

	def translate_x(self,img,tx_range):

		tx = random.randint(tx_range[0],tx_range[1])
		M = np.float32([[1,0,tx],[0,1,0]])
		dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]))
		return dst,M

	def translate_y(self,img,ty_range):

		ty = random.randint(ty_range[0],ty_range[1])
		M = np.float32([[1,0,0],[0,1,ty]])
		dst = cv2.warpAffine(img,M,(img.shape[1],img.shape[0]))
		return dst,M

	def rotate(self,img,angle_range,centre):

		angle = random.randint(angle_range[0],angle_range[1])
		h,w = img.shape[0],img.shape[1]
		M = cv2.getRotationMatrix2D(centre,angle,1)
		dst = cv2.warpAffine(img,M,(w,h))
		return dst,M

	def shear(self,img,shear_range):
		h,w = img.shape[0],img.shape[1]
		pts1 = np.float32([[5,5],[20,5],[5,20]])
		pt1 = 5+shear_range*np.random.uniform()-shear_range/2
		pt2 = 20+shear_range*np.random.uniform()-shear_range/2
		pts2 = np.float32([[pt1,5],[pt2,pt1],[5,pt2]])
		M = cv2.getAffineTransform(pts1,pts2)
		dst = cv2.warpAffine(img,M,(w,h))

		return dst,M
