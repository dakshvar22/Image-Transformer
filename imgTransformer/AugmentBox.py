import cv2
import numpy as np

class TransformBox():
	def __init__(self):
		pass

	def getTransformedPoint(self,pt,M):
		'''
		pt - 1x2
		M  - 3x3
		dst(x,y) = src(M11 * x + M12 * y + M13 , M21 * x + M22 * y + M23)
		'''
		# return np.dot(pt,M).astype(np.int32)
		# print pt,pt.shape
		x = M[0,0] * pt[0] + M[0,1] * pt[1] + M[0,2]
		y = M[1,0] * pt[0] + M[1,1] * pt[1] + M[1,2]
		return np.array([x,y])

	def getTransformedBoxes(self,boxes,M_interest):

		boxes_trans = []
		for bb_idx in range(len(boxes)):
			bb = boxes[bb_idx]
			x1,y1,x2,y2 = bb[0],bb[1],bb[2],bb[3]
			tl = np.array([x1,y1])
			br = np.array([x2,y2])
			tr = np.array([x2,y1])
			bl = np.array([x1,y2])

			tl_trans = self.getTransformedPoint(tl,M_interest)
			# print tl,M_interest,tl_trans
			br_trans = self.getTransformedPoint(br,M_interest)
			tr_trans = self.getTransformedPoint(tr,M_interest)
			bl_trans = self.getTransformedPoint(bl,M_interest)

			# new_points = np.array([tl_trans,tr_trans,br_trans,bl_trans])
			new_points = np.float32([[tl_trans, tr_trans, br_trans, bl_trans]])
			# print new_points
			# print new_points.shape
			new_rect = cv2.boundingRect(new_points)
			# print new_rect
			new_box = [new_rect[0],new_rect[1],new_rect[0] + new_rect[2],new_rect[1] + new_rect[3]]
			# new_box = getBoundingRect(new_points)
			# print bb,new_box
			boxes_trans.append(new_box)
		return boxes_trans

	def flip_horizontal(self,boxes,w,h):
		boxes_trans = []
		for bb_idx in range(len(boxes)):
			bb = boxes[bb_idx]
			x1,y1,x2,y2 = bb[0],bb[1],bb[2],bb[3]
			x1_flip = w - x1
			x2_flip = w - x2
			boxes_trans.append([x1_flip,y1,x2_flip,y2])
		return boxes_trans

	def flip_vertical(self,boxes,w,h):
		boxes_trans = []
		for bb_idx in range(len(boxes)):
			bb = boxes[bb_idx]
			x1,y1,x2,y2 = bb[0],bb[1],bb[2],bb[3]
			y1_flip = h - y1
			y2_flip = h - y2
			boxes_trans.append([x1,y1_flip,x2,y2_flip])
		return boxes_trans