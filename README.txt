# MLSLS Tool

Prototype to analyse logical formulas of a logic I developed in my PhD.

This script works with Python v2.7.13. Further, for parsing it uses the included  parser generator waxeye v0.8.0 (see https://waxeye.org/) and the SMT solver Z3 v4.8.4 from Microsoft compiled for 64bit architectures.

USAGE
=====

Linux (x64)
_____

1. Unzip the file.
2. Ensure that check_static_mlsl.sh is executable (with chmod u+x check_static_mlsl.sh)
3. With 
	check_static_mlsl.sh "python2.7" "formula" "model"
where python2.7 is the executable of python version 2.7 you can check if the MLSL model in the file model satisfies the MLSL formula in the file formula.

If you want to use the inner guts of the program, please ensure to have
 - ${WORK_DIR}/lib/z3/bin/python and ${WORK_DIR}/lib/waxeye in your PYTHONPATH and
 - ${WORK_DIR}/lib/z3/bin in yout PATH.

	

MODEL SYNTAX
============

Comments begin with "/*" and end with "*/".
At the start a model contains the definition of its horizontal extension, the lanes and the ego-car (in this order). Afterwards, it contains the claims and reservations of the cars. Claims and reservations are distinguished by their surrounding parentheses/brackets. That is, a reservation has the form "(Int, Float, Float, Name)", and a claim has the form "[Int, Float, Float, Name]". With Int the lane of the claim or the reservation is given, with Float we define the extension as an interval (the first value is the absolute position along the extension and the second value is the length of the extension), and with Name the car to whom this reservation or claim belongs. In EBNF the syntax is
	model ::= 
			"ext = [" Float","  Float"]"
			"lanes = [" Int","  Int"]"
			"ego = " Name
			("(Int, Float, Float, Name)" | "[Int, Float, Float, Name]")*

		
FORMULA SYNTAX
==============

In formulas a variable is represented by its name. Further, every variable has a type, which is "exts", "lanes" or "cars". A Term either is a value or a variable.

The syntax is given by the EBNF
	F ::= F "/" F | F ";" F | F "-->" F | F "<->" F | "!" F | F "|" F | F "&" F | "exists" Name "in" Type "." F | "forall" Name "in" Type "." F | <@ F @> |
	"true" | "false" | "length" ~ FloatTerm |  "height" ~ IntTerm | "re(" Name | "ego" ")" | "cl(" Name | "ego" ")"
where
	Type ::= "exts" | "lanes" | "cars"
and
	~ ::= "<" | "<=" | "=" | ">=" | ">"
	
The operators in MLSL formulas are vertical chop, horizontal chop, implication, iff, negation, disjunction, conjunction, existential quantification, universal quantification and the somewhere modality.
The atoms are the boolean constants true, false, comparison of the length of the extension and comparison of the width (or height) of the lanes.
Additionally we have atoms for reservations and claims of a car, where the car is given by a variable or the special ego constant.
