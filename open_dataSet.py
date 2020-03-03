import pandas as pd
import numpy as np
from game import game
from interface import interface

"""
For now this is the main
"""

a = np.load("data_set.npy", allow_pickle = True)
ini = np.asarray(list(map(lambda x: int(x),list(a[5][0]))))
end = np.asarray(list(map(lambda x: int(x),list(a[5][1]))))
b = game(init_state = ini, final_state = end)
interface(600,600,b, False)
#boxtext = TextBox((0,widths + 10,150,30),command=dumb,clear_on_enter=True,inactive_on_enter=False)
