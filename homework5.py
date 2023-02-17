############################################################
# CIS 5210: Homework 5
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math
import os

student_name = "Jingjing Bai"

############################################################
# Sudoku Solver
############################################################

fileDir = os.path.dirname(os.path.realpath('__file__'))

def read_board(path):
    board={}
    ind = 0
    filename = os.path.join(fileDir, path)
    filehandle = open(filename)
    cell_list = []
    for line in filehandle:
        line = line.rstrip().lstrip()
        cell_list.append(line)
    filehandle.close()
    for i in cell_list:
        for element in i:
            if element == '*':
                board[cell_temp[ind]] = set([1,2,3,4,5,6,7,8,9])
            else:
                board[cell_temp[ind]] = set([int(element)])
            ind +=1
    return board
#b = read_board("Documents/GitHub/jingjingb-cis5210-hw5/homework5_sudoku/hard1.txt")
#print(b)




def sudoku_cells():
    return [(i, j) for i in range(9) for j in range(9)]

same_row = lambda cell1, cell2: cell1[0] == cell2[0]
same_col = lambda cell1, cell2: cell1[1] == cell2[1]
same_sub_square = lambda cell1, cell2: math.floor(cell1[0]/3) == math.floor(cell2[0]/3) and math.floor(cell1[1]/3) == math.floor(cell2[1]/3)

def sudoku_arcs():
    return [(c1, c2) for c1 in sudoku_cells() for c2 in sudoku_cells() if (same_row(c1, c2) or same_col(c1, c2) or same_sub_square(c1, c2)) and c1 != c2]

class Sudoku(object):
    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def get_values(self, cell):
        return self.board.get(cell)
    
    def remove_inconsistent_values(self, cell1, cell2):
        if len(self.get_values(cell2)) == 1:
            v = list(self.get_values(cell2))[0]
            if v in self.board[cell1]:
                self.board[cell1].remove(v)
                return True
        return False

    def ac3_arcs(self, cell):
        return [(c, cell) for c in sudoku_cells() if (same_row(c, cell) or same_col(c, cell) or same_sub_square(c, cell)) and len(self.get_values(c)) > 1 and c != cell]

    def infer_ac3(self):
        queue = []
        for c1, c2 in self.ARCS:
            queue.append((c1, c2))
        while len(queue) > 0:
            # Go through all the arcs.
            cell1, cell2 = queue.pop(0)
            # remove cell2 value from cell1's set.
            if self.remove_inconsistent_values(cell1, cell2):
                for new_c1, new_c2 in self.ac3_arcs(cell1):
                    queue.append((new_c1, new_c2))

    def is_solved(self):
        for cell in self.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True

    def infer_improved(self):
        get_sub_square = lambda cell: [(i, j) for i in range(math.floor(cell[0]/3)*3, math.floor(cell[0]/3)*3+3) for j in range(math.floor(cell[1]/3)*3, math.floor(cell[1]/3)*3+3)]
        sub_square_qualify = lambda v, cell: all([v not in self.get_values(sub) for sub in get_sub_square(cell) if sub != cell])
        row_qualify = lambda v, cell: all([v not in self.get_values((cell[0], col)) for col in range(9) if col != cell[1]])
        col_qualify = lambda v, cell: all([v not in self.get_values((row, cell[1])) for row in range(9) if row != cell[0]])
        # reduced marked the special ideas beyond ac3
        reduced = 1
        while reduced:
            reduced = 0
            self.infer_ac3()
            if self.is_solved():
                return self
            for cell in [(i, j) for i in range(0,9) for j in range(0,9)]:
                if len(self.board[cell]) > 1:
                    # check the cell - value will qualify the special idea.
                    for value in self.board[cell]:
                        # The other cells in the sub squre can't take this value Or
                        # The other cells in the same row can't take this value. Or The other cells in the same col can't take this value.
                        if sub_square_qualify(value, cell) or  row_qualify(value, cell) or col_qualify(value, cell):                              
                            self.board[cell] = set([value])
                            reduced = 1
                            break
                    if reduced:
                        break

    def cell_choice_w_minset(self):
        min = 10
        next_cell = ()
        for cell in self.CELLS:
            # traverse all cells to get the cell with min choices (not 1)
            if len(self.board[cell]) < min and len(self.board[cell]) > 1:
                if len(self.board[cell]) == 2:
                    return cell
                next_cell = cell
                min = len(self.board[cell])
        return next_cell

    def successors_for_cell_value_choice(self, next_cell):
        board_copy = copy.deepcopy(self.board)
        for value in list(self.board[next_cell]):
            board_copy[next_cell] = set([value])
            result_board = copy.deepcopy(board_copy)
            yield Sudoku(result_board)

    def infer_with_guessing(self):
      #set up dfs stack
      stack = [self]
      while stack:
        sudoku = stack.pop()
        sudoku.infer_improved()
        if sudoku.is_solved():
            self.board = sudoku.board
            return sudoku
        if all([len(sudoku.board[cell]) > 0 for cell in sudoku.CELLS]):        
            next_cell = sudoku.cell_choice_w_minset()
            for successor in sudoku.successors_for_cell_value_choice(next_cell):
                stack.append(successor)
        
        

############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = "4"

feedback_question_2 = """
understand the sukudo ideas
"""

feedback_question_3 = """
the order of questions. They guided the systematical way to solve the puzzle.
"""
