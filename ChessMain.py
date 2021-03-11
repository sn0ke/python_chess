"""
Dieses Skrip ist das Frontend, es kümmert sich um das GUI, Interaktion mit dem Nutzer,
Darstellung des Bretts und des aktuellen Spielstandes etc
"""
import pygame as p
from Python Chess import ChessEngine

Breite = Höhe = 400
Dimension = 8
Quadrat_Grösse = Höhe // Dimension
Max_FPS = 15
Bilder = {}

def Bilder_laden():
    Figuren = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for Figur in Figuren:
        Bilder[Figur] = p.transform.scale(p.Bild.laden("images/"+ Figur + ".png"), (Quadrat_Grösse, Quadrat_Grösse))

"""
grafik und input
"""
def main():
    p.init()
    screen = p.display.set_mode(Breite, Höhe)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    print(gs.board)
    Bilder_laden()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p-QUIT:
                running = False
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




    main()