"""An AST as defined by the waxeye tool has
	- a <type> if it is not a string-terminal
	- a list of <children>.
This module provides some convience functions to work and create those trees"""
import pdb
from waxeye import AST
import operator

'''The ids of node-values, as defined by the parsing-grammar'''
START = 'Start'
HCHOP = 'HChop_Expr'
VCHOP = 'VChop_Expr'
IFF = 'Iff_Expr'
RES = 'Re_Expr'
CLM = 'Cl_Expr'
IMPLIES = 'Implies_Expr'
OR = 'Or_Expr'
NOT = 'Not_Expr'
AND = 'And_Expr'
EXISTS = 'Exists_Expr'
FORALL = 'Forall_Expr'
LCOMP = 'Length_Comparisson'
HCOMP = 'Height_Comparisson'
CCOMP = 'Car_Comparisson'
SOMEWHERE = 'Somewhere_Expr'
'''may be composed of additions of more values and varaibles'''
INT_VALUE = 'Int_Value'
REAL_VALUE = 'Real_Value'
'''a simple value, reperesented as string'''
INT = 'Int'
FLOAT = 'Float'
NAME = 'Name'

'''in the trees waxeye stores the labels of these nodes in upper case letters.
	Perhaps because these are terminals!??? 
	==> Probably it takes the names of the nonterminals.
		We remove the strings of these nodes explicitly with the waxeye operator : 
		That is, for the node TRUE we remove the child 'true' by defining TRUE 	<- :( 'true')''' 
LENGTH = 'LENGTH'
HEIGHT = 'HEIGHT'
FREE = 'FREE'
EGO = 'EGO'
TRUE = 'TRUE'
FALSE = 'FALSE'
CARS = 'CARS'
EXTS = 'EXTS'
LANES = 'LANES'
GEQ = 'GEQ'
LEQ = 'LEQ'
LESS = 'LESS'
EQ = 'EQ'
GREATER = 'GREATER'
PLUS = 'PLUS' 

'''usefull collections of these operators/keywords'''
primitive_types = [NAME, FLOAT, INT]
comparators_to_functions = (
		{GEQ : operator.ge, 
		LEQ : operator.le, 
		LESS : operator.lt, 
		EQ : operator.eq, 
		GREATER : operator.gt})


def ast(value):
	"""an easier version to create a waxeye ast, if no children or position in a string are given"""
	return AST(value, [], 0)
		
def copy(t):
	"""creates a copy of t"""
	if isinstance(t, AST):
		children = [copy(child) for child in t.children]
		return AST(t.type, children, t.pos)
	else:
		return t
	
def add_child(ast, value):
	"""to the given ast adds a child that has the type given as value"""
	if ast.type in primitive_types:
		ast.children.append(value)
	else:
		t = AST(value, [], 0)
		ast.children.append(t)
		return t

def eq(a, b):
	"""Checks whether all nodes in tree a have an equal node in tree b,
	at the same position.
	Note that some children may be of class string."""
	if not isinstance(b, a.__class__):
		return False
	elif isinstance(a, ''.__class__):
		return a == b
	return (a.type == b.type and len(a.children) == len(b.children) and 
				all([eq(c1, c2) for c1,c2 in zip(a.children, b.children)]))
		
def accept(self, visitor):
	"""simple visitor method
	Traverses tree in order i.e. parent, complete left, complete right"""
	visitor.visit(self)
	for child in self.children:
		child.accept(visitor)

		
def substitute(t, x, y, create_copy=True):
	"""in all nodes of t substitutes the var-name x with y.
	create_copy is used to differentiate recursive calls from first calls.
	The method initially creates a copy of t, and then searches all name-nodes,
	where it checks the name of the child, and if necessary replaces the child"""
	# This case only applies if substitute was called for a string from the outside
	if isinstance(t, str):
		if t == x:
			return y
	if create_copy:
		t = copy(t)
	if t.type == NAME:
		if t.children[0] == x:
			t.children[0] = y
	else :
		for n in t.children:
			if not isinstance(n, str):
				substitute(n, x, y, False)
	return t 
			
			
def chop_below_not(ast, found_not=False):
	"""returns True if there is a chop below a not""" 
	'''string-nodes may not have children or a type'''
	#pdb.set_trace()
	if isinstance(ast, str) or len(ast.children) == 0:
		return False
	elif ast.type == NOT:
		for child in ast.children:
			return chop_below_not(child, found_not=True)
	elif ast.type in [HCHOP, VCHOP]:
		if found_not :
			return True
	return any([chop_below_not(child, found_not) for child in ast.children])
		
