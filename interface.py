from pygame.locals import *
import pygame
import numpy as np
from textbox import TextBox

def initBoard(ttt):
    """
    Initialize the board
    """
    global  height,width
    # set up the background surface
    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))
    ## PRINCIPAL LINES
    # draw the grid lines
    size = 9
    # vertical lines...
    high = height/size
    for i in range(1,size):
        pygame.draw.line (background, (220,220,220), (i*high, 0), (i*high, height), 4)

    # horizontal lines...
    large = width/size
    for i in range(1,size):
        pygame.draw.line (background, (220,220,220), (0, i*large), (width, i*large),4)
    ##SECONDARY LINES
    # draw the grid lines
    size = 3
    # vertical lines...
    high = height/size
    for i in range(0,size+1):
        line_size =4
        if i == 0 or i == size:
            line_size =8
        pygame.draw.line (background, (0,0,0), (i*high, 0), (i*high, height), line_size)

    # horizontal lines...
    large = width/size
    for i in range(0,size+1):
        line_size =4
        if i == 0 or i == size:
            line_size =8
        pygame.draw.line (background, (0,0,0), (0, i*large), (width, i*large),line_size)

    return background

def boardPos (mouseX, mouseY):
    """
    Given a set of coordinates from the mouse, determine which board space.
    (row, column) the user clicked in.
    """
    global height,width
    size = 9
    # determine the row the user clicked
    high = height/size
    for i in range(1,size+1):
        if mouseY < high*i:
            row = i -1
            break
    # determine the column the user clicked
    large = width/size
    if mouseY > width:
        return (None,None)
    for i in range(1,size+1):
        if mouseX < large*i:
            col = i -1
            break
    # return the tuple containg the row & column
    return (row, col)

def getCoordinate(num_grid):
    """
    Get the coordinate in an axis of the board.
    num_gid: position in the grid
    """
    if num_grid == 0:
        num = 8
    elif num_grid <4:
        num =  69 *num_grid
    elif num_grid <7:
        num_grid = num_grid - 4
        num = 270 + 69 *num_grid
    else:
        num_grid = num_grid - 7
        num = 470 + 69 *num_grid
    return num

def insertNumber(ttt, x_grid, y_grid,value,path_numbers):
    """
    Insert a number in the board
    x_grid, y_grid: coordinates in the grid
    value: number that is going to be insert it
    path_numbers: path of icons to use to insert this number
    """
    x = getCoordinate(x_grid)
    y = getCoordinate(y_grid)
    #ttt.blit(pygame.image.load('numbers_anime/' + str(value)+'.jpg'), (x, y))
    ttt.blit(pygame.image.load('numbers/'+path_numbers+'/' + str(value)+'.jpg'), (x, y))
    return ttt

def initStateBoard(board, game_board):
    """
    Initialize the initial state of the board
    board: board interface
    game_board: object of the actual game
    """
    global path_numbers
    m = game_board.convert_state_ini()
    index = np.nonzero(m)
    for i in range(len(index[0])):
            x = index[0][i]
            y = index[1][i]
            board = insertNumber(board, x,y, m[x][y],path_numbers)
    return board

def renderBoardAgain(board, game_board, showFinish = False):
    """
    Render the board again.
    showFinish: render the board with the final correct result
    """
    global path_numbers
    if showFinish:
        m = game_board.convert_state_final()
    else:
        m = game_board.convert_state_actual()
    index = np.nonzero(m)
    for i in range(len(index[0])):
            x = index[0][i]
            y = index[1][i]
            board = insertNumber(board, x,y, m[x][y],path_numbers)
    return board

def showBoard (ttt, board,boxtext):
    """
    Display the update board.
    """
    #drawStatus (board)
    boxtext.update()
    boxtext.draw(board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()

def dumb(id, value):
    """
    Function use in the textbox to interact with the interface
    """
    global board, grid_x, grid_y,path_numbers, game_board
    try:
        if value == "rwby": #Easter egg
            path_numbers = "chibi"
            renderBoardAgain(board, game_board)
            return None
        if value == "final": #Get final result
            path_numbers = "correct"
            renderBoardAgain(board, game_board,showFinish = True)
            return None
        value = int(value)
        if (0 <value< 10): #check if is a correct value
            if grid_x > -1: #grid_x is -1 if the user point in a initial state
                if not game_board.is_legal(grid_x,grid_y,value): #check if is a legal value
                    insertNumber(board,grid_x, grid_y,value,"wrong")
                else:
                    insertNumber(board,grid_x, grid_y,value,path_numbers)
                    #only update the state if is a correct/legal value
                    game_board.insert_number(grid_x,grid_y,value)
                    #print(game_board.convert_state_actual())
            else:
                print("Inital state cant be change")
        else:
            print("invalid number")
    except:
        print("invalid symbol")

def renderText(board,x,y,game_board):
    """
    Function use to render the text of the game
    x,y: coordinates choose by the player
    game_board: object of the actual game
    """
    global grid_x
    if not game_board.is_initial_state(x,y):
        message = "Selected position x: " + str(x) + " y: " + str(y)
    else: #if you cant modifie that cell because is a initial value
        message = "You can't change this one"
        grid_x = -1 #move grix_x value to -1
    font = pygame.font.Font(None, 30)
    text = font.render(message, 10, (0, 0, 0))
    board.fill ((250, 250, 250), (0, height, width, 250))
    board.blit(text, (15, width + 15))
    return board

def interface(heights, widths, game_boards, chibi = False, game_solve = None):
  """
  Function that render and allow to interact with the interface
  heights, widths: sizes of the board
  game_board: object of the actual game
  chibi: if True icons start with easter egg
  """
  global height, width, grid_x, grid_y, board,path_numbers, game_board
  grid_x = 0
  grid_y = 0
  game_board = game_boards
  path_numbers = "initial"
  if chibi:
      path_numbers = "chibi"
  height = heights
  width = widths
  pygame.init()
  ttt = pygame.display.set_mode ((height, width + 50))
  pygame.display.set_caption ('Sudoku')
  board = initBoard (ttt)
  board = initStateBoard(board,game_board)
  board = renderText(board,grid_x,grid_y,game_board)
  boxtext = TextBox((300,widths + 10,150,30),command=dumb,clear_on_enter=True,inactive_on_enter=False)
  running = 1
  if game_solve == None: #Solve by human
      if not chibi:
         path_numbers = "insert"
      while (running == 1):
        #Events created by the player
        for event in pygame.event.get():
            if event.type is QUIT:
                running = 0
            elif event.type is MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                grid_y_aux,grid_x_aux = boardPos(mouseX, mouseY)
                if grid_x_aux != None:
                    grid_x = grid_x_aux
                    grid_y = grid_y_aux
                    board = renderText(board,grid_x,grid_y,game_board)
        if game_board.is_win():
            path_numbers = "correct"
            renderBoardAgain(board,game_board)

        boxtext.get_event(event)
        showBoard (ttt, board,boxtext)
  else: #Solve by Machine
      if game_solve:
          path_numbers = "correct"
      else:
          path_numbers = "wrong"
      renderBoardAgain(board,game_board)
      while (running == 1):
          for event in pygame.event.get():
              if event.type is QUIT:
                  running = 0
          boxtext.get_event(event)
          showBoard (ttt, board,boxtext)
