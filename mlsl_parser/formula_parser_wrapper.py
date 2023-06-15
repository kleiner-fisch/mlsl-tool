"""wrapper methods for the mlsl-parser. Calls the parser which creates an AST.
This AST is modified by these methods and then returned"""
import waxeye
import pdb
import ast_wrapper
import formula_parser
import create_test_formulas

class FormulaParserWrapper:

	def switch_Case_Of_First_Letter(self, ast):
		"""switches the case of the first letter in all nodes, except in children of
		Name, Double or Int nodes.
		This seems necessary, cause the parser switches them to lower case for some reason.
		We assume the root is not a Double, Int or Name node!!"""
		ast.type = ast.type[0].title() + ast.type[1:]
		if not (ast.type in ast_wrapper.primitive_types):
			for child in ast.children:
				self.switch_Case_Of_First_Letter(child)
			
	def switch_comparator(self, c):
		"""for >= returns <= and vice versa and for < returns > and vice versa"""
		if c == ast_wrapper.GEQ:
			result = ast_wrapper.LEQ
		elif c == ast_wrapper.LEQ:
			result = ast_wrapper.GEQ
		elif c == ast_wrapper.LESS:
			result = ast_wrapper.GREATER
		elif c == ast_wrapper.GREATER:	
			result = ast_wrapper.LESS
		else:
			raise ValueError('Illegal comparator given: ' + c)
		return result


	def unfold_somewhere(self, ast):
		"""
		syntactically replace somewhere by its unfolded formula
		"""
		if ast.type in ast_wrapper.primitive_types:
			return
		for i in range(len(ast.children)):
			if ast.children[i].type == ast_wrapper.SOMEWHERE:
				ast.children[i] = create_test_formulas.somewhere(ast.children[i].children[0])
		for child in ast.children:
				self.unfold_somewhere(child)

	def unify_ast(self, ast):
		"""
		- Ensures that nodes whose children have values (double, int, name) only have one child, 
				and that this child stores the complete name.
		- Further turns all first letters of all types into uppercase (the parser turns them into lower cases...)
		"""
		self.switch_Case_Of_First_Letter(ast)
		if ast.type in ast_wrapper.primitive_types:
			'''The different characters are stored in different nodes. 
			Put them all into one node'''
			ast.children = [''.join(ast.children)]
			return
		'''always, when the current node is not a 'Name' etc, we want to descent recursivly'''
		for child in ast.children:
				self.unify_ast(child)

	def parse(self, input):
		ast = self.parser.parse(input)
		if isinstance(ast, waxeye.ParseError):
			''' here an exception should be raised. in unittests the raise is somehow ignored....'''
			raise ast
		else:		
			self.unify_ast(ast)
			# pdb.set_trace()
			self.unfold_somewhere(ast)
			'''we are not interested in the start rule (which is the root)'''
			return ast.children[0]

	# for debugging
	def test_input(self):
		while True:
			input = raw_input("Waiting: ")
			if input == 'q':
				return
			ast = p.parse(input)
			if isinstance(ast, waxeye.ParseError):
				''' here an exception should be raised. in unittests the raise is somehow ignored....'''
				print ast
				input = raw_input("Raise or continue? r for raise: ")
				if input == 'r':
					raise ast
			else:		
				unify_ast(ast)
				print ast


	def __init__(self):
		self.parser = formula_parser.FormulaParser()