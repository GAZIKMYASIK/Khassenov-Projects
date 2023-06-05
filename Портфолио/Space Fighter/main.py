import pygame
from pygame import *
from fighter import Fighter
from button import Button
mixer.init()
pygame.init()


#создание окна
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Fighter")

#задать кадры в секунду

clock = pygame.time.Clock()
FPS = 60

#цвета


RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


#Игровые переменные
intro_count = 3
controls = "P1: WASD R,T  P2: ARROWS , 1,2 "
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
game_paused = False
#Переменные бойцов
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Загрузка музыки
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)



#Загрузка фото кнопок
resume_img = pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha()
quit_img = pygame.image.load("assets/images/buttons/button_quit.png").convert_alpha()
#Создание кнопок
resume_button = Button(304,125,resume_img,1)
quit_button = Button(297,250,quit_img,1)

#Загрузка заднего фона
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#Загрузка спрайтов
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#Загрузка экрана победы
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#Число шагов в каждой анимации
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Шрифты
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
control_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
#Функция для рисования текста
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


def pause(game_paused):
  paused = True
  while paused:
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      
    key = pygame.key.get_pressed()
    if key[pygame.K_p]:
      paused = False

    pygame.display.update()
    clock.tick(15)



#Функция для рисования заднего фона
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#Функция,рисующая полоски жизней
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#Создать образы бойцов
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#Игровой цикл
run = True
while run:
  clock.tick(FPS)

  #Рисование заднего фона
  draw_bg()

  #Показ статистику игроков
  draw_health_bar(fighter_1.health, 20, 20)
  draw_health_bar(fighter_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
  #Обновление обратного отсчета
  if intro_count <= 0:
    #Движение бойцов
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

  else:
    #Показать таймер со временем
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    draw_text("P1: WASD+R,T P2: ARROWS + 1,2",control_font, RED, 20,60)
    #Обновление таймера
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()
 
  
  #Обновление бойцов
  fighter_1.update()
  fighter_2.update()

  #Рисовать бойцов
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  #Проверка на поражение
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #Показать победный экран
    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
  if game_paused == True:
    if resume_button.draw(screen):
      game_paused = False
      paused = False
    if quit_button.draw(screen):
      run = False
    paused = True
    while paused:
    
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        if resume_button.draw(screen):
          game_paused = False
          paused = False
        if quit_button.draw(screen):
          paused = False
          run = False
      pygame.display.update()
      clock.tick(15)
  #Обработка событий
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        game_paused = True
    if event.type == pygame.QUIT:
      run = False
   



  #Обновление экрана
  pygame.display.update()

#Выход Пайгейм
pygame.quit()