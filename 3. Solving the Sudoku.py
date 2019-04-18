
'''
Below you can find an implementation of the Tree data structure to solve any Sudoku puzzle.
I created this to practice working with trees and using recursion.

It takes an unsolved Sudoku as input (represented as an array) and output the solved Sudoku.

It works as follows:

The method that solves the Sudoku, is named get_solution:
-It calls the info_matrix function, which returns the the size of the Sudoku, the indexes of the zero values and the number
of empty cells.
-Based on this info, the method create_tree creates a tree with depth -1 equal to the amount of empty cells in the Sudoku
and with each parent having an amount of children that is equal to the size of the Sudoku.
For example, consider the following Sudoku:
       [[1., 2., 3.],
       [2., 0., 0.],
       [3., 1., 2.]]
       
The empty cells are represented by a zero, there are 2 empty cells and the size of the Sudoku is 3, thus the 
corresponding tree looks as follows:

         0
  /      |     \
  1------2------3
 /|\    /|\    /|\
1-2-3--1-2-3--1-2-3



-Next, we go trough the tree to find the solution, using the go_through_tree method:
We start at the first level. At the first level, we determine the possible values for the first empty cell in the Sudoku.
Per node (which represents a value), we check whether this value could be the correct value for that cell.
A value is correct if this value is not present in the same row and column (this is checked by the legit_value method).
If yes, we recursively go to the next level (aka next empty cell in the Sudoku) and again run through all possible values.
If the node value cannot be the value for the cell, we omit the children nodes of that node.
If we reach the end of the tree, we have completed all the empty cells in the Sudoku without violating the rules
and we return the completed Sudoku.
    
    
    
'''






class SudokuTree():
    
    #Each possible value for an empty/zero Sudoku cell, is represented by a node. 
    #The children nodes are the possible values for the next empty/zero cell in the Sudoku.
    class Cell():
        def __init__(self,value):
            self.value = value
            self.children = []
    
    
    def __init__(self):
        self.root = self.Cell(None)
        
    #returns size, location of zeros and amount of zeros of a Sudoku matrix
    def info_matrix(self,matrix):
        size =  len(matrix)
        index_zeros = []
        for row in range(len(matrix)): 
            for column in range(len(matrix)):
                if matrix[row][column] ==0:
                    index_zeros.append([row,column])
        amount_zeros= len(index_zeros)         
        return size, index_zeros, amount_zeros
        
    #create tree with depth = amount of zero Sudoku cells -1 and size = size of the Sudoku game (eg size = 5 when Sudoku is 5x5)
    def create_tree(self, depth,size,cell= None):
        if  cell == None:
            cell = self.root
            for rootchild in range(1,size+1):
                cell.children.append(self.Cell(rootchild))
            depth -= 1
            for grandchild in cell.children:
                self.create_tree(depth = depth, size = size, cell = grandchild)
        
        elif cell!= None and depth > 0:
            for child in range(1,size+1):
                cell.children.append(self.Cell(child))
            depth -= 1
            for grandchild in cell.children:
                self.create_tree(depth = depth, size = size, cell = grandchild)
                


    #Starting at the first zero cell, it checks whether a value is valid 
    #If it is valid, this is repeated for the next zero cell
    #If it is not valid, this value is not considered anymore for this zero cell
    def go_through_tree(self, matrix, index_zeros, correct_values, cell):
        if cell == None:
            cell = self.root
        for child in cell.children:
            if (self.legit_value(child, index_zeros,matrix)):
                correct_values.append(child.value)
                matrix[index_zeros[0][0]][index_zeros[0][1]] = child.value
                if len(child.children) >0:
                    self.go_through_tree(matrix,index_zeros[1:], correct_values, cell = child)               
                else:
                    print(matrix)
                    break
            else:
                pass
                
    #Checks whether a value is valid. This is when the same value is not present in the same row and column
    def legit_value(self,child,index_zeros,matrix):
        horizontal = matrix[index_zeros[0][0]]
        vertical = []
        for horizontalindex in range(len(matrix)):
            vertical.append(matrix[horizontalindex][index_zeros[0][1]])
        if child.value not in horizontal and child.value not in vertical:
            return True
        else:
            return False
    
    def get_solution(self,matrix):
        size, index_zeros, amount_zeros = self.info_matrix(matrix)
        self.create_tree(depth = amount_zeros, size = size)
        self.go_through_tree(matrix,index_zeros, correct_values = [], cell =None)