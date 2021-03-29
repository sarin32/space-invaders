import math
import random

import pygame
from pygame import mixer


class Game(object):
    def __init__(self):
        # Initialise the pygame
        pygame.init()

        self.score_value = 0
        self.num_of_enemies = 8
        self.running = True

        font = pygame.font.Font('freesansbold.ttf', 32)
        self.score = font.render("Score : " + str(self.score_value), True, (255, 255, 255))

        over_font = pygame.font.Font("freesansbold.ttf", 64)
        self.over_text = over_font.render("GAME OVER", True, (255, 255, 255))

        # background Sound
        mixer.music.load("background.wav")
        mixer.music.play(-1)
        # Background image
        self.background = pygame.image.load('sky.png')
        # Caption and Icon
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)

        self.game_over = mixer.Sound("Game Over.wav")

    # shows score in the library
    def show_score(self):
        screen.blit(self.score, (10, 10))

    # shows game over when game over
    def game_over_text(self):
        screen.blit(self.over_text, (200, 250))
        self.game_over.play()


class Player(object):
    def __init__(self):
        self.playerImg = pygame.image.load('player.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0
        # on starting of game the player should not move
        # the change will occur when event occurs. so playerX_change is 0

    # function to draw player image
    def draw_player(self):
        screen.blit(self.playerImg, (self.playerX, self.playerY))

    # function to update position of the player during game play
    def update_pos(self):
        self.playerX += self.playerX_change
        if self.playerX <= 0:
            self.playerX = 0

        elif self.playerX >= 736:
            self.playerX = 736


class Bullet(object):
    def __init__(self):
        self.bulletImg = pygame.image.load('bullet.png')
        self.explosionSound = mixer.Sound("explosion.wav")
        self.bulletX = 0
        self.bulletY = 480
        self.bulletY_change = 40
        self.bullet_state = "ready"
        # Ready:-You can't see the bullet on the screen
        # Fire:-The bullet is currently moving

    # function to draw bullet image
    def draw_bullet(self):
        if self.bullet_state == 'fire':
            screen.blit(self.bulletImg, (self.bulletX + 16, self.bulletY + 10))

    # function to check collision of bullet with the enemy
    def is_collision(self, enemyX, enemyY):
        # equation used here is the distance b/w two points
        # d = √((X1-x2)^2 + (Y2-Y1)^2)
        distance = math.sqrt(math.pow(enemyX - self.bulletX, 2) + (math.pow(enemyY - self.bulletY, 2)))
        if distance < 27:
            self.explosionSound.play()
            self.bulletY = 480
            self.bullet_state = "ready"
            return True
        else:
            return False

    # function to update position of the bullet during game play
    def update_pos(self):
        if self.bulletY <= 0:
            self.bulletY = 480
            self.bullet_state = "ready"

        if self.bullet_state == "fire":
            self.bulletY -= self.bulletY_change


class Enemy(object):
    def __init__(self):
        self.enemyImg = pygame.image.load('enemy.png')
        self.enemyX = random.randint(0, 736)
        self.enemyY = random.randint(50, 150)
        self.enemyX_change = 3
        self.enemyY_change = 40

    # function to draw enemy on the screen
    def draw_enemy(self):
        screen.blit(self.enemyImg, (self.enemyX, self.enemyY))

    # function to update position of the enemy during game play
    def update_pos(self):
        self.enemyX += self.enemyX_change
        if self.enemyX <= 0:
            self.enemyX_change = abs(self.enemyX_change)
            self.enemyY += self.enemyY_change
        elif self.enemyX >= 736:
            self.enemyX_change = - self.enemyX_change
            self.enemyY += self.enemyY_change


# class for missiles send by enemy
class EnemyMissile(object):
    def __init__(self):
        self.missileImg = pygame.image.load('missile.png')
        self.missileX = 0
        self.missileY = 480
        self.missileY_change = 5
        self.missile_state = "ready"
        self.missile_firing_pby = 1

    # function to draw enemy missile on the screen
    def draw_enemy_missile(self):
        if self.missile_state == 'fire':
            screen.blit(self.missileImg, (self.missileX + 16, self.missileY + 10))

    # function to check collision of missile with the player
    def is_collision(self, playerX, playerY):
        # equation used here is the distance b/w two points
        # d = √((X1-x2)^2 + (Y2-Y1)^2)
        distance = math.sqrt(math.pow(playerX - self.missileX, 2) + (math.pow(playerY - self.missileY, 2)))
        if distance < 27:
            return True
        else:
            return False

    #  function to update the position of the missile in the screen
    def update_pos(self):
        if self.missileY > 600:
            self.missileY = 0
            self.missile_state = "ready"

        if self.missile_state == "fire":
            self.missileY += self.missileY_change


# create the screen
screen = pygame.display.set_mode((800, 600))


gm = Game()
py = Player()
bt = Bullet()
emy = []
em = []
for i in range(gm.num_of_enemies):
    emy.append(Enemy())
    em.append(EnemyMissile())

# Game Loop
while gm.running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(gm.background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gm.running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                py.playerX_change = -5
            if event.key == pygame.K_RIGHT:
                py.playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bt.bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x coordinate of the spaceship
                    bt.bulletX = py.playerX
                    bt.bullet_state = 'fire'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                py.playerX_change = 0

    py.update_pos()
    bt.update_pos()

    for i in range(gm.num_of_enemies):
        em[i].missile_firing_pby = int(gm.score_value / 5)
        em[i].missileY_change = int(gm.score_value / 30 + 1)
        emy[i].update_pos()
        em[i].update_pos()

        # checks for game over
        if emy[i].enemyY > 440:
            for j in range(gm.num_of_enemies):
                emy[j].enemyY = 2000
            gm.game_over_text()
            break

        # checks for bullet Collision
        collision = bt.is_collision(emy[i].enemyX, emy[i].enemyY)
        if collision:
            gm.score_value += 1
            emy[i].enemyX = random.randint(0, 736)
            emy[i].enemyY = random.randint(50, 150)

        # generates random enemy fire
        pby = random.randint(0, 1001)
        if pby <= em[i].missile_firing_pby and em[i].missile_state == 'ready':
            em[i].missileX = emy[i].enemyX
            em[i].missileY = emy[i].enemyY
            em[i].missile_state = 'fire'
            missileSound = mixer.Sound("missile.wav")
            missileSound.play()

        # draws enemy and enemy fire
        emy[i].draw_enemy()
        em[i].draw_enemy_missile()

        # checks for enemy fire collision
        collision = em[i].is_collision(py.playerX, py.playerY)
        if collision:
            for j in range(gm.num_of_enemies):
                emy[j].enemyY = 2000
            gm.game_over_text()
            break

    bt.draw_bullet()
    py.draw_player()
    gm.show_score()
    pygame.display.update()
