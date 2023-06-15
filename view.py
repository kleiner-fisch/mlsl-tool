from z3 import *
import car as car_
import mlsl_parser.ast_wrapper as ast_wrapper



def empty_view(cars, ego):
	"""creates an empty view with information about the given cars"""
	return View(0, -1,RealVal(0),RealVal(-1),cars, ego)
	

		
class View:
	'''
		id : object identifier
		min_lane : lane with smallest ID considered
		max_lane : lane with largeste ID considered
		min_ext : leftmost (smallest) point considered for the given lanes
		max_ext : rightmost (largest) point considered for the given lanes
		ego : car under consideration
		cars = list of cars visible in this view
		ego = the car from whose viewpoint we argue
		val: car variable valuation (as in thesis). Assumed to be empty initially (i.e. we only consider clsoed formulas)
	'''
	
	def __init__(self, min_lane, max_lane, min_ext, max_ext, cars, ego):
		"""creates an instance of this class. The lane values are assumed to be z3 objects."""
		self.min_lane = min_lane
		self.max_lane = max_lane
		self.min_ext = min_ext
		self.max_ext = max_ext
		self.cars = cars
		self.ego = ego
		self.val = dict({self.ego.id : self.ego })


	@classmethod
	def ast_to_view(self, ast):
		"""takes the ast of a model and creates a view-object from it"""
		ast = ast.children
		min_ext = ast[0].children[0].children[0]
		max_ext = ast[0].children[1].children[0]
		min_lane = ast[1].children[0].children[0]
		max_lane = ast[1].children[1].children[0]
		
		ilane, ipos, ilength, iname = (0,1,2,3)
		cars = dict()
		for i in range(3, len(ast)):
			cnode = ast[i]
			lane, pos, length, name = [cnode.children[k].children[0] for k in range(4) ] 
			car = cars.get(name)
			if not car:
				if cnode.type == 'Re_Expr':
					car = car_.Car(name, pos, length, [lane])
				elif cnode.type == 'Cl_Expr':
					car = car_.Car(name, pos, length, [], lane)
				else:
					raise ValueError('Unexpected type: '+ cnode.type)
			else:
				if cnode.type == 'Re_Expr':
					car.res.append(lane)
				elif cnode.type == 'Cl_Expr':
					car.clm = lane
				else:
					raise ValueError('Unexpected type: '+ cnode.type)
			cars[name] = car
		
		cars = cars
		ego_name = ast[2].children[0].children[0]
		ego = cars[ego_name]
		return View(min_lane, max_lane, min_ext, max_ext, cars, ego)		
	
	def get_car_from_ast(self, ast):
		'''For ast representing a variable name (root label is NAME or EGO) 
		returns the car-object represented by the variable name'''
		if ast.type == ast_wrapper.NAME:
			varname = ast.children[0]
			return self.val[varname]
		elif ast.type == ast_wrapper.EGO:
			return self.ego
		else:
			raise ValueError('Enexpected input: ' + str(ast))

	def length(self):
		"""returns the extension of this view. A view with extension 0 may include a point intervall."""
		return self.max_ext - self.min_ext
		
	def height (self):
		"""returns the number of lanes within this view. 
		A view with one lane has a height of 1."""
		return self.max_lane + 1- self.min_lane
		
	def is_empty(self):
		"""returns true if one of the extensions is None or 
		the max. extension is larger than the min. extension"""
		return Or(self.width() < 0, self.height() <= 0)

	def __repr__(self):
		return ('ext=[' + str(self.min_ext) +',' + str(self.max_ext)+'], ' +
				'lanes=[' + str(self.min_lane) +',' + str(self.max_lane)+'], ' +
				'ego=' + self.ego.id + '\n' + str(self.cars.values()) )
					
	def restrict_to_right(self, v):
		result = self.copy()
		result.min_ext = v		
		return result
		
	def restrict_to_left(self, v):
		result = self.copy()
		result.max_ext = v
		return result

	def restrict_to_bottom(self, v):
		result = self.copy()
		result.max_lane = v
		return result

	def restrict_to_top(self, v):
		result = self.copy()
		result.min_lane = v
		return result

	def update_val(self, n, c):
		'''returns a view where the name n points to the car c'''
		result = self.copy()
		result.val[n] = c
		return result

	def copy(self):
		"""creates a dep copy of this object"""
		result = View(self.min_lane, self.max_lane, self.min_ext, self.max_ext,
				self.cars, self.ego)
		result.val = self.val.copy()
		return result
		
#_EMPTY_VIEW__ = View(IntVal(0),IntVal(-1),RealVal(0),RealVal(-1),None,None)
