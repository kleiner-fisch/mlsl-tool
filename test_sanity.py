from z3 import *
import car, view, mlsl2z3
import mlsl_parser.create_test_formulas as f
import model_creator
import mlsl_parser.formula_parser_wrapper as formula_parser_wrapper
import mlsl_parser.ast_wrapper as ast_wrapper
import unittest
import functools

import sys, pdb

class TestSanity(unittest.TestCase):

	def setUp(self):
		self.models = model_creator.ModelCreator()
		self.formula_parser = formula_parser_wrapper.FormulaParserWrapper()
	
	def sanity_formula1_man(self):
		"""Creates the 1st sanity condition, that there is no car 
		with a res and a claim for the same lane"""
		and_ = f.and_(f.res('var'), f.clm('var'))
		not_somewhere = f.not_(f.somewhere(and_))
		return f.forall('var', ast_wrapper.CARS, not_somewhere)

	def sanity_formula1_parsed(self):
		"""see above"""
		formula = 'forall var in cars. (!<@ re(var) & cl(var) @>)'
		return self.formula_parser.parse(formula)
		
	def sanity_formula2_man(self):
		"""Creates the 2nd sanity condition, that all cars do not have three 
		reservations on different lanes"""
		sw1,sw2, sw3  = f.somewhere(f.res('c1')), f.somewhere(f.res('c1')), f.somewhere(f.res('c1'))
		sw_all = f.vchop(sw1, f.vchop(sw2, sw3))
		return f.forall('c1', ast_wrapper.CARS, f.not_(sw_all))

	def sanity_formula2_parsed(self):
		"""see above"""
		formula = 'forall v in cars. ( !((<@ re(v) @> / <@ re(v) @>) / <@ re(v) @>) )'
		return self.formula_parser.parse(formula)		

	def sanity_formula4_man(self):
		"""Creates that there is no car that has two reservations and has a claim"""
		swhere_res1 = f.somewhere(f.res('c'))
		swhere_res2 = f.somewhere(f.res('c'))
		two_res = f.vchop(swhere_res1, swhere_res2)
		not_swhere_clm = f.not_(f.somewhere(f.clm('c')))
		return f.forall('c', ast_wrapper.CARS, f.implies(two_res, not_swhere_clm))

	def sanity_formula4_parsed(self):
		"""see above"""
		formula = 'forall v in cars. ( (<@ re(v) @> / <@ re(v) @>) --> !<@ cl(v) @> )'
		return self.formula_parser.parse(formula)			

	def sanity_formula5_man(self):
		"""Creates the 5th sanity condition that if there is 
		a res and a claim then they are on adjacent lanes"""
		swhere_res = f.somewhere(f.res('c'))
		swhere_clm = f.somewhere(f.clm('c'))
		res_up = f.somewhere(f.vchop(f.res('c'), f.clm('c')))
		res_down = f.somewhere(f.vchop(f.clm('c'), f.res('c')))
		res_clm = f.and_(swhere_res, swhere_clm)
		formula = f.implies(res_clm, f.or_(res_up, res_down))
		return f.forall('c', ast_wrapper.CARS, formula)

	def sanity_formula5_parsed(self):
		"""see above"""
		formula = 'forall v in cars. ( (<@ re(v) @> & <@ cl(v) @>) --> ' +\
				'<@ (cl(v) / re(v)) | (re(v) / cl(v)) @> )'
		return self.formula_parser.parse(formula)		
		
		
	def sanity_formula6_man(self):	
		"""Creates the 6th sanity condition, which is
		if there are at least two different reservations, there are at least two different res next to each other"""
		swhere_res1 = f.somewhere(f.res('c'))
		swhere_res2 = f.somewhere(f.res('c'))
		two_res1 = f.vchop(swhere_res1, swhere_res2)
		two_res2 = f.somewhere(f.vchop(f.res('c'), f.res('c')))
		return f.forall('c', ast_wrapper.CARS, f.implies(two_res1, two_res2))

	def sanity_formula6_parsed(self):
		"""see above"""
		formula = 'forall v in cars. ( (<@ re(v) @> & <@ re(v) @>) --> <@ (re(v) / re(v)) @> )'
		return self.formula_parser.parse(formula)			
		
	def some_sanity_formulas(self):
		"""creates the sanity formulas 1,2,4,5,6"""
		s1 = self.sanity_formula1_man()
		s2 = self.sanity_formula2_man()
		s4 = self.sanity_formula4_man()
		s5 = self.sanity_formula5_man()
		s6 = self.sanity_formula6_man()
		s1_s2 = f.and_(s1, s2)
		s4_s5 = f.and_(s4, s5)
		s1_s2_s4_s5 = f.and_(s1_s2, s4_s5)
		return f.and_(s1_s2_s4_s5, s6)
		
	'''---
	--- Here come the sanity-test methods
	---'''
	def test_sanity1_man(self):
		"""tests whether the 1st sanity condition, that there is no car with a res and a claim for the same lane 
		is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model1()
		t = self.sanity_formula1_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

	def test_sanity1_parsed(self):
		"""tests whether the 1st sanity condition, that there is no car with a res and a claim for the same lane 
		is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model1()
		t = self.sanity_formula1_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)		
		
	def test_sanity2_sat_man(self):
		"""tests whether the 2nd sanity condition, that there are no three 
		reservations on different lanes, is satisfied on a view that does sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.sat_big_model()
		t = self.sanity_formula2_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), sat)

	def test_sanity2_sat_parsed(self):
		"""tests whether the 2nd sanity condition, that there are no three 
		reservations on different lanes, is satisfied on a view that does sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.sat_big_model()
		t = self.sanity_formula2_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), sat)		
			
	def test_sanity2_unsat_man(self):
		"""tests whether the 2nd sanity condition, that there are no three 
		reservations on different lanes, is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False, check_some_sanity_conditions=False)
		v = self.models.unsat_big_model2()
		t = self.sanity_formula2_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

	def test_sanity2_unsat_parsed(self):
		"""tests whether the 2nd sanity condition, that there are no three 
		reservations on different lanes, is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False, check_some_sanity_conditions=False)
		v = self.models.unsat_big_model2()
		t = self.sanity_formula2_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)		

	def test_sanity4_man(self):
		"""tests whether the 4th sanity condition, that there is no car 
		that has two reservations and has a claim is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model4()
		t = self.sanity_formula4_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

	def test_sanity4_parsed(self):
		"""tests whether the 4th sanity condition, that there is no car 
		that has two reservations and has a claim is not satisfied on a view that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model4()
		t = self.sanity_formula4_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)		

	def test_sanity5_man(self):
		"""tests whether the 5th sanity condition, that if there are 
		a res and a claim then they are on adjacent lanes on a view 
		that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model5()
		t = self.sanity_formula5_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

	def test_sanity5_parsed(self):
		"""tests whether the 5th sanity condition, that if there are 
		a res and a claim then they are on adjacent lanes on a view 
		that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model5()
		t = self.sanity_formula5_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)		
		
	def test_sanity6_man(self):
		"""tests whether the 6th sanity condition that 
		if there are at least two different reservations, there are at least two different res next to each other 
		on a view  that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model6()
		t = self.sanity_formula6_man()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

	def test_sanity6_parsed(self):
		"""tests whether the 6th sanity condition that 
		if there are at least two different reservations, there are at least two different res next to each other 
		on a view  that does not sat it"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model6()
		t = self.sanity_formula6_parsed()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)		
		
	def test_sanity_all1(self):
		"""tests whether the sanity conditions 1,2,4,5,6 hold on a view that satisfies them"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.sat_big_model()
		t = self.some_sanity_formulas()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), sat)

	def test_sanity_all2(self):
		"""tests whether the sanity conditions 1,2,4,5,6 hold on a view that 
		violates condition 5"""
		self.transformer = mlsl2z3.MLSL2Z3(hrestrict=False)
		v = self.models.unsat_big_model5()
		t = self.some_sanity_formulas()
		s = Solver()
		s.add(self.transformer.eval_formula(t, v))
		self.assertEqual(s.check(), unsat)

if __name__ == '__main__':
    unittest.main()
