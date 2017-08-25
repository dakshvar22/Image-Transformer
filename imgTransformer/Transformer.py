from AugmentImg import TransformImg
from AugmentBox import TransformBox
import random

class Transformer():
	def __init__(self,transform_boxes = False):
		self.transform_boxes = transform_boxes
		self.img_transformer = TransformImg()
		self.transform_boxes = transform_boxes
		if self.transform_boxes:
			self.box_transformer = TransformBox()
		self.transforms = 5

	def set_params(self, tx_range, ty_range, rot_angle_range, shear_range):
		self.tx_range = tx_range
		self.ty_range = ty_range
		self.rot_angle_range = rot_angle_range
		self.shear_range = shear_range


	def callTransform(self,img,idx,boxes=None):
		if self.transform_boxes:
			if boxes == None:
				print 'Boxes not supplied'
		img_clone = img.copy()
		h,w = img.shape[0],img.shape[1]

		if idx == 0:
			'''
			Flip Horizontal
			'''
			img_clone = self.img_transformer.flip_horizontal(img_clone)

			if self.transform_boxes:
				boxes = self.box_transformer.flip_horizontal(boxes,w,h)

		elif idx == 1:
			'''
			Flip Vertical
			'''
			img_clone = self.img_transformer.flip_vertical(img_clone)

			if self.transform_boxes:
				boxes = self.box_transformer.flip_vertical(boxes,w,h)

		elif idx == 2:
			'''
			Translate in x
			'''
			img_clone, M_tx = self.img_transformer.translate_x(img_clone,self.tx_range)

			if self.transform_boxes:
				boxes = self.box_transformer.getTransformedBoxes(boxes,M_tx)

		elif idx == 3:
			'''
			Translate in y
			'''
			img_clone, M_ty = self.img_transformer.translate_y(img_clone,self.ty_range)

			if self.transform_boxes:
				boxes = self.box_transformer.getTransformedBoxes(boxes,M_ty)

		elif idx == 4:
			'''
			Rotate
			'''
			center_points = [(0,0),(w/2,h/2)]
			center_idx = random.randint(0,1)

			img_clone, M_rot = self.img_transformer.rotate(img_clone,self.rot_angle_range,center_points[center_idx])
			if self.transform_boxes:
				boxes = self.box_transformer.getTransformedBoxes(boxes,M_rot)

		elif idx == 5:
			'''
			Shear
			'''
			img_clone, M_shear = self.img_transformer.shear(img_clone,self.shear_range)
			if self.transform_boxes:
				boxes = self.box_transformer.getTransformedBoxes(boxes,M_shear)

		return img_clone,boxes

	def applyTransforms(self,img,boxes=None,num_transforms=2):
		img_clone = img.copy()
		# boxes_clone = boxes.copy()

		for transform_idx in range(num_transforms):
			idx = random.randint(0,self.transforms)
			img_clone,boxes = self.callTransform(img_clone,idx,boxes)
		if boxes == None:
			return img_clone
		else:
			return img_clone,boxes
