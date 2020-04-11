from elasticsearch import Elasticsearch
import pandas as pd
from datetime import datetime
import numpy as np
from progress.bar import IncrementalBar

"""
Use to load data to the server
"""

es = Elasticsearch()

df = pd.read_csv("sudoku.csv")

size = 100

bar = IncrementalBar('Processing', max=size)
for i in range(size):
    doc = {}
    doc[0] = {"quizzes":np.array(df)[i][0],"results:":np.array(df)[i][1],'timestamp': datetime.now()}
    res = es.index(index="sudoku", id=i, body=doc)
    bar.next()
bar.finish()
