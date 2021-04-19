import pygame
import random
from gam2e import Button

pygame.init()
pygame.font.init()
pygame.display.set_caption('My Flappy Bird')

# OBJECTS
sfondo = pygame.image.load('files/sfondo.png')
base = pygame.image.load('files/base.png')
tubo_giu = pygame.image.load('files/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)
uccello = pygame.image.load('files/uccello.png')
gameover = pygame.image.load('files/gameover.png')
tasto_spento = pygame.image.load('files/tasto-spento.png')
tasto_acceso = pygame.image.load('files/tasto-acceso.png')
volume1 = pygame.image.load('files/speaker.png')
volume_a = pygame.transform.scale(volume1, (50, 50))
volume2 = pygame.image.load('files/barred_speaker.png')
volume_b = pygame.transform.scale(volume2, (50, 50))
play = pygame.image.load('files/PlayIcon.png')
play1 = pygame.transform.scale(play, (100, 100))
playbutt = Button(95, 220, play1.get_height(), play1.get_width())
titolo1 = pygame.image.load('files/title.png')
titolo = pygame.transform.scale(titolo1, (192, 51))
schermo = pygame.display.set_mode((288, 512))
# SFX
GMsound = pygame.mixer.Sound('files/Fail-sound-effect.wav')
hit = pygame.mixer.Sound('files/sfx_hit.wav')
point = pygame.mixer.Sound('files/sfx_point.wav')
wing = pygame.mixer.Sound('files/sfx_wing.wav')
click = pygame.mixer.Sound('files/click.wav')
swoosh = pygame.mixer.Sound('files/swoosh.wav')
blower = pygame.mixer.Sound('files/blower.wav')
# OTHER
fps = 60
vel_avanzamento = 3
score_font = pygame.font.SysFont('Standard', 90, bold=True)
high_score_font = pygame.font.Font('files/MinecraftRegular-Bmg3.otf', 35)
text_font1 = pygame.font.Font('files/MinecraftRegular-Bmg3.otf', 30)
text_font2 = pygame.font.Font('files/MinecraftRegular-Bmg3.otf', 20)
high_score = 0
#########################################################################


class Tubo:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)

    def avanza_e_disegna(self):
        self.x -= vel_avanzamento
        schermo.blit(tubo_giu, (self.x, self.y + 210))
        schermo.blit(tubo_su, (self.x, self.y - 210))

    def collisione(self, uccello, uccellox, uccelloy):
        tolleranza = 5
        uccello_lato_dx = uccellox + uccello.get_width() - tolleranza
        uccello_lato_sx = uccellox + tolleranza
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        uccello_lato_su = uccelloy + tolleranza
        uccello_lato_giu = uccelloy + uccello.get_height() - tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx:
            if uccello_lato_su < tubi_lato_su or uccello_lato_giu > tubi_lato_giu:
                game_over()

    def fra_i_tubi(self, uccello, uccellox):
        tolleranza = 1
        uccello_lato_dx = uccellox + uccello.get_width() - tolleranza
        uccello_lato_sx = uccellox + tolleranza
        tubi_lato_dx = self.x + tubo_giu.get_width()
        tubi_lato_sx = self.x
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx:
            return True


def disegna_oggetti():
    schermo.blit(sfondo, (0, 0))
    for t in tubi:
        t.avanza_e_disegna()
    schermo.blit(uccello, (uccellox, uccelloy))
    schermo.blit(base, (basex, 400))
    punti_render = score_font.render(str(punti), True, (255, 255, 255))
    schermo.blit(punti_render, (offset, 445))
    if 49 >= playcount > 0:
        text_render = text_font1.render(str('New High Score!'), True, (255, 140, 0))
        schermo.blit(text_render, (35, 40))


def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(fps)


def inizializza():
    global uccellox, uccelloy, uccello_vely
    global basex
    global tubi
    global punti
    global fra_i_tubi
    global offset
    global playcount
    global starting
    global menu

    uccellox, uccelloy = 60, 150
    uccello_vely = 0
    basex = 0
    punti = 0
    offset = 125
    tubi = [Tubo()]
    fra_i_tubi = False
    playcount = 50
    starting = True


def game_over():
    schermo.blit(gameover, (50, 200))
    aggiorna()
    hit.play()
    GMsound.play()
    ricominciamo = False
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GMsound.stop()
                inizializza()
                ricominciamo = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                swoosh.play()
                inizializza()
                ricominciamo = True
            elif event.type == pygame.QUIT:
                pygame.quit()


inizializza()

running = True
menu = True
starting = True
volume = True
muted = False
while running:
    global uccellox, uccelloy, uccello_vely
    global basex
    global tubi
    global punti
    global fra_i_tubi
    global offset
    global playcount
    if muted:
        pygame.mixer.stop()
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                click.play()
                inizializza()
                menu = False
                starting = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if volume_a.get_rect().collidepoint(x, y):
                    schermo.blit(volume_b, (118, 340))
                    pygame.mixer.stop()
                    muted = True
                    volume = False
                    aggiorna()
                elif play1.get_rect().collidepoint(x, y):
                    click.play()
                    inizializza()
                    menu = False
                    starting = True
            if event.type == pygame.QUIT:
                pygame.quit()

        high_score_render = high_score_font.render(str('High Score: ' + str(high_score)), True, (0, 0, 0))
        sound_render = text_font2.render('Sound', True, (0, 0, 0))
        schermo.fill((255, 255, 255))
        schermo.blit(play1, (95, 220))
        schermo.blit(titolo, (50, 90))
        schermo.blit(high_score_render, (10, 470))
        schermo.blit(sound_render, (115, 385))
        if volume:
            schermo.blit(volume_a, (118, 340))
        aggiorna()

    basex -= vel_avanzamento
    if basex < -45: basex = 0
    uccello_vely += 1
    uccelloy += uccello_vely
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            wing.stop()
            uccello_vely = -10
            wing.play()
        elif event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            swoosh.play()
            menu = True
    if tubi[-1].x < 150: tubi.append(Tubo())

    for t in tubi:
        t.collisione(uccello, uccellox, uccelloy)
    if not fra_i_tubi:
        for t in tubi:
            if t.fra_i_tubi(uccello, uccellox):
                fra_i_tubi = True
                break
    if fra_i_tubi:
        fra_i_tubi = False
        for t in tubi:
            if t.fra_i_tubi(uccello, uccellox):
                fra_i_tubi = True
                break
        if not fra_i_tubi:
            punti += 1
            point.play()
            if high_score < punti:
                high_score = punti
                if playcount == 50:
                    blower.play()
                    playcount -= 1
    if punti >= 10:
        offset = 105
    if uccelloy > 382:
        game_over()
    disegna_oggetti()
    aggiorna()

    if playcount == 50:
        pass
    else:
        playcount -= 1
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                starting = False
                wing.stop()
                uccello_vely = -10
                wing.play()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                swoosh.play()
                menu = True
                starting = False
            elif event.type == pygame.QUIT:
                pygame.quit()

            start_render = text_font2.render('Press UP ARROW to start', True, (0, 0, 0))
            schermo.blit(start_render, (25, 75))
            aggiorna()
