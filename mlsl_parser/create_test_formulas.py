import ast_wrapper
import pdb
"""In this file we define methods to directly create formulas (bypassing the parser).
	This enables us to test the parser."""

	

def crash(name1, name2):
	"""creates a formula that is satisfied by overlaying reservations"""
	return and_(res(name1), res(name2))

def somewhere(f):
	"""f : syntax tree of the formula which should hold somewhere 
	Creates the syntax tree for <f> """	
	# first true above, then true below
	middle = vchop(true_(), f)
	middle = vchop(middle, true_())
	# then true in front and true behind
	hchop1 = hchop(true_(), middle)
	hchop1 = hchop(hchop1, true_())
	return hchop1
	
def on_some_subintervall(f):
	"""creates a formula (true ; f ; true)""" 
	result = hchop(true_(), f)
	result = hchop(result, true_())	
	return result
	
#def free():
	#result = forall('x', ast_wrapper.CARS, not_(re('x')))
	#result = and_(result, lcomp)
	
'''simple formulas that take formulas as arguments and put themselves 
on top of those arguments'''
def lcomp(comparator, length):
	"""creates a formula (\ell ~ length) where ~ is the comparator"""
	result = ast_wrapper.ast(ast_wrapper.LCOMP)
	ast_wrapper.add_child(result, comparator)
	fnode = ast_wrapper.add_child(result, ast_wrapper.FLOAT)
	ast_wrapper.add_child(fnode, str(length))
	return result

def hcomp(comparator, height):
	"""creates a formula (\omega ~ height) where ~ is the comparator"""
	result = ast_wrapper.ast(ast_wrapper.HCOMP)
	ast_wrapper.add_child(result, comparator)
	fnode = ast_wrapper.add_child(result, ast_wrapper.INT)
	ast_wrapper.add_child(fnode, str(height))
	return result


	
def true_():
	return ast_wrapper.ast(ast_wrapper.TRUE)
	
def false_():
	return ast_wrapper.ast(ast_wrapper.FALSE)

def hchop(l,r):
	"""connects two formulas l,r with a hchop"""
	troot = ast_wrapper.ast(ast_wrapper.HCHOP)
	troot.children = [l,r]
	return troot

def vchop(top, bottom):
	"""connects two formulas top, bottom with a vchop"""
	troot = ast_wrapper.ast(ast_wrapper.VCHOP)
	troot.children = [top, bottom]
	return troot
	
def and_(a, b):
	"""creates a mlsl syntax tree for a&b"""
	root = ast_wrapper.ast(ast_wrapper.AND)
	root.children.append(a)
	root.children.append(b)
	return root

def implies(a, b):
	"""creates a mlsl syntax tree for a --> b"""
	root = ast_wrapper.ast(ast_wrapper.IMPLIES)
	root.children.append(a)
	root.children.append(b)
	return root
	
def or_(a, b):
	"""creates a mlsl syntax tree for a | b"""
	root = ast_wrapper.ast(ast_wrapper.OR)
	root.children.append(a)
	root.children.append(b)
	return root
	

def car_comp(car1, car2):
	"""creates a formula (car1 = car2)"""
	# pdb.set_trace()
	result = ast_wrapper.ast(ast_wrapper.CCOMP)
	result.children.append(name(car1))
	result.children.append(name(car2))
	return result


def free():
	"""creates a formula free"""
	return  ast_wrapper.ast(ast_wrapper.FREE)


def res(n):
	"""creates a formula res(a) for car"""
	result = ast_wrapper.ast(ast_wrapper.RES)
	result.children.append(name(n))
	return result
	
def name(n):
	"""returns a NAME-node to which a string of value n is attached"""
	# We have to compare against lower case ego, becaues waxeye capitalised terminals without value, but in our syntax we require lower case letters.
	if n != ast_wrapper.EGO.lower():
		result = ast_wrapper.ast(ast_wrapper.NAME)
		ast_wrapper.add_child(result, n)
	else:
		result = ast_wrapper.ast(ast_wrapper.EGO)
	return result

def clm(n):
	"""creates a formula cl(a) for car"""
	clm = ast_wrapper.ast(ast_wrapper.CLM)
	clm.children.append(name(n))
	return clm

def not_(f):
	"""creates not(f)"""
	troot = ast_wrapper.ast(ast_wrapper.NOT)
	troot.children = [f]
	return troot

def exists(var, type_, f):
	""" creates the formula (forall var in type_.f)"""
	result = ast_wrapper.ast(ast_wrapper.EXISTS)
	result.children.append(name(var))
	ast_wrapper.add_child(result, type_)
	result.children.append(f)
	return result

def forall(var, type_, f):
	""" creates the formula (forall var in type_.f)"""
	result = ast_wrapper.ast(ast_wrapper.FORALL)
	result.children.append(name(var))
	ast_wrapper.add_child(result, type_)
	result.children.append(f)
	return result
	
def as_string(f):
	"""transforms the formula f into a string, s.t. if the string was parsed, we would get the same formula"""
	if f.type == ast_wrapper.RES:
		return 're(' + as_string(f.children[0]) + ')'
	if f.type == ast_wrapper.CLM:
		return 'cl(' + as_string(f.children[0]) + ')'
	elif f.type == ast_wrapper.NAME:
		return f.children[0]
	elif f.type == ast_wrapper.HCHOP:
		return '(' + as_string(f.children[0]) + ' ; ' + as_string(f.children[1]) + ')'
	elif f.type == ast_wrapper.VCHOP:
		return '(' + as_string(f.children[0]) + ' / ' + as_string(f.children[1]) + ')'
	elif f.type == ast_wrapper.AND:
		return '(' + as_string(f.children[0]) + ' & ' + as_string(f.children[1]) + ')'
	elif f.type == ast_wrapper.OR:
		return '(' + as_string(f.children[0]) + ' | ' + as_string(f.children[1]) + ')'
	elif f.type == ast_wrapper.IMPLIES:
		return '(' + as_string(f.children[0]) + ' --> ' + as_string(f.children[1]) + ')'
	elif f.type == ast_wrapper.TRUE:
		return 'true'
	else:
		raise NotImplemented('Operator currently not supported.') 
