import numpy as np
import copy

class game:
    """
    Class were the logic and the states of the game are save
    """

    def __init__(self,init_state=None, final_state = None, name = "No name"):
        self.init_state = copy.copy(init_state)
        self.actual_state = copy.copy(init_state)
        self.final_state = copy.copy(final_state)
        self.name = "No name"

    def convert_state_ini(self):
        """
        Return a nxn matrix of the initial board
        """
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

    def is_win(self):
        """
        Check if the game is finish
        """
        return all(np.equal(0,self.actual_state.reshape(-1)))
