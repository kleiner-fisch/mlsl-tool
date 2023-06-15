import unittest
import create_test_formulas as f
import formula_parser
import ast_wrapper, formula_parser_wrapper
import pdb

class TestFormulaParser(unittest.TestCase):
	
	def test_parse1(self):
		"""FIXME: Perhaps remove this test? With larger formula tree equality largely depends on precedence and parentheses...
		tests that the AST build by hand corresponding to the formula 
		<re(1) & re(2)> is created by the parser with a corresponding 
		string repr. of the formula"""
		formula = '(true ; ((true / (re(c1) & re(c2))) / true)) ; true'
		parsed_formula = self.parser_wrapper.parse(formula)
		
		middle = f.and_(f.res('c1'), f.res('c2'))
		middle = f.vchop(f.true_(), middle)
		middle = f.vchop(middle, f.true_())

		hchop1 = f.hchop(f.true_(), middle)
		complete_formula = f.hchop(hchop1, f.true_())
		
		self.assertTrue(ast_wrapper.eq(complete_formula, parsed_formula))
		
	def test_parse2(self):
		"""tests that the AST build by hand corresponding to the formula 
		re(1) & re(2) is created by the parser with a corresponding 
		string repr. of the formula"""
		t1 = f.crash('c1','c2')
		formula = 're(c1) & re(c2)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))

	def test_parse_vchop1(self):
		"""In latex the lower operand comes first and then the higher one.
			Here, it is the other way around. The first operand parsed, also is the first child of the operator node.
			In ascii text it makes sense for the higher operator to come first"""
		r1 = f.res('c1')
		r2 = f.res('c2')
		t1 = f.vchop(r1, r2)
		formula = 're(c1) / re(c2)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))

	def test_parse_hchop1(self):
		"""In latex the lower operand comes first and then the higher one.
			In ascii text it makes sense for the higher operator to come first"""
		r = f.res('c1')
		c = f.clm('c2')
		t1 = f.hchop(r, c)
		formula = 're(c1) ; cl(c2)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))		
		
	def test_parse3(self):
		"""tests that the AST build by hand corresponding to the formula 
		true ; re(c1) is created by the parser with a corresponding 
		string repr. of the formula"""
		t1 = f.hchop(f.true_(), f.res('c1'))
		formula = 'true ; re(c1)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))
		
	def test_parse_not1(self):
		"""tests that !(re(c)) is build correctly"""
		t1 = f.not_(f.res('c1'))
		formula = '!(re(c1))'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))
		
	def test_parse_lcomp(self):
		"""tests that the AST build by hand corresponding to the formula 
		1.1 <= length  & re(ego) is created by the parser with a corresponding 
		string repr. of the formula"""
		lcomp = f.lcomp(ast_wrapper.LEQ, 1.1)
		t1 = f.and_(lcomp, f.clm('ego'))
		formula = 'length <= 1.1   & cl(ego)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))
		
	def test_parse_hcomp(self):
		"""tests that the AST build by hand corresponding to the formula 
		1 < height  & re(ego) which is reformulated by the parser into 
		height > 1 & re(ego)
		Note that we assume in the parse tree the extension is on the right side, 
		accordingly we create the formula tree"""
		hcomp = f.hcomp(ast_wrapper.LESS, 1)
		t1 = f.and_(hcomp, f.clm('ego'))
		formula = 'height < 1   & cl(ego)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))

	def test_parse_free1(self):
		"""tests parsing of atom free"""
		free = f.free()
		formula = 'free'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(free, t2))

	def test_parse_free2(self):
		"""tests parsing of free toegether with other formulas"""
		free = f.free()
		lcomp = f.lcomp(ast_wrapper.LESS, 100)
		conj = f.and_(free, lcomp)
		formula = 'free & length < 100'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(conj, t2))		


	def test_parse_car_comp1(self):
		"""tests that the formula 'c1 = c2' is parsed correctly"""
		formula_manuel = f.car_comp('c1', 'c2')
		formula_string = 'c1 = c2'
		formula_parsed = self.parser_wrapper.parse(formula_string)
		self.assertTrue(ast_wrapper.eq(formula_manuel, formula_parsed))

	def test_parse_car_comp2(self):
		"""tests that the formula 'c1 = c2' is parsed correctly"""
		formula_manuel = f.car_comp('c1', 'ego')
		formula_string = 'c1 = ego'
		formula_parsed = self.parser_wrapper.parse(formula_string)
		self.assertTrue(ast_wrapper.eq(formula_manuel, formula_parsed))		

	def test_parse_car_comp3(self):
		"""tests that the formula 'c1 = c2' is parsed correctly"""
		formula_manuel = f.forall('c', ast_wrapper.CARS, f.car_comp('c', 'ego'))
		formula_string = 'forall c in cars. c = ego'
		formula_parsed = self.parser_wrapper.parse(formula_string)
		self.assertTrue(ast_wrapper.eq(formula_manuel, formula_parsed))			
		
	def test_parse_forall(self):
		"""tests whether the parser builds the forall ast correctly"""
		t1 = f.forall('x', ast_wrapper.CARS, f.res('x'))
		formula = 'forall x in cars.re(x)'
		t2 = self.parser_wrapper.parse(formula)
		self.assertTrue(ast_wrapper.eq(t1, t2))
		
	def test_chop_below_not1(self):
		""""tests whether a chop below a not is correctly found."""
		formula = f.not_(f.somewhere(f.res('c1')))
		self.assertTrue(ast_wrapper.chop_below_not(formula))		

	def test_chop_below_not2(self):
		"""checks whether there is a chop below a not, which there is not"""
		formula = f.somewhere(f.res('c1'))
		self.assertFalse(ast_wrapper.chop_below_not(formula))
		
	def setUp(self):
		self.parser_wrapper = formula_parser_wrapper.FormulaParserWrapper() 

if __name__ == '__main__':
    unittest.main()

 # for debugging
#def test_parse():
	#"""tests that the AST build by hand corresponding to the formula 
	#<re(1) & re(2)> is created by the parser with a corresponding 
	#string repr. of the formula"""
	#t1 = formulas.somewhere_crash('c1','c2')
	#f = 'true ; (true / re(c1) & re(c2) / true) ; true'
	#t2 = formula_parser_wrapper.parse(f)
	#return (t1,t2)
