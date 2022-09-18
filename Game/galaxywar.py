# -*- coding: utf-8 -*-

# Game developers:
# Gustavo Corrêa da Cunha
# João Pedro Scremin Ramos
# Lucas Costa Valença

import pygame, random

pygame.init()
pygame.mixer.init()

# Screen size, title and icon variables
altura = 600
largura = 800
titulo = "Galaxy War"
icone = pygame.image.load("_images/score_icone.png")
pygame.display.set_icon(icone)
pygame.display.set_caption(titulo)
tela = pygame.display.set_mode((largura, altura))

# Background game modes images
fundo1 = pygame.image.load("_images/fundo1.png").convert_alpha()
fundo2 = pygame.image.load("_images/fundo3.png").convert_alpha()
fundo3 = pygame.image.load("_images/fundo2.png").convert_alpha()

# Laser images
laser = pygame.image.load('_images/laser1.png').convert_alpha()
laser2 = pygame.image.load('_images/laser1.png').convert_alpha()

# Classes
class Display:
    def __init__(self):
        self.seletor = 0
        self.seletor_options = False
        self.atualizar = 0
        self.contador_pause = 0
        self.contador_cima = 0
        self.contador_baixo = 0
        self.contador_tiro = 0
        self.instructions = False
        self.som = False
        self.music = True
        self.sound_effects = True
        self.fundo_y = -5400
        self.fundo_y2 = -5400
        self.fundo_y3 = -5400
        self.vel = 0
        self.loop = True
        self.verificador = 0
        self.font_type = pygame.font.Font("_fonts/8-bit pusab.TTF", 12)
        self.font_type2 = pygame.font.Font("_fonts/8-bit pusab.TTF", 20)

    def reset(self):
        self.seletor = 0
        self.seletor_options = False
        self.atualizar = 0
        self.contador_pause = 0
        self.contador_cima = 0
        self.contador_baixo = 0
        self.contador_tiro = 0
        self.instructions = False
        self.som = False
        self.fundo_y = -5400
        self.fundo_y2 = -5400
        self.fundo_y3 = -5400
        self.loop = True
        self.vel = 0
        creditos.set_pos(0, 600)

display = Display()

class Estados:
    def __init__(self, image, sound, state):
        self.image = pygame.image.load(image).convert_alpha()
        self.sound = pygame.mixer.Sound(sound)
        self.state = state

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def mov(self):
        self.pos_y -= 0.5
        if self.pos_y < -1330:
            creditos.sound.fadeout(300)
            menu.state = True
            creditos.state = False
            reset_geral()

menu = Estados("_images/menu/menu_fundo.png", "_sounds/menu8bit.wav", True)
arcade = Estados("_images/menu/menu_fundo.png", "_sounds/spinalcoaster.wav", False)
creditos = Estados("_images/creditos/creditos.png", "_sounds/creditos8bit.wav", False)
creditos.set_pos(0, 600)
multiplayer = Estados("_images/menu/menu_fundo.png", "_sounds/spinalcoaster.wav", False)
options = Estados("_images/menu/options_on-on.png", "_sounds/menu8bit.wav", False)
pause = Estados("_images/menu/pause.png", "_sounds/menu8bit.wav", False)
game_over = Estados("_images/menu/game_over.png", "_sounds/game_over.wav", False)

class Personagem(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, vel, image, image2, life, life_image, display_pos_x, display_pos_y, pu_pos_x, pu_pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_x_base = pos_x
        self.pos_y_base = pos_y
        self.vel = vel
        self.image = pygame.image.load(image).convert_alpha()
        self.image2 = pygame.image.load(image2).convert_alpha()
        self.life = life
        self.life_image = pygame.image.load(life_image).convert_alpha()
        self.pontos = 0
        self.display_pontos = display.font_type.render(str(self.pontos), True, (255, 255, 255))
        self.display_pos_x = display_pos_x
        self.display_pos_y = display_pos_y
        self.display_text = ["LIFE:", "SCORE:"]
        self.display_life = display.font_type.render(self.display_text[0], True, (255, 255, 255))
        self.display_score = display.font_type.render(self.display_text[1], True, (255, 255, 255))
        self.life_image_pos_x = display_pos_x + 70
        self.life_image_pos_y = display_pos_y - 5
        self.state = True
        self.pu_pos_x = pu_pos_x
        self.pu_pos_y = pu_pos_y

    def reset(self):
        self.life = 3
        self.pontos = 0
        self.pos_x = self.pos_x_base
        self.pos_y = self.pos_y_base
        self.vel = 5
        self.state = True

    def update(self):
        if self.state:
            tela.blit(self.image, (self.pos_x, self.pos_y))
        else:
            tela.blit(self.image2, (self.pos_x, self.pos_y))
        tela.blit(self.display_score, (self.display_pos_x, self.display_pos_y + 30))
        self.display_pontos = display.font_type.render(str(self.pontos), True, (255, 255, 255))
        tela.blit(self.display_pontos, (self.display_pos_x + 80, self.display_pos_y + 30))
        tela.blit(self.display_life, (self.display_pos_x, self.display_pos_y))

        if self.life > 0:
            tela.blit(self.life_image, (self.life_image_pos_x, self.life_image_pos_y))
        if self.life > 1:
            tela.blit(self.life_image, (self.life_image_pos_x + 35, self.life_image_pos_y))
        if self.life > 2:
            tela.blit(self.life_image, (self.life_image_pos_x + 70, self.life_image_pos_y))
        if self.life < 1:
            self.state = False

nave = Personagem(300, 500, 5, "_images/character.png", "_images/characterb.png", 3, "_images/life.png", 20, 15, 20, 80)
nave2 = Personagem(400, 500, 5, "_images/character2.png", "_images/character2b.png",  3, "_images/life2.png", 600, 15, 600, 80)

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, vel, image):
        self.pos_x = random.randint(10, 700)
        self.pos_y = -100
        self.vel = vel
        self.image = pygame.image.load(image).convert_alpha()
        self.gerar = True
        self.mov_esq = False

    def reset(self):
        self.gerar = True
        self.mov_esq = False
        self.setPosition()
        self.vel = 3

    def setPosition(self):
        self.pos_x = random.randint(10, 700)
        self.pos_y = -100

    def mov(self):
        if self.pos_y > 700:
            if display.sound_effects == True:
                enemy_pass.sound.play()
            if arcade.state:
                nave.life -= 1
            else:
                if nave.life > nave2.life:
                    nave.life -= 1
                else:
                    nave2.life -= 1

            self.gerar = True
            self.pos_y = -100

        if self.gerar == True:
            self.setPosition()
            self.moviment = random.randint(1, 3)
            self.gerar = False
        else:
            tela.blit(self.image, (self.pos_x, self.pos_y))
            if self.moviment == 1:
                self.pos_y += self.vel

            if self.moviment == 2:
                self.pos_y += self.vel - 0.5
                if self.mov_esq == True:
                    self.pos_x += self.vel
                else:
                    self.pos_x -= self.vel

                if self.pos_x < 0:
                    self.mov_esq = True
                if self.pos_x > 700:
                    self.mov_esq = False

            if self.moviment == 3:
                if 250 < self.pos_y < 350:
                    self.pos_y += self.vel + 40
                else:
                    self.pos_y += self.vel

