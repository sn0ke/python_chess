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
                    gs.makeMove(move)
                    QuSelected = ()
                    Spielerklickt = []

        drawGameState(screen, gs)
        clock.tick(Max_FPS)
        p.display.flip()


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
