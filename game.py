import numpy as np
import copy
from solverIA import solver_sudoku


class game:
    """
    Class were the logic and the states of the game are save
    """

    def __init__(self,init_state=None, final_state = None, name = "No name"):
        self.init_state = copy.copy(init_state)
        self.actual_state = copy.copy(init_state)
        self.final_state = copy.copy(final_state)
        self.name = "No name"

    def convert_state_ini(self,dimension3 = False):
        """
        Return a nxn matrix of the initial board
        """
        if dimension3:
            return self.init_state.reshape((1,9,9))
        return self.init_state.reshape((9,9))

    def convert_state_final(self):
        """
        Return a nxn matrix of the final board (solution)
        """
        return self.final_state.reshape((9,9))

    def convert_state_actual(self):
        """
        Return a nxn matrix of the actual board
        """
        return self.actual_state.reshape((9,9))

    def is_initial_state(self,x,y):
        """
        Check if the position is part of the initial state
        """
        return True if self.init_state.reshape((9,9))[x][y] > 0 else False

    def insert_number(self, x,y,value):
        """
        Insert a number in the actual state board
        x,y: coordinates
        """
        M = self.actual_state.reshape((9,9))
        M[x][y] = value
        self.actual_state= M.reshape(-1)

    def is_legal(self,x,y,value):
        """
        Check if the move is legal.
        The move follow the rules to be consider a correct move.
        x,y: coordinates
        value: number for the cell in the board
        """
        value = int(value)
        M = self.actual_state.reshape((9,9))
        row = any(np.equal(value,M[x]))
        col = any(np.equal(value,np.transpose(M)[y]))
        index = np.array([1,4,7])
        center_x = index[np.argmin(abs(x - index))]
        center_y = index[np.argmin(abs(y - index))]
        M = np.transpose(M[center_x -1: center_x + 2])[center_y -1: center_y + 2]
        square = any(np.equal(value,M.reshape(-1)))
        if any([row,col,square]):
            return False
        return True

    def are_legal(self):
        """
        Check if all the moves done are legal
        """
        m = self.convert_state_actual()
        legal = True
        for i in range(9):
            for j in range(9):
                aux = self.is_legal(i,j,m[i][j])
                if aux:
                    print("Move x:{0} y:{1} value:{2} is ilegal".format(i,j,m[i][j]))
                if legal:
                    aux = legal
        return legal

    def is_win(self):
        """
        Check if the game is finish
        """
        return all(np.equal(0,self.actual_state.reshape(-1)))

    def solve_IA(self):
        """
        Use the IA to solve the sudoku
        """
        IA = solver_sudoku()
        self.actual_state = np.reshape(IA.solve(self.convert_state_ini(dimension3 = True)),-1)
