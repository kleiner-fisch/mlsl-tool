import model_parser
import waxeye
import ast_wrapper



class ModelParserWrapper:

	def switch_Case_Of_First_Letter(self, ast):
		"""switches the case of the first letter in all nodes, except in children of
		Name, Double or Int nodes.
		This seems necessary, cause the parser switches them to lower case for some reason.
		We assume the root is not a Double, Int or Name node!!"""
		ast.type = ast.type[0].title() + ast.type[1:]
		if not (ast.type in ast_wrapper.primitive_types):
			for child in ast.children:
				self.switch_Case_Of_First_Letter(child)

	def unify_ast(self, ast):
		"""
		- Ensures that nodes whose children have values (double, int, name) only have one child, 
				and that this child stores the complete name.
		- Further turns all first letters of all types into uppercase (the parser turns them into lower cases...)
		"""
		self.switch_Case_Of_First_Letter(ast)
		if ast.type == ast_wrapper.NAME:
			'''The different characters are stored in different nodes. 
			Put them all into one node'''
			ast.children = [''.join(ast.children)]
		elif ast.type == ast_wrapper.FLOAT:
			ast.children = [float(''.join(ast.children))]
		elif ast.type == ast_wrapper.INT:
			ast.children = [int(''.join(ast.children))]
		else:
			'''always, when the current node is not a 'Name' etc, we want to descent recursivly'''
			for child in ast.children:
					self.unify_ast(child)


	def parse(self, input):
		ast = self.parser.parse(input)
		if isinstance(ast, waxeye.ParseError):
			raise ast
		else:		
			self.unify_ast(ast)
			return  ast
			
	def __init__(self):
		self.parser = model_parser.ModelParser()