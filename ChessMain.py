"""
Dieses Skrip ist das Frontend, es kümmert sich um das GUI, Interaktion mit dem Nutzer,
Darstellung des Bretts und des aktuellen Spielstandes etc.
"""
import pygame as p
import ChessEngine

Breite = Höhe = 400
Dimension = 8
Quadrat_Grösse = Höhe // Dimension
Max_FPS = 15
Bilder = {}


def bilder_laden():
    Figuren = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for Figur in Figuren:
        Bilder[Figur] = p.transform.scale(p.image.load("assets/images/"+ Figur + ".png"), (Quadrat_Grösse, Quadrat_Grösse))

"""
grafik und input
"""

def main():
    p.init()
    screen = p.display.set_mode((Breite, Höhe))
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
            if e.type == p-QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//Quadrat_Grösse
                row = location[1]//Quadrat_Grösse
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
    drawBoard(screen) #Quadrate zeichnen

    drawFiguren(screen, gs.board) #Figuren zeichnen auf den Quadraten


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("black")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*Quadrat_Grösse, r*Quadrat_Grösse, Quadrat_Grösse, Quadrat_Grösse))


def drawFiguren(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            Figur = board[r][c]
            if Figur != "--":
                screen.blit(Bilder[Figuren],p.Rect(c*Quadrat_Grösse, r*Quadrat_Grösse, Quadrat_Grösse, Quadrat_Grösse))





if __name__ == "__main__":
    main()