enemy = Inimigo(2, "_images/enemy1.png")
enemy2 = Inimigo(2, "_images/enemy3.png")
enemy3 = Inimigo(2, "_images/enemy4.png")
enemy4 = Inimigo(2, "_images/enemy5.png")
enemy5 = Inimigo(2, "_images/enemy1.png")

class Efeitos_Sonoros():
    def __init__(self, sound):
        self.sound = pygame.mixer.Sound(sound)


tiro = Efeitos_Sonoros("_sounds/tiro.wav")
colide = Efeitos_Sonoros("_sounds/enemy_death.wav")
powerup = Efeitos_Sonoros("_sounds/power_up2.wav")
life_charge = Efeitos_Sonoros("_sounds/power_up.wav")
sistema = Efeitos_Sonoros("_sounds/sistema.wav")
enemy_pass = Efeitos_Sonoros("_sounds/enemy_pass.wav")

class Power_Ups():
    def __init__(self, image_100, image_70, image_30):
        self.image_100 = pygame.image.load(image_100).convert_alpha()
        self.image_70 = pygame.image.load(image_70).convert_alpha()
        self.image_30 = pygame.image.load(image_30).convert_alpha()

puVel = Power_Ups("_images/power_ups/pu.png","_images/power_ups/pu_70.png", "_images/power_ups/pu_30.png")

# Menu images
menu100 = pygame.image.load("_images/menu/menu_100.png").convert_alpha()
menu80 = pygame.image.load("_images/menu/menu_80.png").convert_alpha()
menu60 = pygame.image.load("_images/menu/menu_60.png").convert_alpha()
menu40 = pygame.image.load("_images/menu/menu_40.png").convert_alpha()
menu20 = pygame.image.load("_images/menu/menu_20.png").convert_alpha()
options_TF = pygame.image.load("_images/menu/options_on-off.png").convert_alpha()
options_FT = pygame.image.load("_images/menu/options_off-on.png").convert_alpha()
options_FF = pygame.image.load("_images/menu/options_off-off.png").convert_alpha()
game_instructions = pygame.image.load("_images/menu/game_instructions.png").convert_alpha()

# General variables
clock = pygame.time.Clock()
Laser = False
Laser2 = False
dL = False
speed = False
speed2 = False
startCDS2 = False
contCD12 = 0
contD12 = 0
contD22 = 0
startCDS = False
startCDL = False
startCDL2 = False
contCD1 = 0
contD1 = 0
contCD2 = 0
contCD22 = 0
contD2 = 0
verificador1 = 0
verificador2 = 0

# Functions
def menu_function(seletor, atualizar):
    if (seletor % 4 == 0) and (atualizar % 2 == 0):
        pygame.draw.rect(tela, (0, 0, 0), (250, 210, 300, 40))
    if (seletor % 4 == 1) and (atualizar % 2 == 0):
        pygame.draw.rect(tela, (0, 0, 0), (250, 280, 300, 40))
    if (seletor % 4 == 2) and (atualizar % 2 == 0):
        pygame.draw.rect(tela, (0, 0, 0), (250, 340, 300, 40))
    if (seletor % 4 == 3) and (atualizar % 2 == 0):
        pygame.draw.rect(tela, (0, 0, 0), (250, 410, 300, 40))

