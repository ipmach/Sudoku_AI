import pandas as pd
import numpy as np
from game import game
from interface import interface
from elasticsearch import Elasticsearch
from solverIA import solver_sudoku
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

"""
For now this is the main
"""
es = Elasticsearch()

try:
    res = es.search(index="sudoku", body={"query": {"match_all": {}}})
    numberSudokus = res['hits']['total']['value']
except:
    print("sudoku server not found, initialize elastic search")
    exit()


print("Welcome, choose game type:")
print("1) Player do sudoku")
print("2) IA do sudoku")
print("3) IA sudoku stadistics")
while(True): #Initial menu
    try:
        game_mode = input("Select number: ")
        assert game_mode in ["1","2","3"], "Must be one of the options"
        break
    except:
        print("You must choose one of the options")

game_mode = int(game_mode)

if game_mode <3:
    print("Total number of sudokus: {0}".format(numberSudokus))
    print("Choose which one to play")
    while(True): #Initial menu
        try:
            number_game = input("Select number: ")
            number_game = int(number_game)
            assert number_game in np.arange(numberSudokus) , "Must be one of the options"
            break
        except:
            print("You must choose one of the options")

    res = es.get(index="sudoku", id=number_game)
    a_ini = res['_source']['0']['quizzes']
    a_end = res['_source']['0']['results:']

    ini = np.asarray(list(map(lambda x: int(x),list(a_ini))))
    end = np.asarray(list(map(lambda x: int(x),list(a_end))))
    b = game(init_state = ini, final_state = end)


    if game_mode == 1:  #Player mode
        interface(600,600,b, chibi = False)
    else: #IA
        b.solve_IA()
        interface(600,600,b, chibi = False, game_solve = b.are_legal())
else:
    print("Total number of sudokus: {0}".format(numberSudokus))
    print("Choose how many")
    while(True): #Initial menu
        try:
            number_games = input("Select number: ")
            number_games = int(number_games)
            assert number_games <= numberSudokus , "Must be one of the options"
            break
        except:
            print("You must choose  smaller or equal of {0}".format(numberSudokus))

    list_games = []
    start = time.time()
    for i in range(number_games):
        print("Game {0}/{1}".format(i+1,number_games))
        res = es.get(index="sudoku", id=i)
        a_ini = res['_source']['0']['quizzes']
        ini = np.asarray(list(map(lambda x: int(x),list(a_ini))))
        b = game(init_state = ini)
        b.solve_IA()
        aux = b.are_legal()
        print(" Is correct ", aux)
        list_games.append(aux)
    end = time.time()
    print("=============================")
    print("Game || Result")
    for i in range(len(list_games)):
        print(i+1,"    || ",list_games[i])
    print("Time: ", end - start)
