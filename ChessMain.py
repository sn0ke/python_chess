"""
Dieses Skrip ist das Frontend, es kümmert sich um das GUI, Interaktion mit dem Nutzer,
Darstellung des Bretts und des aktuellen Spielstandes etc.
"""
import pygame as p
import ChessEngine  #, SmartMoveFinder

Board_Breite = Board_Height = 400
MOVE_LOG_PANEL_BREITE = 250
MOVE_LOG_PANEL_HEIGHT = Board_Height
Dimension = 8
SQ_Size = Board_Height // Dimension
Max_FPS = 15
Bilder = {}


def bilder_laden():
    Figuren = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for Figur in Figuren:
        Bilder[Figur] = p.transform.scale(p.image.load("assets/images/"+ Figur + ".png"), (SQ_Size, SQ_Size))

"""
grafik und input
"""

def main():
    p.init()
    screen = p.display.set_mode((Board_Breite + MOVE_LOG_PANEL_BREITE, Board_Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 12, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    bilder_laden()
    running = True
    SQ_Selected = ()
    Spielerklickt = []
    gameOver = False
    playerOne = True #Wahr wenn Mensch weiss spielt, falsch wenn AI spielt
    playerTwo = False #gleiches wie oben aber für schwarz
    while running:
        #humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        humanTurn = True
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # (x, y) Position der Maus im Fenster
                    col = location[0]//SQ_Size
                    row = location[1]//SQ_Size
                    if SQ_Selected == (row, col) or col >= 8:
                        SQ_Selected= ()
                        Spielerklickt = []
                    else:
                        SQ_Selected = (row, col)
                        Spielerklickt.append(SQ_Selected)
                    if len(Spielerklickt) == 2:
                        move = ChessEngine.Move(Spielerklickt[0], Spielerklickt[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                animate = True
                                SQ_Selected = ()
                                Spielerklickt = []
                    if not moveMade:
                        Spielerklickt = [SQ_Selected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    SQ_Selected = ()
                    Spielerklickt = []
                    moveMade = False
                    animate = False
                    gameOver = False

        if not gameOver and not humanTurn: #AI move finder
            AIMove = SmartMoveFinder.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                 animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves,SQ_Selected, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'stalemate' if gs.stalemate else 'Schwarz gewinnt' if gs.whiteToMove else 'Weiss gewinnt' )



        clock.tick(Max_FPS)
        p.display.flip()

def drawGameState(screen, gs, validMoves, SQ_Selected, moveLogFont): #verantwortlich für Grafik in GameState
    drawBoard(screen) # Quadrate zeichnen
    highlightQuadrate(screen, gs, validMoves, SQ_Selected)
    drawFiguren(screen, gs.board)  # Figuren zeichnen auf den Quadraten
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen): #Schachbrett
    global colors
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))


def highlightQuadrate(screen, gs, validMoves, SQ_Selected): #Quadrate (gewählt & für Züge) werden angeleuchtet
    if SQ_Selected != ():
        r, c, = SQ_Selected
        if gs.board[r][c][0]== ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_Size, SQ_Size))
            s.set_alpha(100)
            s.fill(p.Color('red'))
            screen.blit(s, (c*SQ_Size, r*SQ_Size))
            s.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startColumn == c:
                    screen.blit(s, (move.endColumn*SQ_Size, move.endRow*SQ_Size))



def drawFiguren(screen, board): #Figuren, Position
    for r in range(Dimension):
        for c in range(Dimension):
            Figur = board[r][c]
            if Figur != "--":
                screen.blit(Bilder[Figur], p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(Board_Breite, 0, MOVE_LOG_PANEL_BREITE, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts =[]
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + "." + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + " "
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    TextY = padding
    for i in range(len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, 0, p.Color('Black'))
        textlocation = moveLogRect.move(padding, padding)
        screen.blit(textObject, textlocation)
        TextY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock): #Animation von Zug
    global colors
    dR = move.endRow - move.startRow
    dC = move.endColumn - move.startColumn
    frameperSquare = 10
    frameCount = (abs(dR) + abs(dC)) * frameperSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startColumn + dC*frame/frameCount )
        drawBoard(screen)
        drawFiguren(screen, board)
        color = colors[(move.endRow + move.endColumn)% 2]
        endSquare = p.Rect(move.endColumn*SQ_Size, move.endRow*SQ_Size, SQ_Size, SQ_Size)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            #if move.enPassant:
             #   enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
              #  endSquare = p.Rect(move.endColumn * SQ_Size, enPassantRow * SQ_Size, SQ_Size, SQ_Size)
            screen.blit(Bilder[move.pieceCaptured], endSquare)
        if move.pieceMoved != '--':
            screen.blit(Bilder[move.pieceMoved], p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))
        p.display.flip()
        clock.tick(60)


def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 30, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textlocation = p.Rect(0, 0, Breite, Height).move(Breite/2 -textObject.get_Breite()/2, Height/2 - textObject.get_Height()/2)
    screen.blit(textObject, textlocation)



if __name__ == "__main__":
    main()