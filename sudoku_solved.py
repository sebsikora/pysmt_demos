
from pysmt.shortcuts import Symbol, Plus, Equals, GE, LE, And, Int, AllDifferent, get_model
from pysmt.typing import INT

import numpy as np

# Starting board position

board = np.array([0, 0, 0, 0, 0, 0, 0, 4, 5,
				  7, 0, 0, 0, 0, 8, 0, 0, 9,
				  0, 0, 0, 4, 0, 9, 8, 0, 0,
				  0, 1, 2, 0, 5, 0, 6, 0, 0,
				  0, 0, 3, 0, 6, 0, 9, 0, 0,
				  0, 7, 4, 0, 8, 0, 1, 0, 0,
				  0, 0, 0, 2, 0, 7, 4, 0, 0,
				  8, 0, 0, 0, 0, 3, 0, 0, 1,
				  0, 0, 0, 0, 0, 0, 0, 7, 2])

board = board.reshape(9, 9)

# Create symbols to represent the 81 unique locations on the sudoku board
#
# We'll use a numpy array to simplify slicing out ranges for our constraints later. The pysmt functions don't seem to like taking
# ndarray as arguments so we'll need to use .flatten().tolist() to convert the sliced ranges into a flat list when we want to pass them.

cells = np.array([Symbol(str(i), INT) for i in range(81)]).reshape(9, 9)

# All symbols must be in range 1 - 9
valid_range = And([And(GE(c, Int(1)), LE(c, Int(9))) for c in cells.flatten().tolist()])

# Each 3x3 sub-region of the 9x9 game board can only contain each value once
no_3x3_repeats_1 = AllDifferent(cells[0:3, 0:3].flatten().tolist())
no_3x3_repeats_2 = AllDifferent(cells[3:6, 0:3].flatten().tolist())
no_3x3_repeats_3 = AllDifferent(cells[6:9, 0:3].flatten().tolist())
no_3x3_repeats_4 = AllDifferent(cells[0:3, 3:6].flatten().tolist())
no_3x3_repeats_5 = AllDifferent(cells[3:6, 3:6].flatten().tolist())
no_3x3_repeats_6 = AllDifferent(cells[6:9, 3:6].flatten().tolist())
no_3x3_repeats_7 = AllDifferent(cells[0:3, 6:9].flatten().tolist())
no_3x3_repeats_8 = AllDifferent(cells[3:6, 6:9].flatten().tolist())
no_3x3_repeats_9 = AllDifferent(cells[6:9, 6:9].flatten().tolist())

no_3x3_repeats = And(no_3x3_repeats_1, no_3x3_repeats_2, no_3x3_repeats_3, no_3x3_repeats_4, no_3x3_repeats_5,
					 no_3x3_repeats_6, no_3x3_repeats_7, no_3x3_repeats_8, no_3x3_repeats_9)

# Each column can only contain each value once
no_col_repeats_1 = AllDifferent(cells[0:9, 0].flatten().tolist())
no_col_repeats_2 = AllDifferent(cells[0:9, 1].flatten().tolist())
no_col_repeats_3 = AllDifferent(cells[0:9, 2].flatten().tolist())
no_col_repeats_4 = AllDifferent(cells[0:9, 3].flatten().tolist())
no_col_repeats_5 = AllDifferent(cells[0:9, 4].flatten().tolist())
no_col_repeats_6 = AllDifferent(cells[0:9, 5].flatten().tolist())
no_col_repeats_7 = AllDifferent(cells[0:9, 6].flatten().tolist())
no_col_repeats_8 = AllDifferent(cells[0:9, 7].flatten().tolist())
no_col_repeats_9 = AllDifferent(cells[0:9, 8].flatten().tolist())

no_col_repeats = And(no_col_repeats_1, no_col_repeats_2, no_col_repeats_3, no_col_repeats_4, no_col_repeats_5,
					 no_col_repeats_6, no_col_repeats_7, no_col_repeats_8, no_col_repeats_9)

# Each row can only contain each value once
no_row_repeats_1 = AllDifferent(cells[0, 0:9].flatten().tolist())
no_row_repeats_2 = AllDifferent(cells[1, 0:9].flatten().tolist())
no_row_repeats_3 = AllDifferent(cells[2, 0:9].flatten().tolist())
no_row_repeats_4 = AllDifferent(cells[3, 0:9].flatten().tolist())
no_row_repeats_5 = AllDifferent(cells[4, 0:9].flatten().tolist())
no_row_repeats_6 = AllDifferent(cells[5, 0:9].flatten().tolist())
no_row_repeats_7 = AllDifferent(cells[6, 0:9].flatten().tolist())
no_row_repeats_8 = AllDifferent(cells[7, 0:9].flatten().tolist())
no_row_repeats_9 = AllDifferent(cells[8, 0:9].flatten().tolist())

no_row_repeats = And(no_row_repeats_1, no_row_repeats_2, no_row_repeats_3, no_row_repeats_4, no_row_repeats_5,
					 no_row_repeats_6, no_row_repeats_7, no_row_repeats_8, no_row_repeats_9)

# Initial starting position on the board
equality_relationships = []
for row in range(9):
	for col in range(9):
		if board[row, col] != 0:
			equality_relationships.append(Equals(cells[row, col], Int(int(board[row, col]))))
starting_positions = And(equality_relationships)

#~starting_positions = And(Equals(cells[0, 7], Int(4)),
						 #~Equals(cells[0, 8], Int(5)),
						 #~Equals(cells[1, 0], Int(7)),
						 #~Equals(cells[1, 5], Int(8)),
						 #~Equals(cells[1, 8], Int(9)),
						 #~Equals(cells[2, 3], Int(4)),
						 #~Equals(cells[2, 5], Int(9)),
						 #~Equals(cells[2, 6], Int(8)),
						 #~Equals(cells[3, 1], Int(1)),
						 #~Equals(cells[3, 2], Int(2)),
						 #~Equals(cells[3, 4], Int(5)),
						 #~Equals(cells[3, 6], Int(6)),
						 #~Equals(cells[4, 2], Int(3)),
						 #~Equals(cells[4, 4], Int(6)),
						 #~Equals(cells[4, 6], Int(9)),
						 #~Equals(cells[5, 1], Int(7)),
						 #~Equals(cells[5, 2], Int(4)),
						 #~Equals(cells[5, 4], Int(8)),
						 #~Equals(cells[5, 6], Int(1)),
						 #~Equals(cells[6, 3], Int(2)),
						 #~Equals(cells[6, 5], Int(7)),
						 #~Equals(cells[6, 6], Int(4)),
						 #~Equals(cells[7, 0], Int(8)),
						 #~Equals(cells[7, 5], Int(3)),
						 #~Equals(cells[7, 8], Int(1)),
						 #~Equals(cells[8, 7], Int(7)),
						 #~Equals(cells[8, 8], Int(2)))

formula = And(valid_range, no_3x3_repeats, no_col_repeats, no_row_repeats, starting_positions)

# Pass the constraint to the solver

model = get_model(formula)

if model:
	for row in range(9):
		row_string = ''
		for col in range(9):
			row_string += str(model.get_value(cells[row, col])) + ' '
		print(row_string)
		print()

else:
	print("Denied!")
	
