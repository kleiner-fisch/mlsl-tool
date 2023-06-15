import math
from z3 import *


def eq(v1, v2, epsilon):
	 return math.fabs(v1 - v2) <= epsilon

def ge(v1, v2, epsilon):
	return v1 - v2 > epsilon
	
def min(a,b):
	"""returns the smaller of two elements"""
	if a < b:
		return a
	else:
		return b 
