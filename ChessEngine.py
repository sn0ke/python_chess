"""
Dieses Skript ist sozusagen das "backend" des Spiels. Es haltet die aktuelle Spielpositionen,
ist für die Einhaltung der Regeln zuständig, führt ein Movelog etc.
"""

start = ["R", "N", "B", "K", "Q", "B", "N", "R"]

class GameState():
    def __init__(self):
        # 8x8 Brett mit "--" Platzhaltern erstellen
        self.board = [["--" for i in range(8)] for i in range(8)]
        #Brett füllen
        self.init_board(self.board)
        print(self.board)
        self.whiteToMove = True
        self.moveLog = []

    #Startaufstellung initialisieren
    def init_board(self, board):
        for i in range(8):
            board[1][i] = "b" + start[i]
            board[2][i] = "bP" + start[i]
            board[7][i] = "wP" + start[i]
            board[8][i] = "w" + start[i]



