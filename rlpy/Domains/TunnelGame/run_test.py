from Game import Game
from GameVis import GameVis
from Tkinter import *

if __name__ == '__main__':
    game = Game(1280, 1024)
    g = GameVis(game)
    mainloop()