def selecao_estado(seletor, seletor_options):
    if seletor_options == False:
        if seletor % 4 == 0:
            menu.sound.fadeout(300)
            display.som = False
            arcade.state = True
            menu.state = False
        if seletor % 4 == 1:
            menu.sound.fadeout(300)
            display.som = False
            multiplayer.state = True
            menu.state = False
        if seletor % 4 == 2:
            menu.sound.fadeout(300)
            display.som = False
            creditos.state = True
            menu.state = False
        if seletor % 4 == 3:
            display.seletor_options = True
            options.state = True
            menu.state = False
    else:
        if seletor % 4 == 0:
            if display.music == True:
                display.music = False
                menu.sound.stop()
            else:
                display.music = True
                menu.sound.play()
                display.som = True
        if seletor % 4 == 1:
            if display.sound_effects == True:
                display.sound_effects = False
            else:
                display.sound_effects = True
        if seletor % 4 == 2:
            display.instructions = True
        if seletor % 4 == 3:
            display.seletor_options = False
            options.state = False
            menu.state = True

def options_fundo(music, sound):
    if music == True:
        if sound == True:
            tela.blit(options.image, (0, 0))
        else:
            tela.blit(options_TF, (0, 0))
    else:
        if sound == True:
            tela.blit(options_FT, (0, 0))
        else:
            tela.blit(options_FF, (0, 0))

