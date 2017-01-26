assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# Important variable for contrain value problem solver
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]# using with only choice
unitlist = row_units + column_units + square_units # use with naked twin
units = dict((s, [u for u in unitlist if s in u]) for s in boxes) # using with only choice 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # using with elimination

"""
Assisting parameter for the diagonal Sudoku
"""
diag_unit = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['I1','H2','G3','F4','E5','D6','C7','B8','A9']]
diag_box = ['A1','B2','C3','D4','E5','F6','G7','H8','I9','I1','H2','G3','F4','D6','C7','B8','A9']

diag_unitlist = {} # store all its peer including itself
diag_peer= {} # store all its peer in the diagonal constrain only
tmp_value = [] # just to help initialize diag_unitlist
for s in diag_box:
    tmp_value = []
    for diag in diag_unit:
        input_diag = diag.copy()
        #print (diag)
        #print ("\n")
        if s in diag:
            if tmp_value:
                tmp_value = tmp_value+input_diag
            else:
                tmp_value = input_diag
    diag_unitlist[s] = tmp_value

for s in diag_box:
    tmp_value = set(diag_unitlist[s])-set([s])
    diag_peer[s] = tmp_value

"""
***Starting of Solution***
"""

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    for sudo_index, sudo_value in  values.items():
            if len(sudo_value) == 1:
                for peer_ind in peers[sudo_index]:
                    value = values[peer_ind].replace(sudo_value,"")
                    assign_value(values,peer_ind,value)
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit_input in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit_input if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    #Good to got
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for index, value in values.items():
        if len(value) == 2:
            # We study only with the case of string len of 2
            # Even though, it can apply to cluster of range more than 2
            for unit_input in units[index]:
                for box in unit_input:
                    # check for every column, row and box unit
                    if (value == values[box])and (not (box == index)):
                        # naked twin found
                        # start elimited string in whether row, column or box
                        for other in unit_input:
                            # eliminate other character according to naked twin definition
                            if (not(index == other))and (not(box == other)):
                                for str_index in range(len(values[index])):
                                    values[other] = values[other].replace(values[index][str_index],"")

    return values


def diagonal_sudoku_solver(values):
    """
    Input: Sudoku puzzle in the form of dictionary
    Output: Sudoku reduce puzzle form along diagonal
    """
    # Elimination along diagonal
    for diag_input in diag_box:
        if len(values[diag_input]) == 1:
            for peer_ind in diag_peer[diag_input]:
                #value = values[peer_ind].replace(sudo_value,"")
                #assign_value(values,peer_ind,value)
                values[peer_ind] = values[peer_ind].replace(values[diag_input],"")
    #only choice along diagonal
    for diag_input in diag_box: # for each units
        for other_test in diag_peer[diag_input]: # for each unit in a units
            str_proc = values[other_test]
            for diag_compare in diag_peer[diag_input]: # for compare to above unit
                if diag_compare is not other_test:
                    for ind in range(len(values[diag_compare])): # elimite the same charater
                        str_proc = str_proc.replace(values[diag_compare][ind],"")
                if str_proc == "":
                    break
            if len(str_proc) > 0:
                values[other_test] = str_proc
    #naked twin along diagonal
    for diag_input in diag_box:
        if len(values[diag_input]) == 2:
            # We study only with the case of string len of 2
            # Even though, it can apply to cluster of range more than 2
            for other_test in diag_peer[diag_input]:
                # check for its peer in diagonal unit
                if (values[diag_input] == values[diag_compare]):
                    # naked twin found
                    # start elimited string in other digonal unit
                    for other in unit_input:
                        # eliminate other character according to naked twin definition
                        if (not(diag_input == other))and (not(diag_compare == other)):
                            for str_index in range(len(values[index])):
                                values[other] = values[other].replace(values[index][str_index],"")
    return values                


def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use naked twin choice strategy here
        values = naked_twins(values)

        # reduce the diagonal constrian solution
        values = diagonal_sudoku_solver(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
"""
def reduce_puzzle_diagonal(values):
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy for diagonal sudoku
        
        # Use the Only Choice Strategy for diagonal sudoku

        # Use naked twin choice strategy here for diagoal sudoku

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values """
 


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    #problem got halted
    if not values:
        return False
    #founded solution
    if all(len(values[s]) == 1 for s in boxes): 
        return values 
    # Chose one of the unfilled square s with the fewest possibilities
    index_fewest = fewest_option(values)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for index in range(len(values[index_fewest])):
        values_replic = values.copy()
        values_replic[index_fewest] = values[index_fewest][index]
        trial_search = search(values_replic)
        if trial_search:
           return trial_search
#find the fewest possible option for box that we can find
def fewest_option(values):
    smallest_len = 100 # init to highest value possible
    smallest_index = '' # need to return the index back not the len of the value
    for key, value in values.items():
        if len(value) < smallest_len and len(value) > 1:
            smallest_len = len(value)
            smallest_index = key
    return smallest_index  

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # conver grid value into values storage in the form of dictionary
    values = grid_values(grid)
    # Using the the diagonal peer in the list above to work with diagonal sudoku
    values = search(values)
    if values:
        return values
    else:
        return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
