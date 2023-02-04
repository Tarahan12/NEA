import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton
from pygame.locals import *
import sys
import os
import random
from random import choice, randrange
import math
from fractions import Fraction


pygame.init()
pygame.mixer.init()

RES = WIDTH, HEIGHT = 800, 600
TILE = 50
cols = math.ceil(WIDTH / TILE)
rows = math.ceil(HEIGHT / TILE)

black = (0,0, 0)
purple = (100, 29, 176)

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Maths Revsion Game")
icon = pygame.image.load("maze (1).png")
pygame.display.set_icon(icon)
CLOCK = pygame.time.Clock()
FPS = 60



mathmaze_img = pygame.image.load('Math.png').convert_alpha()
name_img = pygame.image.load('math.png').convert_alpha()


correct_sound = pygame.mixer.music.load("Correct.mp3")
incorrect_sound = pygame.mixer.music.load("Incorrect.mp3")
class Button():
    def __init__(self, x ,y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
       
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
           
        window.blit(self.image, (self.rect.x, self.rect.y))
        return action

math_button = Button(90, 50, mathmaze_img, 1)

manager = pygame_gui.UIManager((800, 600))

play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (300, 70)),
                                            text='Play',
                                            manager=manager,
                                            object_id=pygame_gui.core.ObjectID(class_id="selected_bg"))
options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 300), (300, 70)),
                                         text='Options',
                                         manager=manager)
exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 400), (300, 70)),
                                         text='Exit',
                                         manager=manager)






backgroundA = pygame.image.load("background.png").convert()

x = 0
run = True

