from z3 import *
import car, view, mlsl2z3
import mlsl_parser.create_test_formulas as f
import model_creator
import mlsl_parser.formula_parser_wrapper 
import mlsl_parser.ast_wrapper as ast_wrapper
import unittest
import sys, pdb

# not sure if this works as expected. Sometimes errors are swallowed and failed tests pass....
def debug_on(*exceptions):
	"""calls debuger on failed test. The type of the exception has to be in 'exceptions' for it to work"""
	if not exceptions:
		exceptions = (AssertionError, AttributeError, IndexError)
	def decorator(f):
		@functools.wraps(f)
		def wrapper(*args, **kwargs):
			try:
				return f(*args, **kwargs)
			except exceptions:
				pdb.post_mortem(sys.exc_info()[2])
			return wrapper
	return decorator

class TestMC(unittest.TestCase):
	
	def setUp(self):
		self.transformer = mlsl2z3.MLSL2Z3()
		self.names = ['c1','c2','c3']
		self.models = model_creator.ModelCreator()
		self.formula_parser = mlsl_parser.formula_parser_wrapper.FormulaParserWrapper()

	def test_res1(self):
		"""tests whether a view filled by a reservation satisfies a simple reservation formula"""
		v = self.models.create_model1(['C1','C2','C3'])
		formula = f.exists('c', ast_wrapper.CARS, f.res('c'))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_res2(self):
		"""tests whether a view that contains a reservation 
		and free road satisfies a simple reservation formula.
		The formula is not satisfied, because the view is not filled by the reservation"""
		v = self.models.create_model2(['C1','C2','C3'])
		formula = f.exists('c', ast_wrapper.CARS, f.res('c'))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_res_hchop1(self):
		"""tests whether a view that starts with free road 
		and finishes with a reservation satisfies the formula (T ; res(0))"""
		v = self.models.create_model2(self.names)
		res = f.res(self.names[0])
		formula = f.hchop(f.true_(), res)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_not_hchop1(self):
		"""tests whether a view that starts with free road 
		and finishes with a reservation satisfies the formula !(T ; res(0))"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.create_model2(self.names)
		res = f.res(self.names[0])
		formula = f.not_(f.hchop(f.true_(), res))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_res_hchop2(self):
		"""tests whether a view that starts with free road, continues with a reservation 
		and finishes with free road satisfies the formula (T ; res(0)).
		The formula is not satisfied the the formula demands the view ends with a reservation"""
		v = self.models.create_model3(self.names)
		res = f.res(self.names[0])
		formula = f.hchop(f.true_(), res)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)

	def test_res_hchop3(self):
		"""tests whether a view that starts with free road, continues with a reservation 
		and finishes with free road satisfies the formula (T ; res(0) ; T)"""
		v = self.models.create_model3(self.names)
		res = f.res(self.names[0])
		formula = f.on_some_subintervall(res)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_res_hchop4(self):
		"""tests whether a view filled by a reservation 
		satisfies the formula (T ; res(0) ; T)"""
		v = self.models.create_model1(self.names)
		res = f.res(self.names[0])
		formula = f.on_some_subintervall(res)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_res_hchop5(self):
		"""tests whether a view without a reservation 
		satisfies the formula (T ; res(0) ; T)"""
		v = self.models.create_model4(self.names)
		res = f.res(self.names[0])
		formula = f.on_some_subintervall(res)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_res_vchop1(self):
		"""tests whether a view filled by a reservation 
		satisfies the formula (T / res(0))"""
		v = self.models.create_model1(self.names)
		formula = '(true / re('+self.names[0]+'))'
		ft = self.formula_parser.parse(formula)
		s = Solver()
		s.add(self.transformer.eval_formula(ft, v))
		self.assertEqual(s.check(), sat)
		
		
    ## calls the debug function on fail    
	##@debug_on()
	def test_res_vchop2(self):
		"""tests whether a view that has a reservation somehwere satisfies
		<res(a)>, or alternativly (somewhere res(a))"""
		v = self.models.create_model6(self.names)
		formula = f.somewhere(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_res_vchop3(self):
		"""tests whether a view that is filled by a reservation satuisifes
		<res(a)>, or alternativly (somewhere res(a))"""
		v = self.models.create_model1(self.names)
		formula = f.somewhere(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)

	def test_res_vchop4(self):
		"""tests whether a view without a reservation satuisifes
		<res(a)>, or alternativly (somewhere res(a))"""
		v = self.models.create_model4(self.names)
		formula = f.somewhere(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_res_vchop5(self):
		"""tests whether a view with 2 reservations satuisifes
		<res(a)>, or alternativly (somewhere res(a))"""
		v = self.models.create_model6(self.names)
		formula = f.somewhere(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)

	def test_res_vchop6(self):
		"""tests if there is somwhere a reservation with free space above it"""
		v = self.models.small_model1()
		res_form = f.exists('c1', ast_wrapper.CARS, f.res('c1'))
		vert_form = f.vchop(f.free(), res_form)
		formula = f.somewhere(vert_form)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)

	def test_res_vchop7(self):
		"""tests if there is somwhere a reservation with free space below  it"""
		v = self.models.small_model1()
		res_form = f.exists('c1', ast_wrapper.CARS, f.res('c1'))
		vert_form = f.vchop(res_form, f.free())
		# vert_form = f.vchop(f.hcomp(ast_wrapper.EQ,1), f.hcomp(ast_wrapper.LEQ,1))
		formula = f.somewhere(vert_form)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)


	def test_hcomp1(self):
		"""tests if there is free space infront of ego"""
		v = self.models.unsat_big_model5()
		formula = '<@ re(ego) ; (free & length >= 3) @>'
		formula_parsed = self.formula_parser.parse(formula)		
		s = Solver()
		s.add(self.transformer.eval_formula(formula_parsed, v))
		self.assertEqual(s.check(), unsat)

	def test_hcomp2(self):
		"""tests if there is a res infront of ego"""
		v = self.models.unsat_big_model5()
		formula = '<@ re(ego) ; length <= 3 ;  exists var in cars. (!(var = ego) & re(var)) @>'
		formula_parsed = self.formula_parser.parse(formula)		
		s = Solver()
		s.add(self.transformer.eval_formula(formula_parsed, v))
		self.assertEqual(s.check(), sat)


	def test_not1(self):
		"""tests whether not(res(a)) is satisfied on the empty view"""
		v = self.models.create_empty_model(self.names)
		formula = f.not_(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)
		
	def test_not2(self):
		"""tests whether not(res(a)) is satisfied by a view filled by res(a)"""
		v = self.models.create_model1(self.names)
		formula = f.not_(f.res(self.names[0]))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
	
	def test_not3(self):
		""""tests whether not<res(a)> is satisfied a view containing res(a).
		This requires that we allow full negation"""
		v = self.models.create_model8(self.names)
		formula = f.not_(f.somewhere(f.res(self.names[0])))
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_not4(self):
		""""tests whether not<res(a)> is satisfied a view containing res(a).
		This requires that we allow full negation"""
		v = self.models.create_model2(self.names)
		formula = f.not_(f.somewhere(f.res(self.names[0])))
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_and1(self):
		"""tests whether res(a) & res(b) is satisfied by a view filled with
		res(a), res(b)"""
		v = self.models.create_view_crash1(['C1','C2','C3'])
		formula = f.and_(f.not_(f.car_comp('c1', 'c2')), f.and_(f.res('c1'), f.res('c2')))
		exists = f.exists('c1', ast_wrapper.CARS, f.exists('c2', ast_wrapper.CARS, formula))
		s = Solver()
		s.add(self.transformer.eval_formula(exists, v))
		self.assertEqual(s.check(), sat)
		
	def test_free1(self):
		"""tests if somewhere free is satisfied"""
		v = self.models.small_model1()
		formula = f.somewhere(f.free())
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)

	def test_free2(self):
		"""tests if there is a car with free space infront of- and behind of it"""
		v = self.models.small_model1()
		exists_res = f.exists('c', ast_wrapper.CARS, f.res('c'))
		free = f.hchop(f.free(), f.hchop(exists_res, f.free()))
		formula = f.somewhere(free)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)		

	def test_and2(self):
		"""tests whether res(a) & res(b) is satisfied by a view filled with
		res(a), The formula is not satisfied because there are no overlapping
		reservations"""
		v = self.models.create_model7(['C1','C2','C3'])
		formula = f.and_(f.not_(f.car_comp('c1', 'c2')), f.and_(f.res('c1'), f.res('c2')))
		exists = f.exists('c1', ast_wrapper.CARS, f.exists('c2', ast_wrapper.CARS, formula))
		s = Solver()
		s.add(self.transformer.eval_formula(exists, v))
		self.assertEqual(s.check(), unsat)

	def test_and3(self):
		"""similar to test_and2, only that here we allow the quantified variables to be equal.
		Thus the property is satisfies"""
		v = self.models.create_model7(['C1','C2','C3'])
		formula = f.and_(f.res('c1'), f.res('c2'))
		exists = f.exists('c1', ast_wrapper.CARS, f.exists('c2', ast_wrapper.CARS, formula))
		s = Solver()
		s.add(self.transformer.eval_formula(exists, v))
		self.assertEqual(s.check(), sat)		
		
	def test_somewhere1(self):
		"""tests the somewhere abbreviation"""
		v = self.models.create_view_crash2(self.names)
		formula ='<@ exists c1 in cars. ( exists c2 in cars. ( !(c1=c2) & re(c1) & re(c2)) ) @>'
		parsed_form = self.formula_parser.parse(formula)
		s = Solver()
		s.add(self.transformer.eval_formula(parsed_form, v))
		self.assertEqual(s.check(), sat)

	def test_somewhere_crash1(self):
		"""tests whether somewhere there are overlapping reservations of car_a and car_b
		on a view where there are overlapping reservations"""
		v = self.models.create_view_crash2(['C1', 'C2'])
		f1 = f.and_(f.res('d1'), f.res('d2'))
		f2 = f.not_(f.car_comp('d1', 'd2'))
		f3 = f.and_(f1, f2)
		ex = f.exists('d1', ast_wrapper.CARS, f3)
		ex = f.exists('d2', ast_wrapper.CARS, ex)
		formula = f.somewhere(ex)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)

	def test_somewhere_crash2(self):
		"""tests whether somewhere there are overlapping reservations of car_a and car_b
		on a view where there are no overlapping reservations"""
		v = self.models.create_model6(['C1', 'C2'])
		f1 = f.and_(f.res('d1'), f.res('d2'))
		f2 = f.not_(f.car_comp('d1', 'd2'))
		f3 = f.and_(f1, f2)
		ex = f.exists('d1', ast_wrapper.CARS, f3)
		ex = f.exists('d2', ast_wrapper.CARS, ex)
		formula = f.somewhere(ex)
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_forall_cars1(self):
		"""tests whether (forall x in cars.!re(x)) is satisfied on a view that is filled by a reservation.
		The formula is not satisfied satisfied, because there is a car whose reservation fills the view"""
		v = self.models.create_model1(self.names)
		formula =  f.forall('x', ast_wrapper.CARS, f.not_(f.res('x')))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), unsat)
		
	def test_forall_cars2(self):
		"""tests whether (forall x in cars.!re(x)) is satisfied on a view that is not filled by a reservation.
		The formula is satisfied, because the view is not filled by the reservatoin."""
		v = self.models.create_model2(self.names)
		formula =  f.forall('x', ast_wrapper.CARS, f.not_(f.res('x')))
		s = Solver()
		s.add(self.transformer.eval_formula(formula, v))
		self.assertEqual(s.check(), sat)

	def test_chop_below_not1(self):
		free = ('length > 0.0 & height = 1 & forall x in cars.' + 
					'(!(true ; cl(x) | re(x) ; true))' )
		v = self.models.create_model2(self.names)
		t = self.formula_parser.parse(free)
		self.assertRaises(ValueError, self.transformer.eval_formula, t, v)
		
	def test_free1(self):
		"""Tests the formula free on a view with one lane that finishes
		with a reservation""" 
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		free = ('length > 0.0 & height = 1 & forall x in cars.' + 
					'(!(true ; cl(x) | re(x) ; true))' )
		v = self.models.create_model2(self.names)
		t = self.formula_parser.parse(free)
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)
		
	def test_free2(self):
		"""Tests the formula free on a view with one lane that does not 
		contain a reservation""" 
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		free = ('length > 0.0 & height = 1 & forall x in cars.' + 
					'(!(true ; cl(x) | re(x) ; true))' )
		v = self.models.create_model4(self.names)
		t = self.formula_parser.parse(free)
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), sat)
	

if __name__ == '__main__':
	# sys.path.append(os.getcwd()+'/lib/waxeye')
	# sys.path.append(os.getcwd()+'/lib/z3/python')
	# sys.path.append(os.getcwd()+'/lib/z3')
 	unittest.main()