
from pysmt.shortcuts import Symbol, Plus, Equals, GE, LE, And, Int, AllDifferent, get_model
from pysmt.typing import INT

# Create a 3x3 grid of integer symbols, one for each puzzle unknown.

cells = {}
for col in ['a', 'b', 'c']:
	for row in ['1', '2', '3']:
		key = col + row
		cells[key] = Symbol(key, INT)

# Create symbol contraints

valid_range = And([And(GE(c, Int(1)), LE(c, Int(9))) for c in cells.values()])

no_repeats = AllDifferent(cells.values())

sum_area_1 = Equals(Plus(cells['a1'], cells['b1'], cells['b2']), Int(17))
sum_area_2 = Equals(Plus(cells['c1'], cells['c2'], cells['c3']), Int(16))
sum_area_3 = Equals(Plus(cells['a2'], cells['a3'], cells['b3']), Int(12))

circle_sum_1 = Equals(Plus(cells['a1'], cells['b1'], cells['a2'], cells['b2']), Int(21))
circle_sum_2 = Equals(Plus(cells['b1'], cells['c1'], cells['b2'], cells['c2']), Int(29))
circle_sum_3 = Equals(Plus(cells['a2'], cells['b2'], cells['a3'], cells['b3']), Int(21))
circle_sum_4 = Equals(Plus(cells['b2'], cells['c2'], cells['b3'], cells['c3']), Int(22))

# Combine the constraints into the overll constraint

formula = And(valid_range, no_repeats, sum_area_1, sum_area_2, sum_area_3, circle_sum_1, circle_sum_2, circle_sum_3, circle_sum_4)

# Pass the constraint to the solver

model = get_model(formula)

if model:
	print(model)
else:
	print("Denied!")
	