def play():
    
    
    FPS = 60
    game_surface = pygame.Surface(RES)
    surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
    clock = pygame.time.Clock()

    # images
    bg_game = pygame.image.load('background2.jpg').convert()

    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False
            self.thickness = 4

        def draw(self, sc):
            x, y = self.x * TILE, self.y * TILE

            if self.walls['top']:
                pygame.draw.line(sc, pygame.Color('black'), (x, y), (x + TILE, y), self.thickness)
            if self.walls['right']:
                pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
            if self.walls['bottom']:
                pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
            if self.walls['left']:
                pygame.draw.line(sc, pygame.Color('black'), (x, y + TILE), (x, y), self.thickness)

        def get_rects(self):
            rects = []
            x, y = self.x * TILE, self.y * TILE
            if self.walls['top']:
                rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
            if self.walls['right']:
                rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
            if self.walls['bottom']:
                rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
            if self.walls['left']:
                rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
            return rects

        def check_cell(self, x, y):
            find_index = lambda x, y: x + y * cols
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return self.grid_cells[find_index(x, y)]

        def check_neighbors(self, grid_cells):
            self.grid_cells = grid_cells
            neighbors = []
            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            if top and not top.visited:
                neighbors.append(top)
            if right and not right.visited:
                neighbors.append(right)
            if bottom and not bottom.visited:
                neighbors.append(bottom)
            if left and not left.visited:
                neighbors.append(left)
            return choice(neighbors) if neighbors else False

    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def generate_maze():
        grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        current_cell = grid_cells[0]
        array = []
        break_count = 1

        while break_count != len(grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(grid_cells)
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        return grid_cells

    
    maze = generate_maze()
    player_speed = 5
    player_img = pygame.image.load('rocket.png').convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
    player_rect = player_img.get_rect()
    player_rect.center = TILE // 2, TILE // 2
    directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)}
    keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
    direction = (0, 0)

    decimals = [0.32, 0.4, 0.35, 0.309]
    modified_decimals = [round(random.uniform(0, 1), 3) for decimal in decimals]

    target = random.randint(2,9)
    a = random.randint(1,30)
    b = random.randint(1,30)
    c = random.randint(1,30)
    d = random.randint(1,30)

    min_num = 1
    max_num = 30
    random_num = random.randint(min_num, max_num)
    random_multiple = math.floor(random_num / target) * target

    while (a % target == 0) or (b % target == 0) or (c % target == 0) or (d % target == 0) :
        a = random.randint(1,30)
        b = random.randint(1,30)
        c = random.randint(1,30)
        d = random.randint(1,30)

    while random_multiple == target:
        random_multiple = math.floor(random_num / target) * target
        
    number = round(random.uniform(0, 10), 3)


    denominators = [2,4,5,10,20,50,100]
    denominator = random.choice(denominators)
    numerator = random.randint(1, denominator)
    fraction = str(Fraction(numerator, denominator))

    four_digit_number = [random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
    while four_digit_number[0] == four_digit_number[1] or four_digit_number[0] == four_digit_number[2] or four_digit_number[0] == four_digit_number[3] or four_digit_number[1] == four_digit_number[2] or four_digit_number[1] == four_digit_number[3] or four_digit_number[2] == four_digit_number[3]:
        four_digit_number = [random.randint(1,9),random.randint(1,9),random.randint(1,9),random.randint(1,9)]

    value = random.choice(four_digit_number)

    num = round(random.uniform(0,1),2)
    num2 = random.randint(1,1000000)
    num3 = random.randint(-10,10)
    num4 = random.randint(1,10)
    num5 = random.randint(1,10)
    num6 = random.randint(1,10)
    num7 = random.randint(1,10)
                      
    superscript_2 = chr(0x00B2)
    superscript_3 = chr(0x00B3)
    questions = ["Write the following numbers in order of size. \n Start with the smallest number. \n" + str(modified_decimals)
             ,"Here is a list of numbers. \n{}, {}, {}, {}, {} \nFrom the list, write down a multiple of {}".format(a, b, c, random_multiple, d, target)
              ,"Write {:.3f} correct to the nearest whole number.".format(number),
              ("What is the value of %d in the number %d%d%d%d?" % (value, four_digit_number[0], four_digit_number[1], four_digit_number[2], four_digit_number[3])),
              "Write {} as a decimal.".format(fraction),
               "Write {} as a fraction.".format(num),
              "What is {} rounded to the nearest 10,000?".format(num2),
              ("What is %dx + %dx - %dx?" % (num3, num4, num5)),
              "Write {} as a percentage.".format(fraction), 
              ("What is %d.5{}?".format(superscript_2) % (num6)),
              ("What is %d.5{}?".format(superscript_3) % (num7))]


    modified_decimals.sort()
    coefficient = num3 + num4 - num5
    black = (200, 200, 200)
    answers = []
    answers.append(modified_decimals)
    answers.append(random_multiple)
    answers.append(round(number))
    if value == four_digit_number[3]:
        answers.append(value)
    elif value == four_digit_number[2]:
        answers.append(value * 10)
    elif value == four_digit_number[1]:
        answers.append(value * 100)
    elif value == four_digit_number[0]:
        answers.append(value * 1000)
    answers.append(float(Fraction(numerator, denominator)))
    answers.append( Fraction.from_float(num).limit_denominator(100))
    answers.append(round(num2, -4))
    answers.append("%dx" % (coefficient))
    answers.append("%d" % (float(Fraction(numerator, denominator)) * 100) + "%")
    answers.append((num6 + 0.5) ** 2)
    answers.append((num7 + 0.5) ** 3)
        
    question = random.choice(questions)
    correct_answer = answers[questions.index(question)]
    font = pygame.font.Font(None, 32)
    text = font.render(str(question), True, black)

    manager = pygame_gui.UIManager((1100, 600))
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 500), (300, 50)), manager=manager,
                                                   object_id='#main_text_entry')

    # define the font size and spacing
    fontsize = 50
    margin_x = 25  # pixels from the left
    margin_y = 25  # pixels from the top
    spacing_y = 4  # pixels between lines
    # initialize a font (Arial)
    font = pygame.freetype.SysFont('Arial', fontsize)

    # create a list from the string and render it to surfaces
    rendered_fonts =[]
    for i, line in enumerate(question.split('\n')):
        txt_surf, txt_rect = font.render(line, pygame.Color('black'))
        # set the text rect to a position based on the line number and 
        # spacing parameters
        txt_rect.topleft = (margin_x, margin_y + i * (fontsize + spacing_y))
        rendered_fonts.append((txt_surf, txt_rect))

    def check_answer(user_answer, score):
        tries = 3
        correct = False
        while tries > 0 and not correct:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if str(user_answer) == str(correct_answer):
                new_text = pygame.font.SysFont("bahnschrift", 50).render("Correct Answer!", True, "green")
                new_text_rect = new_text.get_rect(center=(WIDTH/2, HEIGHT/2))
                window.blit(new_text, new_text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                score += 1
                correct = True
            else:
                new_text = pygame.font.SysFont("bahnschrift", 50).render("Oops! Try again...", True, "red")
                new_text_rect = new_text.get_rect(center=(WIDTH/2, HEIGHT/2))
                window.blit(new_text, new_text_rect)
                pygame.display.flip()
                pygame.time.wait(1000)
                score -= 1
            tries -= 1

        return score






    def get_answer(score):
        done_question = False
        while not done_question:
            UI_REFRESH_RATE = clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                    score = check_answer(event.text, score)
                    done_question = True
                manager.process_events(event)
            manager.update(UI_REFRESH_RATE)
            window.fill("white")
            for txt_surf, txt_rect in rendered_fonts:
                window.blit(txt_surf, txt_rect)
            manager.draw_ui(window)
            
            pygame.display.flip()

        return score






    
    class Food:
        def __init__(self):
            self.img = pygame.image.load('food.png').convert_alpha()
            self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))
            self.rect = self.img.get_rect()
            self.set_pos()

        def set_pos(self):
            self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5

        def draw(self):
            game_surface.blit(self.img, self.rect)


    def is_collide(x, y):
        tmp_rect = player_rect.move(x, y)
        if tmp_rect.collidelist(walls_collide_list) == -1:
            return False
        return True


    def eat_food():
        for food in food_list:
            if player_rect.collidepoint(food.rect.center):
                food.set_pos()
                return True
        return False

    def game_over(time, score):
        if time < 0:
            # Display the game over screen
            game_over_image = pygame.image.load("game_over.jpg").convert()

            # Resize the image to fit the screen
            game_over_image = pygame.transform.scale(game_over_image, (WIDTH + 300, HEIGHT))

            # Display the image
            window.blit(game_over_image, (0, 0))
           
            
            # Display the score
            score_font = pygame.font.SysFont('verdanaprocondsemibold', 100)
            score_text = score_font.render("Score: " + str(score), True, black)
            window.blit(score_text, (350, 400))
            
   # food settings
    food_list = [Food() for i in range(3)]

    # collision list
    walls_collide_list = sum([cell.get_rects() for cell in maze], [])

    # timer, score, record
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    time = 60
    score = 0

    # fonts
    font = pygame.font.SysFont('Impact', 50)
    text_font = pygame.font.SysFont('Impact', 50)
    while True:
        surface.blit(bg_game, (WIDTH, 0))
        surface.blit(game_surface, (0, 0))
        game_surface.blit(bg_game, (0, 0))
        surface.blit(text_font.render('Time:', True, pygame.Color('white'), True), (WIDTH + 20, 5))
        surface.blit(font.render(f'{time}', True, pygame.Color('black')), (WIDTH + 20, 70))
        surface.blit(text_font.render('Score:', True, pygame.Color('white'), True), (WIDTH + 20, 205))
        surface.blit(font.render(f'{score}', True, pygame.Color('black')), (WIDTH + 20, 270))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                time -= 1
        game_over(time, score)

        # controls and movement
        pressed_key = pygame.key.get_pressed()
        for key, key_value in keys.items():
            if pressed_key[key_value] and not is_collide(*directions[key]):
                direction = directions[key]
                break
        if not is_collide(*direction):
            player_rect.move_ip(direction)

        # draw maze
        [cell.draw(game_surface) for cell in maze]
        
        # gameplay
        if eat_food():
            get_answer(score)


        # draw player
        game_surface.blit(player_img, player_rect)

        # draw food
        [food.draw() for food in food_list]

        
        # print(clock.get_fps())
        pygame.display.flip()
        clock.tick(FPS)
        
        

