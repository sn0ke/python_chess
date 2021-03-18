"""
Dieses Skrip ist das Frontend, es kümmert sich um das GUI, Interaktion mit dem Nutzer,
Darstellung des Bretts und des aktuellen Spielstandes etc.
"""
import pygame as p
import ChessEngine

Breite = Height = 400
Dimension = 8
SQ_Size = Height // Dimension
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
    screen = p.display.set_mode((Breite, Height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False

    print(gs.board)
    bilder_laden()
    running = True
    QuSelected = ()
    Spielerklickt = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) Position der Maus im Fenster
                col = location[0]//SQ_Size
                row = location[1]//SQ_Size
                if QuSelected == (row, col):
                    QuSelected = ()
                    Spielerklickt = []
                else:
                    QuSelected = (row, col)
                    Spielerklickt.append(QuSelected)
                if len(Spielerklickt) == 2:
                    move = ChessEngine.Move(Spielerklickt[0], Spielerklickt[1], gs.board)
                    print(move.getSchachNotation())
                    for i in range(len(validMoves)):
                     if move == validMoves[i]:
                        gs.makeMove(move)
                        moveMade = True
                        QuSelected = ()
                        Spielerklickt = []
                if not moveMade:
                        Spielerklickt = [QuSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(Max_FPS)
        p.display.flip()

def highlightQuadrate(screen, gs, validMoves, QuSelected):
    if QuSelected != ():
        r, c, = QuSelected
        if gs.board[r][c][0]== ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_Size, SQ_Size))
            s.set_alpha(100)
            s.fill(p.Color('red'))
            screen.blit(s, (c*SQ_Size, r*SQ_Size))
            s.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s(move.endCol*SQ_Size, move.endRow*SQ_Size))

def drawGameState(screen, gs):
    drawBoard(screen) # Quadrate zeichnen

    drawFiguren(screen, gs.board)  # Figuren zeichnen auf den Quadraten


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))


def drawFiguren(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            Figur = board[r][c]
            if Figur != "--":
                screen.blit(Bilder[Figur],p.Rect(c*SQ_Size, r*SQ_Size, SQ_Size, SQ_Size))





if __name__ == "__main__":
    main()
