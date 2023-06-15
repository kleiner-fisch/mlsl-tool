"""Takes the syntax tree for a MLSL formula and a description of a view and
returns z3-constraints that are satisfiable iff the view satisfies the formula"""

import car as car_
import view as view_
import mlsl_parser.ast_wrapper as ast_wrapper
import sys, pdb
import util, operator
from z3 import *
'''TODO: If we define a finite datatype of name, we can quantify over the values of the model
and have a procedure that attempts to find a model to a given formula. For a 
known number of cars (i.e. the size of the finite datatype) this should be complete.
Martin is researching about the required amount of cars to check whether a formula is satisfiable.
He first assumes, there are only finitly many cars, and then he checks how many cars needs at most to satisfy the formula. '''

class MLSL2Z3:
	'''instance variables are:
		- hrestrict : This option allows to avoid explicit quantifers in horizontal chops,
			however this is only possible if there are no negated hchops
		- check_some_sanity_conditions : defines whether sanity checks should be done.
			For test-purposes these checks can be disabled. If enabled, currently, not all
			conditions are checked.
	'''
	
	def vchop(self, top, bottom, view):
		# if the view is empty we do not attempt to chop it
		# pdb.set_trace()
		view_empty_constraint = And(self.eval_op(top, view), self.eval_op(bottom, view))
		
		# top_empty = And(self.eval_op(top, self.empty_view), self.eval_op(bottom, view))
		# bottom_empty = And(self.eval_op(top, view), self.eval_op(bottom, self.empty_view))
		# big_or = Or(top_empty, bottom_empty)
		# pdb.set_trace()
		m = Int(self.get_new_name('vchopvar'))
		chop_constraint = And(view.min_lane - 1 <= m, m <= view.max_lane)
		top_restr = self.eval_op(top, view.restrict_to_top(m + 1))
		bottom_restr = self.eval_op(bottom, view.restrict_to_bottom(m))
		# big_or = Or(big_or, Exists(m, And(top_restr, bottom_restr, chop_constraint)))
		combined = Exists(m, And(top_restr, bottom_restr, chop_constraint))

		return If(view.height() < 1, view_empty_constraint, combined)

		
	def notop(self, op, v):
		"""<op> the formula below the Not-Operator
		<v> the view on which to evaluate the Not-Operator
		<n> the number of negations seen from the root of the formula (excluding the current not)"""
		return Not(self.eval_op(op, v))
	
	def andop(self, ops, v):
		"""Creates a z3 epxression that is satisfied on v iff the z3-expressions 
		consisting of all of the operands in ops is satisfied on v"""
		return And([self.eval_op(op, v) for op in ops])

	def impliesop(self, a, b, v):
		"""Creates a z3 epxression that is satisfied on v iff the z3-expressions 
		consisting of all of the operands in ops is satisfied on v"""
		return Implies(self.eval_op(a, v), self.eval_op(b, v))
		
	def orop(self, ops, v):
		"""Creates a z3 epxression that is satisfied on v iff the any 
		of the operands in ops is satisfied by v"""
		return Or([self.eval_op(op, v) for op in ops])
		
	def hchop(self, op1, op2, view):
		"""Returns z3 expression for hchop. If the hchop is not negated, 
		we use the fact that the SMT-solver searches for satisfying assignments,
		and we do not add an quantifier.
		If there are negated hchops we have to add a quantifier.
		The constraints on the chop-point are added to the solver at the topmost level,
		to ensure they are not negated."""
		m = Real(self.get_new_name('hchopvar'))
		chop_constraint = And(m >= view.min_ext, m <= view.max_ext)
		left_restr = self.eval_op(op1, view.restrict_to_left(m))
		right_restr = self.eval_op(op2, view.restrict_to_right(m))
		if self.hrestrict:
			return And(left_restr, right_restr, chop_constraint)
		else:
			return Exists(m, And(left_restr, right_restr, chop_constraint))
	
	def forall(self, varname, vartype, formula, view):
		"""transforms the allquantified <formula>, with <varname> of <vartype> into a z3 expression"""
		'''first we extract the actual values from the nodes'''
		if vartype == ast_wrapper.CARS:
			result =  self.forall_cars(varname, formula, view)
		elif vartype == ast_wrapper.LANES:
			result = self.forall_lanes(varname, formula, view)			
		elif vartype == ast_wrapper.EXTS:
			result = self.forall_extensions(varname, formula, view)
		return result
        
     
	def forall_cars(self, varname, formula, view):
		"""transforms <formula>, quantified over all cars by the name <varname> into a z3 expression.
		We follow the approach in the thesis"""
		return And([self.eval_op(formula, view.update_val(varname, car)) 
			for car in view.cars.values()])
	
		
	def forall_lanes(self, varname, formula, view):
		"""transforms <formula>, quantified over all lanes by the name <varname> into a z3 expression"""
		'''look at comment in forall_cars for things to improve'''
		and_list = [ast_wrapper.substitute(formula, varname, lane) 
				for lane in range(view.min_lane, view.max_lane+1)]
		return self.andop(and_list, view)
		
	def forall_extensions(self, varname, formula, view):
		"""transforms <formula>, quantified over all extensions by the name <varname> into a z3 expression"""
		'''TODO: is it possible and/or helpful to only consider real values within the view??'''
		var = Real(varname)
		return ForAll(var, eval_op(formula, view))




		
	def exists(self, varname, vartype, formula, view):
		"""transforms the existentially quantified <formula>, with <varname> of <vartype> into a z3 expression"""
		'''first we extract the types of the variable'''
		if vartype == ast_wrapper.CARS:
			result =  self.exists_cars(varname, formula, view)
		elif vartype == ast_wrapper.LANES:
			result = self.exists_lanes(varname, formula, view)			
		elif vartype == ast_wrapper.EXTS:
			result = self.exists_extensions(varname, formula, view)
		return result        
     
	def exists_cars(self, varname, formula, view):
		"""transforms <formula>, quantified over all cars by the name <varname> into a z3 expression.
		We follow the approach in the thesis"""
		return Or([self.eval_op(formula, view.update_val(varname, car)) 
			for car in view.cars.values()])
		
		
	def exists_lanes(self, varname, formula, view):
		"""transforms <formula>, quantified over all lanes by the name <varname> into a z3 expression"""
		'''look at comment in exists_cars for things to improve'''
		var = Int(varname)
		return Exists(var, eval_op(formula, view))
		
	def exists_extensions(self, varname, formula, view):
		"""transforms <formula>, quantified over all extensions by the name <varname> into a z3 expression"""
		'''TODO: is it possible and/or helpful to only consider real values within the view??'''
		var = Real(varname)
		return Exists(var, eval_op(formula, view))
		
	def eval_op(self, op, view):
		"""To the outside this is the method that transforms a syntax tree and a view into 
		z3 constraints.
		<n> is the number of negations seen so far
		Determines from the operator at the current root the method to be called.
		The method then calls this function with a child and a changed view."""
		# pdb.set_trace()
		if op.type == ast_wrapper.HCHOP:
			return self.hchop(op.children[0], op.children[1], view)
		elif op.type == ast_wrapper.VCHOP:
			return self.vchop(op.children[0], op.children[1], view)
		elif op.type == ast_wrapper.TRUE:
			return BoolVal(True)
		elif op.type == ast_wrapper.FALSE:
			return BoolVal(False)
		elif op.type == ast_wrapper.FREE:
			return self.free(view)
		elif op.type == ast_wrapper.RES:
			return self.res(op.children[0], view)
		elif op.type == ast_wrapper.CLM:
			return self.clm(op.children[0], view)
		elif op.type == ast_wrapper.AND:
			return self.andop(op.children, view)
		elif op.type == ast_wrapper.OR:
			return self.orop(op.children, view)
		elif op.type == ast_wrapper.IMPLIES:
			return self.impliesop(op.children[0], op.children[1], view)
		elif op.type == ast_wrapper.NOT:
			return self.notop(op.children[0], view)
		elif op.type == ast_wrapper.LCOMP:
			return self.lcomp(op.children[0].type, op.children[1], view)
		elif op.type == ast_wrapper.HCOMP:
			return self.hcomp(op.children[0].type, op.children[1], view)
		elif op.type == ast_wrapper.EXISTS:
			varname = op.children[0].children[0]
			vartype = op.children[1].type
			return self.exists(varname, vartype, op.children[2], view)
		elif op.type == ast_wrapper.FORALL:
			varname = op.children[0].children[0]
			vartype = op.children[1].type
			return self.forall(varname, vartype, op.children[2], view)
		elif op.type == ast_wrapper.CCOMP:
			return self.car_comp(op.children[0], op.children[1], view)			
		else:
			raise ValueError('Unexpected operator/operand: ' +op.type)
	
	def lcomp(self, c, value, view):
		"""<c> is the comparator used
		<value> is the value the view is compared against. 
				The value may be a sum of values and variables 
		<view> the view for which the length should be compared"""
		c = ast_wrapper.comparators_to_functions[c]
		return c(view.length(), self.float_value(value))

	def car_comp(self, op1, op2, view):
		"""<car1, car2> the variablesto be compared 
		<view> the view for which the length should be compared"""
		car1 = view.get_car_from_ast(op1)
		car2 = view.get_car_from_ast(op2)
		return car1 == car2

	def hcomp(self, c, value, view):
		"""<c> is the comparator used
		<value> is the value the view is compared against. 
				The value may be a sum of values and variables 
		<view> the view for which the length should be compared"""
		c = ast_wrapper.comparators_to_functions[c]
		return c(view.height(), self.int_value(value))
		
	def float_value(self, *v):
		"""for a value, composed of sums, variables and float values
		returns a corresponding z3 expression"""
		if v[0].type == ast_wrapper.REAL_VALUE:
			return self.float_value(v.children)
		elif ast_wrapper.PLUS in [n.type for n in v]:
			assert v[1].type == ast_wrapper.PLUS
			return self.float_value(v[0]) + value(v[2])
		elif  v[0].type == ast_wrapper.FLOAT:
			return float(v[0].children[0])
		elif v[0].type == ast_wrapper.NAME:
			return Real(v[0].children[0])
		else:
			raise ValueError('Unexpected value: ' + str(v))
			
	def int_value(self, *v):
		"""for a value, composed of sums, variables and int values
		returns a corresponding z3 expression"""
		if v[0].type == ast_wrapper.INT_VALUE:
			return self.int_value(v.children)
		elif ast_wrapper.PLUS in [n.type for n in v]:
			assert v[1].type == ast_wrapper.PLUS
			return self.int_value(v[0]) + value(v[2])
		elif  v[0].type == ast_wrapper.INT:
			return int(v[0].children[0])
		elif v[0].type == ast_wrapper.NAME:
			return Int(v[0].children[0])
		else:
			raise ValueError('Unexpected value: ' + str(v))
	
	def free(self, view):
		"""creates a formula that checks that the current view 
		  - does not contain reservations or claims,
		  - has nonzero extension and
		  - contains exactly one lane."""
		height_constraint = view.height() == 1
		ext_constraint = view.length() > 0
		cars_outside_view = [car.outside_view(view) for car in view.cars.values()]
		return And(height_constraint, ext_constraint, *cars_outside_view)

	def clm(self, op, view):
		"""Almost the same as res, but a little easier as there can be at most 1 claim"""
		car = view.get_car_from_ast(op)
		if car.clm is None:
			return BoolVal(False)
		else:
			return And(view.height() == 1, view.length() > 0,
					view.min_lane == car.clm, car.fills_view(view))


		
	def res(self, op, view):
		"""determines whether on a given view a reservation holds.
		For this
			- the view must have height 1
			- the views width must be > 0
			- the views lane must be reserved
			- the view must be filled by the reservation of the car
		(also see the publications on MLSL).
		Note that the ast has the structure re(Name(foo) | ego)"""
		car = view.get_car_from_ast(op)
		if len(car.res) == 0:
			return BoolVal(False)
		elif self.check_some_sanity_conditions and len(car.res) > 2:
			raise Exception('no of reserved lanes must be 1 or 2; is ' + str(car.res))
		else:
			res_check = Or([view.min_lane == lane for lane in car.res])
			return And(view.height() == 1, view.length() > 0, 
					car.fills_view(view), res_check)
			
			
	def get_new_name(self, prefix):
		"""returns a new var name with the given prefix"""
		result = prefix + str(self.var_counter)
		self.var_counter += 1
		return result 
		
	def eval_formula(self, formula, view):
		"""top level function to be called to evaluate a formula on a model.
		Ensures that restricted negation is satisfied, if it is given"""
		# pdb.set_trace()
		# self.empty_view = view_.empty_view(view.cars, view.ego)
		if self.vrestrict or self.hrestrict:
			if ast_wrapper.chop_below_not(formula):
				raise ValueError("With restricted negation 'chops' are not allowed bellow 'not'")
		return self.eval_op(formula, view)
		
		
	def __init__(self, hrestrict=True, check_some_sanity_conditions=True):
		self.check_some_sanity_conditions = check_some_sanity_conditions
		self.var_counter = 0
		self.vrestrict = False
		self.hrestrict = hrestrict