def options():
    options_screen = pygame.display.set_mode(RES)
    pygame.display.set_caption("Options")
    manager = pygame_gui.UIManager((800, 600))
    avatar_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 200), (200, 50)),
                                             text='Select Avatar',
                                             manager=manager,
                                             button_bg_color=(128, 0, 128))
    background_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 300), (200, 50)),
                                             text='Select Background',
                                             manager=manager)
    music_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 400), (200, 50)),
                                             text='Select Music',
                                             manager=manager)
    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (50, 50)),
                                             text='Back',
                                             manager=manager)

    clock = pygame.time.Clock()
    is_running = True
    x = 0
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        background_x = x % backgroundA.get_rect().width
        window.blit(backgroundA, (background_x - backgroundA.get_rect().width, 0))
        if background_x < WIDTH:
            window.blit(backgroundA, (background_x, 0))
        x -= 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == avatar_button:
                    # Add code to select avatar here
                    pass
                if event.ui_element == background_button:
                    # Add code to select background here
                    pass
                if event.ui_element == music_button:
                    # Add code to select music here
                    pass
                if event.ui_element == back_button:
                    # Add code to return to previous screen here
                    pass

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(window)

        pygame.display.update()





    
    
        
    
run = True   
while run:
    time_delta = CLOCK.tick(60)/1000.0
    background_x = x % backgroundA.get_rect().width
    window.blit(backgroundA, (background_x - backgroundA.get_rect().width, 0))
    if background_x < WIDTH:
        window.blit(backgroundA, (background_x, 0))
    x -= 1
    # Load the music file
    pygame.mixer.music.load("Music.mp3")
    pygame.mixer.music.play()
    if math_button.draw():
        run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == play_button:
                  play()
              if event.ui_element == options_button:
                  options()
              if event.ui_element == exit_button:
                  pygame.quit()
                  sys.exit()

        manager.process_events(event)

    manager.draw_ui(window)
    manager.update(time_delta)
    
   
    pygame.display.update()


    
    


    
    
    

    

