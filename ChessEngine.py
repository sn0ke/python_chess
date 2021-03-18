"""
Dieses Skript ist sozusagen das "backend" des Spiels. Es haltet die aktuelle Spielpositionen,
ist für die Einhaltung der Regeln zuständig, führt ein Movelog etc.
"""

setup = ["R", "N", "B", "K", "Q", "B", "N", "R"]

class GameState():
    def __init__(self):
        # 8x8 Brett mit "--" Platzhaltern erstellen
        self.board = [["--" for i in range(8)] for i in range(8)]
        #Brett füllen
        self.init_board(self.board)
        self.whiteToMove = True
        self.moveLog = []

    #setupaufstellung generieren
    def init_board(self, board):
        for i in range(8):
            board[0][i] = "b" + setup[i]
            board[1][i] = "bp"
            board[6][i] = "wp"
            board[7][i] = "w" + setup[i]

    def makeMove(self, move):



class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startColumn = startSQ[1]
        self.endRow = endSQ[0]
        self.endColumn = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startColumn]
        self.pieceCaptured = board[self.endRow][self.endColumn]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)


    def geRankFile(self, r,c)
        return self.colsToFiles[c] + self.rowsToRanks[r]











