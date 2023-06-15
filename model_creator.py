import car, view
from z3 import *
import mlsl_parser.model_parser_wrapper as model_parser_wrapper

class ModelCreator:
	'''has functions to create some models for test purposes'''

	def load_model(self, rel_file_path):
		f = open(rel_file_path, "r")
		# we do not allow files that are very large. Currently limit is set to 1MB
		return f.read(1000000)

	def create_model1(self, names):
		"""creates a view that is filled by a reservation"""
		car1 = car.Car(names[0],1,2,[0])
		v = view.View(0, 0 ,RealVal(1),RealVal(2),{names[0] : car1},car1)
		return v
			
	def create_model2(self, names):
		"""creates a view, that starts with an empty road and finishes with a reservation"""
		car1 = car.Car(names[0],1,2,[0])
		v = view.View(0, 0, RealVal(0),RealVal(2),{names[0] : car1},car1)
		return v

	def create_model3(self, names):
		"""creates a view, that starts with an empty road, continues with a reservation and finishes a free road"""
		car1 = car.Car(names[0],1,2,[0])
		v = view.View(0, 0,RealVal(0),RealVal(5),{names[0] : car1},car1)
		return v
		
	def create_model4(self, names):
		"""creates a view with a free road"""
		car1 = car.Car(names[0],1,2,[])
		v = view.View(0, 0,RealVal(0),RealVal(5),{names[0] : car1},car1)
		return v
		
	def create_model5(self, names):
		"""creates a view with 3 lanes and a reservation somewhere on the middle lane"""
		car1 = car.Car(names[0],2,1,[1])
		v = view.View(0, 2,RealVal(0),RealVal(5),{names[0] : car1},car1)
		return v
		
	def create_view_crash1(self, names):
		"""creates a view filled by two reservatoins exactly at the same area"""
		car1 = car.Car(names[0],0,1,[0])
		car2 = car.Car(names[1],0,1,[0])
		v = view.View(0, 0,RealVal(0),RealVal(1),{names[0] : car1, names[1] : car2},car1)
		return v

	def create_view_crash2(self, names):
		"""creates a view that contains two overlapping reservatoins"""
		car1 = car.Car(names[0],0,2,[0])
		car2 = car.Car(names[1],1,2,[0])
		v = view.View(0, 2,RealVal(0),RealVal(4),{names[0]: car1, names[1] : car2},car1)
		return v
		
	def create_model6(self, names):
		"""creates a view with two reservations"""
		car1 = car.Car(names[0],2,1,[0])
		car2 = car.Car(names[1],0,2,[2])
		v = view.View(0, 2,RealVal(0),RealVal(5),{names[0]:car1, names[1]:car2},car1)
		return v
		
	def create_model7(self, names):
		"""creates a view that is filled by a reservation, and which contains another car without a resrvation"""
		car1 = car.Car(names[0],1,2,[0])
		car2 = car.Car(names[1],10,20,[])
		v = view.View(0, 0 ,RealVal(1),RealVal(2),{names[0] : car1, names[1]:car2},car1)		
		return v
		
	def create_model8(self, names):
		"""creates a view somewhere contains a reservation"""
		car1 = car.Car(names[0],1,2,[1])
		v = view.View(0, 2 ,RealVal(1),RealVal(2),{names[0] : car1},car1)		
		return v	

	def create_empty_model(self, names):
		"""creates an empty view"""
		car1 = car.Car(names[0],2,1,[])
		return view.View(0, -1,RealVal(0),RealVal(-5),
				{names[0]: car1}, car1)
				
	def sat_big_model(self):
		"""Creates a larger model that does not violate any sanity conditions"""
		m = self.load_model('test_models/model_sat')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def unsat_big_model1(self):
		"""Creates a larger model where a car has a claim and a res on the same lane"""
		m = self.load_model('test_models/model1')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v
		
	def unsat_big_model2(self):
		"""Creates a larger model where a car has 3 reservations o ndifferent lanes"""
		m = self.load_model('test_models/model2')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def unsat_big_model4(self):
		"""Creates a larger model where a car has a claim and two res"""
		m = self.load_model('test_models/model4')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def unsat_big_model5(self):
		"""Creates a larger model where there is a lane between a res and a clm of a car"""	
		m = self.load_model('test_models/model5')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def unsat_big_model6(self):
		"""Creates a larger model where there is a lane between two reserved lanes"""
		m = self.load_model('test_models/model6')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def small_model1(self):
		m = self.load_model('test_models/model7')
		ast = self.parser_wrapper.parse(m)
		v= view.View.ast_to_view(ast)
		return v

	def __init__(self):
		self.parser_wrapper = model_parser_wrapper.ModelParserWrapper() 
	
#def big_model1(names):
	#"""creates an empty view"""
	#carA = car.Car(names[0],2,1,[2],1)
	#carB = car.Car(names[1],3,2,[2])
	#carC = car.Car(names[2],4,2,[2])
	#return view.View(0, -1,RealVal(0),RealVal(-5),
			#{names[0]: car1}, car1)

