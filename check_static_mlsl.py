import sys, pdb
import util
import mlsl2z3
import view
import mlsl_parser.ast_wrapper as ast_wrapper
from z3 import *
import mlsl_parser.model_parser_wrapper
import mlsl_parser.formula_parser_wrapper
import waxeye

			

def main():
	# we do not allow files that are very large. Currently limit is set to 1MB
	formula_parser = mlsl_parser.formula_parser_wrapper.FormulaParserWrapper() 
	formula_file = sys.argv[1]
	input_formula = open(formula_file, "r").read(1000000)
	try:
		parsed_formula = formula_parser.parse(input_formula)
	except waxeye.ParseError as error:
		print (error)
		sys.exit('Formula Parsing Error: While parsing the formula in ' + formula_file + ' a parsing error occured.')
	is_chopfree_below_not = not ast_wrapper.chop_below_not(parsed_formula)

	model_parser = mlsl_parser.model_parser_wrapper.ModelParserWrapper()
	model_file = sys.argv[2]
	input_model = open(model_file, "r").read(1000000)
	try:
		parsed_model = model_parser.parse(input_model)
	except waxeye.ParseError as error:
		print (error)
		sys.exit('Model Parsing Error: While parsing the model in ' + model_file + ' a parsing error occured.')
	v= view.View.ast_to_view(parsed_model)

	s = Solver()
	transformer = mlsl2z3.MLSL2Z3(hrestrict=is_chopfree_below_not)
	s.add(transformer.eval_formula(parsed_formula, v))
	result = s.check()
	if result == sat:
		print('The model satisfies the formula.')
	elif result == unsat:
		print('The model does NOT satisfy the formula.')
	elif result == unkown:
		print('Seems your query is too complex. Z3 was not able to solve the constraints.')		
	else:
		raise ValueError('Unexpected result from z3. Got ' +str(result))

if  __name__ =='__main__':
	main()
