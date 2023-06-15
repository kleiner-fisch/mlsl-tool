import util
from z3 import *
 
class Car:
	'''	
		id : object identifier
		pos : value indicating the cars position (real)
		clm : integer that defines the lane on which the car has a claim.
			If no claim, then None (Int)
		res : List of lanes this car has reservations on (Int)
		size : defines the size of this car (real)
	'''
	
	def __init__(self, id, pos, size, res, clm=None):
		self.id = id
		self.pos = pos
		self.clm = clm
		self.res = res
		self.size = size
		
	def fills_view(self, view):
		"""returns an expression that determines whether this car fills the extension of the given view.
		This is used to determine whether res(this) or clm(this) holds"""
		return And(self.pos <= view.min_ext, self.pos + self.size >= view.max_ext)

	def intersection_greater_zero(self, (l0, r0), (l1, r1)):
		'''returns two intervals have a nonzero overlap'''
		return And(l0 < r1, l1 < r0)

	def outside_view(self, view):
		"""checks if a claim or reservation of this car overlaps with the given view"""
		ival1 = (self.pos, self.pos + self.size)
		ival2 = (view.min_ext, view.max_ext)
		ext_overlaps = self.intersection_greater_zero(ival1, ival2)
		if self.clm:
			lanes = self.res + [self.clm]
		else:
			lanes = self.res
		lanes_overlap = Or([And(view.min_lane <= l, l <= view.max_lane) for l in lanes])
		return Or(Not(ext_overlaps), Not(lanes_overlap))

				
	def __repr__(self):
		result = ("id = " + str(self.id) + ", " +
				"pos = " + str(self.pos) + ", " +
				"res = " + str(self.res) + ", " +
				"size = " + str(self.size))
		if not (self.clm is None):
			result += ", clm = " + str(self.clm) + "\n"
		else:
			result += "\n"
		return result

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.id == other.id
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)