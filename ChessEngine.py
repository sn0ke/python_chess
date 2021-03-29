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

	# Diese Funktion führt Züge aus mithilfe der Move() Klasse
	def makeMove(self, move):
		self.board[move.startRow][move.startColumn] = "--"
		self.board[move.endRow][move.endColumn] = move.pieceMoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove

	# mit dieser Funktion kann ein Zug rückgängig gemacht werden
	def undoMove(self):
		if len(self.moveLog) != 0:
			lastmove = self.moveLog[-1]
			self.board[lastmove.startRow][lastmove.startColumn] = lastmove.pieceMoved
			self.board[lastmove.endRow][lastmove.endColumn] = lastmove.pieceCaptured
			self.whiteToMove = not self.whiteToMove
			del self.moveLog[-1]

	# Listet alle Züge auf, welche erlaubt sind für einen GameState
	def getValidMoves(self):
		return self.getPossibleMoves()

	# Listet alle möglichen Züge auf, ohne auf Schach zu achten
	def getPossibleMoves(self):
		print(self.board)
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				colour = self.board[r][c][0]
				piece = self.board[r][c][1]
				if (colour == "w" and self.whiteToMove) or (colour == "b" and not self.whiteToMove):
					if piece == "p":
						self. getPawnMoves(r, c, moves)
					if piece == "R":
						self.getRookMoves(r, c, moves)
					if piece == "N":
						self.getNiteMoves(r, c, moves)
					if piece == "B":
						self.getBishopMoves(r, c, moves)
					if piece == "Q":
						self.getQueenMoves(r, c, moves)
					if piece == "K":
						self.getKingMoves(r, c, moves)
		print(len(moves))
		return moves

	def getPawnMoves(self, r, c, moves):
		if self.whiteToMove:
			if self.board[r-1][c] == "--": #überprüfe, ob sich 1 Feld vor dem Bauern eine Figur befindet
				moves.append(Move((r, c), (r-1, c), self.board))
				if self.board[r-2][c] == "--" and r ==6: #überprüfe, ob sich 2 Felder vor dem Bauern eine Figur befindet und ob er sich noch auf seiner Startposition befindet
					moves.append(Move((r, c), (r-2, c), self.board))

			if 0 <= c <= 7:
				colLeft = c-1
				colRight = c+1
				if colLeft >= 0:
					if self.board[r - 1][colLeft][0] == "b":
						moves.append(Move((r, c), (r - 1, colLeft), self.board))
				if colRight <= 7:
					if self.board[r-1][colRight][0] == "b" and colRight <= 7:
						moves.append(Move((r, c), (r-1, colRight), self.board))

		if not self.whiteToMove:
			if self.board[r+1][c] == "--": #überprüfe, ob sich 1 Feld vor dem Bauern eine Figur befindet
				moves.append(Move((r, c), (r+1, c), self.board))
				if self.board[r+2][c] == "--" and r ==1: #überprüfe, ob sich 2 Felder vor dem Bauern eine Figur befindet und ob er sich noch auf seiner Startposition befindet
					moves.append(Move((r, c), (r+2, c), self.board))

			if 0 <= c <= 7:
				colLeft = c-1
				colRight = c+1
				if colLeft >= 0:
					if self.board[r+1][colLeft][0] == "w":
						moves.append(Move((r, c), (r+1, colLeft), self.board))
				if colRight <= 7:
					if self.board[r+1][colRight][0] == "w":
						moves.append(Move((r, c), (r+1, colRight), self.board))

	def getRookMoves(self, r, c, moves):
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		opponentColor = "b" if self.whiteToMove else "w"
		for d in directions:
			for i in range(1, 7):
				horDir = c + (i * d[1])
				vertDir = r + (i * d[0])
				if 0 <= horDir <=7 and 0 <= vertDir <=7:
					if self.board[vertDir][horDir] == "--":
						moves.append(Move((r, c), (vertDir, horDir), self.board))
					elif self.board[vertDir][horDir][0] == opponentColor:
						moves.append(Move((r, c), (vertDir, horDir), self.board))
						break
					else:
						break
				else:
					break
		return moves

	def getNiteMoves(self, r, c, moves):
		directions = [(2, 1), (2, -1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2)] # alle Bewegungsrichtungen
		opponentColor = "b" if self.whiteToMove else "w"
		for d in directions: # für jede Richtung prüfen, ob der Zug möglich ist, und falls ja zur moves Liste hinzufügen
			horDir = c + d[1]
			vertDir = r + d[0]
			if 0 <= horDir <= 7 and 0 <= vertDir <= 7: # ist der Zug überhaupt möglich / auf dem Feld
				if self.board[vertDir][horDir] == "--":
					moves.append(Move((r, c), (vertDir, horDir), self.board))
				elif self.board[vertDir][horDir][0] == opponentColor:
					moves.append(Move((r, c), (vertDir, horDir), self.board))
		return moves

	def getBishopMoves(self, r, c, moves):
		directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
		opponentColor = "b" if self.whiteToMove else "w"
		for d in directions:
			for i in range(1, 7):
				horDir = c + (i * d[1])
				vertDir = r + (i * d[0])
				if 0 <= horDir <= 7 and 0 <= vertDir <= 7:
					if self.board[vertDir][horDir] == "--":
						moves.append(Move((r, c), (vertDir, horDir), self.board))
					elif self.board[vertDir][horDir][0] == opponentColor:
						moves.append(Move((r, c), (vertDir, horDir), self.board))
						break
					else:
						break
				else:
					break
		return moves

	def getQueenMoves(self, r, c, moves):
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
		opponentColor = "b" if self.whiteToMove else "w"
		for d in directions:
			for i in range(1, 7):
				horDir = c + (i * d[1])
				vertDir = r + (i * d[0])
				if 0 <= horDir <= 7 and 0 <= vertDir <= 7:
					if self.board[vertDir][horDir] == "--":
						moves.append(Move((r, c), (vertDir, horDir), self.board))
					elif self.board[vertDir][horDir][0] == opponentColor:
						moves.append(Move((r, c), (vertDir, horDir), self.board))
						break
					else:
						break
				else:
					break
		return moves

	def getKingMoves(self, r, c, moves):
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
		opponentColor = "b" if self.whiteToMove else "w"
		for d in directions:
			horDir = c + d[1]
			vertDir = r + d[0]
			if 0 <= horDir <= 7 and 0 <= vertDir <= 7:
				if self.board[vertDir][horDir] == "--":
					moves.append(Move((r, c), (vertDir, horDir), self.board))
				elif self.board[vertDir][horDir][0] == opponentColor:
					moves.append(Move((r, c), (vertDir, horDir), self.board))
		return moves

class Move():
	# Diese Klasse kümmert sich um die Züge der Figuren
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
		self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn

	# Überschreiben der euqals Methode, welche dazu verwendet wird um herauszufinden, ob es sich bei zwei Instanzen um die selbe handelt.
	# Da wir ja nicht überprüfen möchten, ob zwei verglichene Klassen exakt die selbe Klasse sind, sondern nur ob der Zug der selbe ist, lösen wir dies mit einer einfachen MoveID.
	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID
		else:
			return False

	#Diese Funktion nimmt einen Zug, und wandelt die Notation von array[][] zu B2B4 Schachnotation um
	def getChessNotation(self):
		return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

	#Diese Funktion wandelt mit Hilfe der Dictionnaries von weiter oben Zeilen und Spalten Notation in Schachnotation um
	def getRankFile(self, r,c):
		return self.colsToFiles[c] + self.rowsToRanks[r]