# Collision
def colisao():
    global display, tiroLaser

    if nave.state:
        # Detects collision between ship 1 and enemy 1
        if (nave.pos_x < enemy.pos_x < nave.pos_x + 65 or nave.pos_x < enemy.pos_x + 80 < nave.pos_x + 65 or
            enemy.pos_x < nave.pos_x < enemy.pos_x + 85 or enemy.pos_x < nave.pos_x + 85 < enemy.pos_x + 100) and \
                (nave.pos_y < enemy.pos_y < nave.pos_y + 50 or nave.pos_y < enemy.pos_y + 60 < nave.pos_y + 60 or
                 enemy.pos_y < nave.pos_y < enemy.pos_y + 50 or enemy.pos_y < nave.pos_y + 60 < enemy.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave.life -= 1
            enemy.gerar = True

        # Detects collision between ship 1 and enemy 2
        if (nave.pos_x < enemy2.pos_x < nave.pos_x + 65 or nave.pos_x < enemy2.pos_x + 80 < nave.pos_x + 65 or
            enemy2.pos_x < nave.pos_x < enemy2.pos_x + 85 or enemy2.pos_x < nave.pos_x + 85 < enemy2.pos_x + 100) and \
                (nave.pos_y < enemy2.pos_y < nave.pos_y + 50 or nave.pos_y < enemy2.pos_y + 60 < nave.pos_y + 60 or
                 enemy2.pos_y < nave.pos_y < enemy2.pos_y + 50 or enemy2.pos_y < nave.pos_y + 60 < enemy2.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave.life -= 1
            enemy2.gerar = True

        # Detects collision between ship 1 and enemy 3
        if (nave.pos_x < enemy3.pos_x < nave.pos_x + 65 or nave.pos_x < enemy3.pos_x + 80 < nave.pos_x + 65 or
            enemy3.pos_x < nave.pos_x < enemy3.pos_x + 85 or enemy3.pos_x < nave.pos_x + 85 < enemy3.pos_x + 100) and \
                (nave.pos_y < enemy3.pos_y < nave.pos_y + 50 or nave.pos_y < enemy3.pos_y + 60 < nave.pos_y + 60 or
                 enemy3.pos_y < nave.pos_y < enemy3.pos_y + 50 or enemy3.pos_y < nave.pos_y + 60 < enemy3.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave.life -= 1
            enemy3.gerar = True

        # Detects collision between ship 1 and enemy 4
        if (nave.pos_x < enemy4.pos_x < nave.pos_x + 65 or nave.pos_x < enemy4.pos_x + 80 < nave.pos_x + 65 or
            enemy4.pos_x < nave.pos_x < enemy4.pos_x + 85 or enemy4.pos_x < nave.pos_x + 85 < enemy4.pos_x + 100) and \
                (nave.pos_y < enemy4.pos_y < nave.pos_y + 50 or nave.pos_y < enemy4.pos_y + 60 < nave.pos_y + 85 or
                 enemy4.pos_y < nave.pos_y < enemy4.pos_y + 50 or enemy4.pos_y < nave.pos_y + 60 < enemy4.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave.life -= 1
            enemy4.gerar = True

        # Detects collision between ship 1 and enemy 5
        if (nave.pos_x < enemy5.pos_x < nave.pos_x + 65 or nave.pos_x < enemy5.pos_x + 80 < nave.pos_x + 65 or
            enemy5.pos_x < nave.pos_x < enemy5.pos_x + 85 or enemy5.pos_x < nave.pos_x + 85 < enemy5.pos_x + 100) and \
                (nave.pos_y < enemy5.pos_y < nave.pos_y + 50 or nave.pos_y < enemy5.pos_y + 60 < nave.pos_y + 85 or
                 enemy5.pos_y < nave.pos_y < enemy5.pos_y + 50 or enemy5.pos_y < nave.pos_y + 60 < enemy5.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave.life -= 1
            enemy5.gerar = True

    if nave2.state:
        # Detects collision between ship 2 and enemy 1
        if (nave2.pos_x < enemy.pos_x < nave2.pos_x + 65 or nave2.pos_x < enemy.pos_x + 80 < nave2.pos_x + 65 or
            enemy.pos_x < nave2.pos_x < enemy.pos_x + 85 or enemy.pos_x < nave2.pos_x + 85 < enemy.pos_x + 100) and \
                (nave2.pos_y < enemy.pos_y < nave2.pos_y + 50 or nave2.pos_y < enemy.pos_y + 60 < nave2.pos_y + 85 or
                 enemy.pos_y < nave2.pos_y < enemy.pos_y + 50 or enemy.pos_y < nave2.pos_y + 60 < enemy.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave2.life -= 1
            enemy.gerar = True

        # Detects collision between ship 2 and enemy 2
        if (nave2.pos_x < enemy2.pos_x < nave2.pos_x + 65 or nave2.pos_x < enemy2.pos_x + 80 < nave2.pos_x + 65 or
            enemy2.pos_x < nave2.pos_x < enemy2.pos_x + 85 or enemy2.pos_x < nave2.pos_x + 85 < enemy2.pos_x + 100) and \
                (nave2.pos_y < enemy2.pos_y < nave2.pos_y + 50 or nave2.pos_y < enemy2.pos_y + 60 < nave2.pos_y + 85 or
                 enemy2.pos_y < nave2.pos_y < enemy2.pos_y + 50 or enemy2.pos_y < nave2.pos_y + 60 < enemy2.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave2.life -= 1
            enemy2.gerar = True

        # Detects collision between ship 2 and enemy 3
        if (nave2.pos_x < enemy3.pos_x < nave2.pos_x + 65 or nave2.pos_x < enemy3.pos_x + 80 < nave2.pos_x + 65 or
            enemy3.pos_x < nave2.pos_x < enemy3.pos_x + 85 or enemy3.pos_x < nave2.pos_x + 85 < enemy3.pos_x + 100) and \
                (nave2.pos_y < enemy3.pos_y < nave2.pos_y + 50 or nave2.pos_y < enemy3.pos_y + 60 < nave2.pos_y + 85 or
                 enemy3.pos_y < nave2.pos_y < enemy3.pos_y + 50 or enemy3.pos_y < nave2.pos_y + 60 < enemy3.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave2.life -= 1
            enemy3.gerar = True

        # Detects collision between ship 2 and enemy 4
        if (nave2.pos_x < enemy4.pos_x < nave2.pos_x + 65 or nave2.pos_x < enemy4.pos_x + 80 < nave2.pos_x + 65 or
            enemy4.pos_x < nave2.pos_x < enemy4.pos_x + 85 or enemy4.pos_x < nave2.pos_x + 85 < enemy4.pos_x + 100) and \
                (nave2.pos_y < enemy4.pos_y < nave2.pos_y + 50 or nave2.pos_y < enemy4.pos_y + 60 < nave2.pos_y + 85 or
                 enemy4.pos_y < nave2.pos_y < enemy4.pos_y + 50 or enemy4.pos_y < nave2.pos_y + 60 < enemy4.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave2.life -= 1
            enemy4.gerar = True

        # Detects collision between ship 2 and enemy 5
        if (nave2.pos_x < enemy5.pos_x < nave2.pos_x + 65 or nave2.pos_x < enemy5.pos_x + 80 < nave2.pos_x + 65 or
            enemy5.pos_x < nave2.pos_x < enemy5.pos_x + 85 or enemy5.pos_x < nave2.pos_x + 85 < enemy5.pos_x + 100) and \
                (nave2.pos_y < enemy5.pos_y < nave2.pos_y + 50 or nave2.pos_y < enemy5.pos_y + 60 < nave2.pos_y + 85 or
                 enemy5.pos_y < nave2.pos_y < enemy5.pos_y + 50 or enemy5.pos_y < nave2.pos_y + 60 < enemy5.pos_y + 60):
            if display.sound_effects == True:
                colide.sound.play()
            nave2.life -= 1
            enemy5.gerar = True

# Ship 1 laser collision
def colisao2():

    if (xl < enemy.pos_x < xl + 30 or xl < enemy.pos_x + 80 < xl + 30 or enemy.pos_x < xl < enemy.pos_x + 85 or
        enemy.pos_x < xl + 30 < enemy.pos_x + 100) and (yl < enemy.pos_y < yl + 800 or
        yl < enemy.pos_y + 60 < yl + 800 or enemy.pos_y < yl < enemy.pos_y + 50 or
        enemy.pos_y < yl + 800 < enemy.pos_y + 60) and enemy.pos_y > -50:
        enemy.gerar = True
        nave.pontos += 1

    if (xl < enemy2.pos_x < xl + 30 or xl < enemy2.pos_x + 80 < xl + 30 or enemy2.pos_x < xl < enemy2.pos_x + 85 or
        enemy2.pos_x < xl + 30 < enemy2.pos_x + 100) and (yl < enemy2.pos_y < yl + 800 or
        yl < enemy2.pos_y + 60 < yl + 800 or enemy2.pos_y < yl < enemy2.pos_y + 50 or
        enemy2.pos_y < yl + 800 < enemy2.pos_y + 60) and enemy2.pos_y > -50:
        enemy2.gerar = True
        nave.pontos += 1

    if (xl < enemy3.pos_x < xl + 30 or xl < enemy3.pos_x + 80 < xl + 30 or enemy3.pos_x < xl < enemy3.pos_x + 85 or
        enemy3.pos_x < xl + 30 < enemy3.pos_x + 100) and (yl < enemy3.pos_y < yl + 800 or
        yl < enemy3.pos_y + 60 < yl + 800 or enemy3.pos_y < yl < enemy3.pos_y + 50 or
        enemy3.pos_y < yl + 800 < enemy3.pos_y + 60) and enemy3.pos_y > -50:
        enemy3.gerar = True
        nave.pontos += 1

    if (xl < enemy4.pos_x < xl + 30 or xl < enemy4.pos_x + 80 < xl + 30 or enemy4.pos_x < xl < enemy4.pos_x + 85 or
        enemy4.pos_x < xl + 30 < enemy4.pos_x + 100) and (yl < enemy4.pos_y < yl + 800 or
        yl < enemy4.pos_y + 60 < yl + 800 or enemy4.pos_y < yl < enemy4.pos_y + 50 or
        enemy4.pos_y < yl + 800 < enemy4.pos_y + 60) and enemy4.pos_y > -50:
        enemy4.gerar = True
        nave.pontos += 1

    if (xl < enemy5.pos_x < xl + 30 or xl < enemy5.pos_x + 80 < xl + 30 or enemy5.pos_x < xl < enemy5.pos_x + 85 or
        enemy5.pos_x < xl + 30 < enemy5.pos_x + 100) and (yl < enemy5.pos_y < yl + 800 or
        yl < enemy5.pos_y + 60 < yl + 800 or enemy5.pos_y < yl < enemy5.pos_y + 50 or
        enemy5.pos_y < yl + 800 < enemy5.pos_y + 60) and enemy5.pos_y > -50:
        enemy5.gerar = True
        nave.pontos += 1

# Ship 2 laser collision
def colisao3():

    if (xl2 < enemy.pos_x < xl2 + 30 or xl2 < enemy.pos_x + 80 < xl2 + 30 or enemy.pos_x < xl2 < enemy.pos_x + 85 or
        enemy.pos_x < xl2 + 30 < enemy.pos_x + 100) and (yl2 < enemy.pos_y < yl2 + 800 or
        yl2 < enemy.pos_y + 60 < yl2 + 800 or enemy.pos_y < yl2 < enemy.pos_y + 50 or
        enemy.pos_y < yl2 + 800 < enemy.pos_y + 60) and enemy.pos_y > -50:
        enemy.gerar = True
        nave2.pontos += 1

    if (xl2 < enemy2.pos_x < xl2 + 30 or xl2 < enemy2.pos_x + 80 < xl2 + 30 or enemy2.pos_x < xl2 < enemy2.pos_x + 85 or
        enemy2.pos_x < xl2 + 30 < enemy2.pos_x + 100) and (yl2 < enemy2.pos_y < yl2 + 800 or
        yl2 < enemy2.pos_y + 60 < yl2 + 800 or enemy2.pos_y < yl2 < enemy2.pos_y + 50 or
        enemy2.pos_y < yl2 + 800 < enemy2.pos_y + 60) and enemy2.pos_y > -50:
        enemy2.gerar = True
        nave2.pontos += 1

    if (xl2 < enemy3.pos_x < xl2 + 30 or xl2 < enemy3.pos_x + 80 < xl2 + 30 or enemy3.pos_x < xl2 < enemy3.pos_x + 85 or
        enemy3.pos_x < xl2 + 30 < enemy3.pos_x + 100) and (yl2 < enemy3.pos_y < yl2 + 800 or
        yl2 < enemy3.pos_y + 60 < yl2 + 800 or enemy3.pos_y < yl2 < enemy3.pos_y + 50 or
        enemy3.pos_y < yl2 + 800 < enemy3.pos_y + 60) and enemy3.pos_y > -50:
        enemy3.gerar = True
        nave2.pontos += 1

    if (xl2 < enemy4.pos_x < xl2 + 30 or xl2 < enemy4.pos_x + 80 < xl2 + 30 or enemy4.pos_x < xl2 < enemy4.pos_x + 85 or
        enemy4.pos_x < xl2 + 30 < enemy4.pos_x + 100) and (yl2 < enemy4.pos_y < yl2 + 800 or
        yl2 < enemy4.pos_y + 60 < yl2 + 800 or enemy4.pos_y < yl2 < enemy4.pos_y + 50 or
        enemy4.pos_y < yl2 + 800 < enemy4.pos_y + 60) and enemy4.pos_y > -50:
        enemy4.gerar = True
        nave2.pontos += 1

    if (xl2 < enemy5.pos_x < xl2 + 30 or xl2 < enemy5.pos_x + 80 < xl2 + 30 or enemy5.pos_x < xl2 < enemy5.pos_x + 85 or
        enemy5.pos_x < xl2 + 30 < enemy5.pos_x + 100) and (yl2 < enemy5.pos_y < yl2 + 800 or
        yl2 < enemy5.pos_y + 60 < yl2 + 800 or enemy5.pos_y < yl2 < enemy5.pos_y + 50 or
        enemy5.pos_y < yl2 + 800 < enemy5.pos_y + 60) and enemy5.pos_y > -50:
        enemy5.gerar = True
        nave2.pontos += 1

# Background animation
def anim_stars():
    tela.blit(fundo1, (0, display.fundo_y))
    tela.blit(fundo2, (0, display.fundo_y2))
    tela.blit(fundo3, (0, display.fundo_y3))
    display.fundo_y += 1 + display.vel
    display.fundo_y2 += 0.1 + display.vel
    display.fundo_y3 += 0.5 + display.vel

    if display.fundo_y >= 810:
        display.fundo_y = -6010
    if display.fundo_y2 >= 810:
        display.fundo_y2 = -6010
    if display.fundo_y3 >= 810:
        display.fundo_y3 = -6010

# Increase game and enemies speed by score
def dificuldade():
    if nave.pontos + nave2.pontos > display.verificador + 20:
        display.verificador = (nave.pontos + nave2.pontos)
        enemy.vel += 0.2
        enemy2.vel += 0.2
        enemy3.vel += 0.2
        enemy4.vel += 0.2
        enemy5.vel += 0.2
        display.vel += 0.6

# Menu animation
def anim_display():
    if int(display.atualizar) % 10 == 1 or int(display.atualizar) % 10 == 0:
        tela.blit(menu100, (0, 0))
    if int(display.atualizar) % 10 == 2 or int(display.atualizar) % 10 == 9:
        tela.blit(menu80, (0, 0))
    if int(display.atualizar) % 10 == 3 or int(display.atualizar) % 10 == 8:
        tela.blit(menu60, (0, 0))
    if int(display.atualizar) % 10 == 4 or int(display.atualizar) % 10 == 7:
        tela.blit(menu40, (0, 0))
    if int(display.atualizar) % 10 == 5 or int(display.atualizar) % 10 == 6:
        tela.blit(menu20, (0, 0))

# Increase enemies by score
def inimigos_control():
    temp = (nave.pontos + nave2.pontos)
    if temp < 30:
        enemy.mov()
    elif 30 <= temp < 70:
        enemy.mov()
        enemy2.mov()
    elif 70 <= temp < 140:
        enemy.mov()
        enemy2.mov()
        enemy3.mov()
    elif 140 <= temp <= 210:
        enemy.mov()
        enemy2.mov()
        enemy3.mov()
        enemy4.mov()
    elif temp > 210:
        enemy.mov()
        enemy2.mov()
        enemy3.mov()
        enemy4.mov()
        enemy5.mov()

# Laser control functions
def coolDownLaser():
    global contCD1, Laser, startCDL
    contCD1 += 1
    if contCD1 >= 10:
        Laser = False
        startCDL = False
        contCD1 = 0

def duracaoLaser():
    global contD1, startCDL
    contD1 += 1
    if contD1 > 10:
        startCDL = True
        contD1 = 0

def duracaoLaser2():
    global contD12, startCDL2
    contD12 += 1
    if contD12 > 10:
        startCDL2 = True
        contD12 = 0

def coolDownLaser2():
    global contCD12, Laser2, startCDL2
    contCD12 += 1
    if contCD12 >= 10:
        Laser2 = False
        startCDL2 = False
        contCD12 = 0

# Recharge ship lifes every 100 points
def vE():
    global verificador1, verificador2
    if nave.pontos % 100 == 0 and (nave.life != 3 or nave2.state == False) and nave.pontos != verificador1:
        verificador1 = nave.pontos
        if display.sound_effects == True:
            life_charge.sound.play()
        nave.life = 3
        if nave2.state == False:
            nave2.life = 3
            nave2.state = True

    if multiplayer.state:
        if nave2.pontos % 100 == 0 and (nave2.life != 3 or nave.state == False) and nave2.pontos != verificador2:
            verificador2 = nave2.pontos
            if display.sound_effects == True:
                life_charge.sound.play()
            nave2.life = 3
            if nave.state == False:
                nave.life = 3
                nave.state = True

# Speed functions
def duracaoSpeed():
    global contD2, startCDS
    nave.vel = 10
    contD2 += 1
    tela.blit(puVel.image_100, (nave.pu_pos_x, nave.pu_pos_y))

    if contD2 >= 500:
        startCDS = True
        contD2 = 0
        nave.vel = 5

def duracaoSpeed2():
    global contD22, startCDS2
    nave2.vel = 10
    contD22 += 1
    tela.blit(puVel.image_100, (nave2.pu_pos_x, nave2.pu_pos_y))

    if contD22 >= 500:
        startCDS2 = True
        contD22 = 0
        nave2.vel = 5

def coolDownSpeed2():
    global contCD22, speed2, startCDS2
    contCD22 += 1
    tela.blit(puVel.image_30, (nave2.pu_pos_x, nave2.pu_pos_y))
    if contCD22 >= 500:
        startCDS2 = False
        speed2 = False
        contCD22 = 0

def coolDownSpeed():
    global contCD2, speed, startCDS
    contCD2 += 1
    tela.blit(puVel.image_30, (nave.pu_pos_x, nave.pu_pos_y))
    if contCD2 >= 500:
        startCDS = False
        speed = False
        contCD2 = 0

# Reset variables
def reset_geral():
    global startCDS, startCDS2, speed, speed2
    display.reset()
    nave.reset()
    nave2.reset()
    enemy.reset()
    enemy2.reset()
    enemy3.reset()
    enemy4.reset()
    enemy5.reset()
    startCDS2 = False
    speed2 = False
    startCDS = False
    speed = False
    verificador1 = 0
    verificador2 = 0

# Game over
def game_over_pontos():
        display_pontos = display.font_type2.render(str("Total Score: " + str(nave.pontos + nave2.pontos)), True, (255, 255, 255))
        tela.blit(display_pontos, (250, 250))

# Main loop
while display.loop:
    clock.tick(60)

    # ------------------------------------------------------MENU-----------------------------------------------------------
    while menu.state:
        clock.tick(8)

        if display.som == False and display.music == True:
            menu.sound.play(loops=-1)
            display.som = True

        tela.fill((0, 0, 0))
        anim_display()
        tela.blit(menu.image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.loop = False
                menu.state = False

        if display.contador_baixo < 4:
            display.contador_baixo += 1
        if display.contador_cima < 4:
            display.contador_cima += 1

        tecla = pygame.key.get_pressed()
        if (tecla[pygame.K_s] or tecla[pygame.K_DOWN]) and display.contador_cima >= 3:
            display.contador_cima = 0
            if display.sound_effects == True:
                sistema.sound.play()
            display.seletor += 1
        if tecla[pygame.K_w] or tecla[pygame.K_UP] and display.contador_baixo >= 3:
            display.contador_baixo = 0
            if display.sound_effects == True:
                sistema.sound.play()
            display.seletor -= 1

        display.atualizar += 1
        menu_function(display.seletor, display.atualizar)

        if tecla[pygame.K_SPACE] or tecla[pygame.K_KP_ENTER] or tecla[pygame.K_RETURN]:
            if display.sound_effects == True:
                sistema.sound.play()
            selecao_estado(display.seletor, display.seletor_options)
        pygame.display.update()

    # ----------------------------------------------------OPTIONS------------------------------------------------------

    while options.state:
        clock.tick(8)

        tela.fill((0, 0, 0))
        anim_display()
        options_fundo(display.music, display.sound_effects)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.loop = False
                options.state = False

        if display.contador_baixo < 4:
            display.contador_baixo += 1
        if display.contador_cima < 4:
            display.contador_cima += 1

        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_s] or tecla[pygame.K_DOWN] and display.contador_baixo > 3:
            display.contador_baixo = 0
            if display.sound_effects == True:
                sistema.sound.play()
            display.seletor += 1
        if tecla[pygame.K_w] or tecla[pygame.K_UP] and display.contador_cima > 3:
            display.contador_cima = 0
            if display.sound_effects == True:
                sistema.sound.play()
            display.seletor -= 1

        display.atualizar += 1
        menu_function(display.seletor, display.atualizar)

        if tecla[pygame.K_BACKSPACE]:
            if display.sound_effects == True:
                sistema.sound.play()
            if display.instructions == True:
                display.instructions = False


        if display.instructions == True:
            tela.blit(game_instructions, (0, 0))

        if tecla[pygame.K_SPACE] or tecla[pygame.K_KP_ENTER] or tecla[pygame.K_RETURN]:
            if display.sound_effects == True:
                sistema.sound.play()
            selecao_estado(display.seletor, display.seletor_options)

        pygame.display.update()

    # --------------------------------------------------CREDITS----------------------------------------------------

    while creditos.state:
        clock.tick(60)

        if display.som == False and display.music == True:
            creditos.sound.play(loops=-1)
            display.som = True

        tela.fill((0, 0, 0))
        tela.blit(creditos.image, (creditos.pos_x, creditos.pos_y))

        creditos.mov()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.loop = False
                creditos.state = False

        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_BACKSPACE]:
            creditos.sound.fadeout(300)
            reset_geral()
            menu.state = True
            creditos.state = False

        pygame.display.update()

    # ---------------------------------------------MULTIPLAYER----------------------------------------------------

    while multiplayer.state:
        clock.tick(60)

        if display.som == False and display.music == True:
            multiplayer.sound.play(loops=-1)
            display.som = True

        tela.fill((0, 0, 0))
        anim_stars()
        nave.update()
        nave2.update()
        dificuldade()
        colisao()
        vE()
        inimigos_control()

        if startCDS2 == False and speed2 == False:
            tela.blit(puVel.image_70, (nave2.pu_pos_x, nave2.pu_pos_y))

        if startCDS == False and speed == False:
            tela.blit(puVel.image_70, (nave.pu_pos_x, nave.pu_pos_y))

        if Laser2 == True and startCDL2 == False:
            duracaoLaser2()
        if Laser2 == True and startCDL2 == True:
            coolDownLaser2()
        if Laser == True and startCDL == False:
            duracaoLaser()
        if Laser == True and startCDL == True:
            coolDownLaser()
        if speed2 == True and startCDS2 == False:
            duracaoSpeed2()
        if speed2 == True and startCDS2 == True:
            coolDownSpeed2()
        if speed == True and startCDS == False:
            duracaoSpeed()
        if speed == True and startCDS == True:
            coolDownSpeed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.loop = False
                multiplayer.state = False

        tecla = pygame.key.get_pressed()
        if nave.state:
            if tecla[pygame.K_d] and nave.pos_x < 715:
                nave.pos_x += nave.vel
            if tecla[pygame.K_a] and nave.pos_x > 0:
                nave.pos_x -= nave.vel
            if tecla[pygame.K_s] and nave.pos_y < 515:
                nave.pos_y += nave.vel
            if tecla[pygame.K_w] and nave.pos_y > 0:
                nave.pos_y -= nave.vel
            if tecla[pygame.K_z] and speed == False:
                if display.sound_effects == True:
                    powerup.sound.play()
                speed = True
            if tecla[pygame.K_SPACE] and startCDL == False:
                if display.sound_effects == True:
                    tiro.sound.play()
                xl = (nave.pos_x + nave.pos_x + 70) // 2
                yl = nave.pos_y - 550
                tela.blit(laser, (xl, yl))
                Laser = True
                colisao2()

        if nave2.state:
            if tecla[pygame.K_RIGHT] and nave2.pos_x < 715:
                nave2.pos_x += nave2.vel
            if tecla[pygame.K_LEFT] and nave2.pos_x > 0:
                nave2.pos_x -= nave2.vel
            if tecla[pygame.K_DOWN] and nave2.pos_y < 515:
                nave2.pos_y += nave2.vel
            if tecla[pygame.K_UP] and nave2.pos_y > 0:
                nave2.pos_y -= nave2.vel
            if tecla[pygame.K_RCTRL] or tecla[pygame.K_RSHIFT] and speed2 == False:
                if display.sound_effects == True:
                    powerup.sound.play()
                speed2 = True
            if tecla[pygame.K_l] and startCDL2 == False:
                if display.sound_effects == True:
                    tiro.sound.play()
                xl2 = (nave2.pos_x + nave2.pos_x + 70) // 2
                yl2 = nave2.pos_y - 550
                tela.blit(laser2, (xl2, yl2))
                Laser2 = True
                colisao3()

        if display.contador_pause < 11:
            display.contador_pause += 1

        if (tecla[pygame.K_ESCAPE] or tecla[pygame.K_p]) and display.contador_pause >= 10:
            display.contador_pause = 0
            tela.blit(pause.image, (0, 0))
            pause.state = True

        while pause.state:
            clock.tick(60)
            pygame.mixer.pause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.loop = False
                    arcade.state = False
                    pause.state = False

            if display.contador_pause < 11:
                display.contador_pause += 1

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_BACKSPACE]:
                menu.state = True
                multiplayer.state = False
                pause.state = False
                reset_geral()

            if (tecla[pygame.K_ESCAPE] or tecla[pygame.K_p]) and display.contador_pause >= 10:
                pygame.mixer.unpause()
                display.contador_pause = 0
                pause.state = False

            pygame.display.update()

        if (nave.life + nave2.life) == 0:
            multiplayer.sound.fadeout(300)
            if display.sound_effects == True:
                game_over.sound.play()
            game_over.state = True
            tela.blit(game_over.image, (0, 0))
            display.som = False

        while game_over.state:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.loop = False
                    multiplayer.state = False
                    game_over.state = False

            game_over_pontos()

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_BACKSPACE]:
                creditos.sound.fadeout(300)
                menu.state = True
                multiplayer.state = False
                game_over.state = False
                reset_geral()

            pygame.display.update()

        pygame.display.update()

    # ------------------------------------------------------ARCADE-----------------------------------------------------------------
    while arcade.state:
        clock.tick(60)
        if display.som == False and display.music == True:
            arcade.sound.play(loops=-1)
            display.som = True

        tela.fill((0, 0, 0))
        anim_stars()
        nave.update()
        inimigos_control()
        dificuldade()
        colisao()
        vE()

        if startCDS == False and speed == False:
            tela.blit(puVel.image_70, (nave.pu_pos_x, nave.pu_pos_y))

        if speed == True and startCDS == False:
            duracaoSpeed()
        if speed == True and startCDS == True:
            coolDownSpeed()
        if Laser == True and startCDL == False:
            duracaoLaser()
        if Laser == True and startCDL == True:
            coolDownLaser()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display.loop = False
                arcade.state = False

        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_d] and nave.pos_x < 715:
            nave.pos_x += nave.vel
        if tecla[pygame.K_a] and nave.pos_x > 0:
            nave.pos_x -= nave.vel
        if tecla[pygame.K_s] and nave.pos_y < 515:
            nave.pos_y += nave.vel
        if tecla[pygame.K_w] and nave.pos_y > 0:
            nave.pos_y -= nave.vel
        if tecla[pygame.K_z] and speed == False:
            if display.sound_effects == True:
                powerup.sound.play()
            speed = True

        if display.contador_tiro < 6:
            display.contador_tiro += 1

        if tecla[pygame.K_SPACE] and startCDL == False:
            xl = (nave.pos_x + nave.pos_x + 70) // 2
            yl = nave.pos_y - 550
            tela.blit(laser, (xl, yl))
            Laser = True
            colisao2()

            if (display.sound_effects == True) and (display.contador_tiro >= 5):
                display.contador_tiro = 0
                tiro.sound.play()

        if display.contador_pause < 11:
            display.contador_pause += 1

        if (tecla[pygame.K_ESCAPE] or tecla[pygame.K_p]) and display.contador_pause >= 10:
            display.contador_pause = 0
            tela.blit(pause.image, (0, 0))
            pause.state = True

        while pause.state:
            clock.tick(60)
            pygame.mixer.pause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.loop = False
                    arcade.state = False
                    pause.state = False

            if display.contador_pause < 11:
                display.contador_pause += 1

            tecla = pygame.key.get_pressed()

            if tecla[pygame.K_BACKSPACE]:
                menu.state = True
                arcade.state = False
                pause.state = False
                reset_geral()

            if (tecla[pygame.K_ESCAPE] or tecla[pygame.K_p]) and display.contador_pause >= 10:
                pygame.mixer.unpause()
                display.contador_pause = 0
                pause.state = False

            pygame.display.update()

        if nave.life <= 0:
            arcade.sound.fadeout(300)
            if display.sound_effects == True:
                game_over.sound.play()
            game_over.state = True
            tela.blit(game_over.image, (0, 0))
            display.som = False

        while game_over.state:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display.loop = False
                    arcade.state = False
                    game_over.state = False

            game_over_pontos()

            tecla = pygame.key.get_pressed()
            if tecla[pygame.K_BACKSPACE]:
                creditos.sound.fadeout(300)
                menu.state = True
                arcade.state = False
                game_over.state = False
                reset_geral()

            pygame.display.update()

        pygame.display.update()

pygame.quit()