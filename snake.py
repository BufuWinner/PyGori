import pygame
import math
import random

pygame.init()
altezza = 500
larghezza = 500
colonne = 20
fps = 30


class Cubo:
    righe = 20
    w = 500

    def __init__(self, start, dx=1, dy=0, colore=(255, 0, 0)):
        self.pos = start
        self.dx = 1
        self.dy = 0
        self.colore = colore

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.pos = (self.pos[0] + self.dx, self.pos[1] + self.dy)

    def draw(self, surface, eyes=False):
        dis = self.w // self.righe
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(schermo, self.colore, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake:
    corpo = []
    mosse = {}

    def __init__(self, pos, colore):
        self.testa = Cubo(pos)
        self.colore = colore
        self.corpo.append(self.testa)
        self.dx = 1
        self.dy = 1

    def muovere(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

            tasti = pygame.key.get_pressed()
            for _ in tasti:
                if tasti[pygame.K_d]:
                    self.dx = -1
                    self.dy = 0
                    self.mosse[self.testa.pos[:]] = [self.dx, self.dy]

                elif tasti[pygame.K_a]:
                    self.dx = 1
                    self.dy = 0
                    self.mosse[self.testa.pos[:]] = [self.dx, self.dy]

                elif tasti[pygame.K_w]:
                    self.dx = 0
                    self.dy = -1
                    self.mosse[self.testa.pos[:]] = [self.dx, self.dy]

                elif tasti[pygame.K_s]:
                    self.dx = 0
                    self.dy = 1
                    self.mosse[self.testa.pos[:]] = [self.dx, self.dy]

        for i, c in enumerate(self.corpo):
            p = c.pos[:]
            if p in self.mosse:
                mossa = self.mosse[p]
                c.muovere(mossa[0], mossa[1])
                if i == len(self.corpo)-1:
                    self.mosse.pop(p)
            else:
                if c.dx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dx == 1 and c.pos[0] >= c.colonne - 1:
                    c.pos = (0, c.pos[1])
                elif c.dy == 1 and c.pos[1] >= c.colonne - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dy == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dx, c.dy)

    def disegna(self, schermo):
        for i, c in enumerate(self.corpo):
            if i == 0:
                c.draw(schermo, True)
            else:
                c.draw(schermo)

def refresh():
    schermo.fill((50, 50, 50))
    pygame.display.update()
    pygame.time.Clock().tick(fps)
    s.disegna(schermo)

def main():
    global schermo, colonne, fps, s
    altezza = 500
    larghezza = 500
    colonne = 20
    fps = 30
    schermo = pygame.display.set_mode((altezza, larghezza))
    s = Snake((10, 10), (0, 240, 0))
    flag = True
    while flag:
        refresh()
main()
