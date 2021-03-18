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
        self.whiteToMove = True
        self.moveLog = []

    #Startaufstellung initialisieren
    def init_board(self, board):
        for i in range(8):
            board[0][i] = "b" + start[i]
            board[1][i] = "bP"
            board[6][i] = "wP"
            board[7][i] = "w" + start[i]


gs = GameState()

print(gs.board)