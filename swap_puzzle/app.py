import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
path = os.getcwd()

import pygame
from grid import Grid
from solver import Solver
import button
from buttons import Button
import time
from math import sqrt
from random import randint

pygame.init()
solver = Solver()

#create game window
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
coeff_font = SCREEN_WIDTH/1200
mid = SCREEN_WIDTH/2

rectangle_columns = pygame.Rect(mid/2-50, 9*SCREEN_HEIGHT/20-50,100*coeff_font,100*coeff_font)
rectangle_lines = pygame.Rect(3*mid/2-50, 9*SCREEN_HEIGHT/20-50,100*coeff_font,100*coeff_font)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SWAP PUZZLE")

#define colours
grey = "#101820"
yellow = "#FEE715"
yellow_passive = "#7a7a0d"
dark_blue = "#00246B"
light_blue = "#CADCFC"
blue_passive = "#325fb8"

yellow_continue = "#ffff14"
dark_hover = "#3f5061"
light_hover = "#b9d2ff"

#game variables
game_paused = False
program_state = "launch"  #launch screen, menu, in_game, optimal_solution, select, pause
theme = "dark"
columns = ""
col_active = False
col_col = yellow_passive
lines = ""
lin_active = False
col_lin = yellow_passive

#define fonts
coeff_font = SCREEN_WIDTH/1200
font = pygame.font.SysFont("arialblack", int(40*coeff_font))
font_small = pygame.font.SysFont("verdana", int(15*coeff_font))

font_end = pygame.font.SysFont("verdana italic", int(50*coeff_font))

font_big = pygame.font.SysFont("arialblack", int(65*coeff_font))
font_title_1 = pygame.font.SysFont("arialblack", int(150*coeff_font))
font_title_2 = pygame.font.SysFont("arialblack", int(120*coeff_font))
font_title_end = pygame.font.SysFont("verdana bold", int(130*coeff_font))
font_menu_1 = pygame.font.SysFont("arialblack", int(120*coeff_font))
font_menu_2 = pygame.font.SysFont("arialblack", int(96*coeff_font))
font_select = pygame.font.SysFont("arialblack", int(90*coeff_font))


#load image
if path[-4:] == "main":
    swap_puzzle_img = pygame.image.load('swap_puzzle/swap_puzzle.png').convert_alpha()
    swap_puzzle_scaled = pygame.transform.scale(swap_puzzle_img, (coeff_font*180, coeff_font*180))
else:
    swap_puzzle_img = pygame.image.load('swap_puzzle.png').convert_alpha()
    swap_puzzle_scaled = pygame.transform.scale(swap_puzzle_img, (coeff_font*180, coeff_font*180))


#create button instances - dark theme
solve_button_d = Button(mid, 15*SCREEN_HEIGHT/32, "SOLVE THE GRID", yellow, dark_hover, int(coeff_font*44), 4, radius = 8)
best_button_d = Button(mid, 19*SCREEN_HEIGHT/32, "BEST SOLUTION", yellow, dark_hover, int(coeff_font*44), 4, radius = 8, padding_x = 25)
theme_button_d = Button(mid, 23*SCREEN_HEIGHT/32, "CHANGE THEME", yellow, dark_hover, int(coeff_font*44), 4, radius = 8, padding_x = 28)
leave_button_d = Button(mid, 27*SCREEN_HEIGHT/32, "LEAVE THE GAME", yellow, dark_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
home_button_d = Button(mid/8, SCREEN_HEIGHT/16, "HOME", yellow, dark_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
pause_button_d = Button(15*mid/8, SCREEN_HEIGHT/16, "PAUSE", yellow, dark_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
#pause buttons
resume_button_d = Button(mid, 10*SCREEN_HEIGHT/32, "RESUME GAME", yellow, dark_hover, int(coeff_font*55), 5, radius = 8)
change_size_button_d = Button(mid, 16*SCREEN_HEIGHT/32, "CHANGE SIZE", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 45)
menu_button_d = Button(mid, 22*SCREEN_HEIGHT/32, "MAIN MENU", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 88)
#level buttons
easy_d = Button(mid, 13*SCREEN_HEIGHT/32, "BEGINNER", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 105)
medium_d = Button(mid, 19*SCREEN_HEIGHT/32, "INTERMEDIATE", yellow, dark_hover, int(coeff_font*55), 5, radius = 8)
hard_d = Button(mid, 25*SCREEN_HEIGHT/32, "ADVANCED", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 100)
#end game
replay_button_d = Button(mid, 13*SCREEN_HEIGHT/32, "REPLAY GAME", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 25)
return_menu_button_d = Button(mid, 19*SCREEN_HEIGHT/32, "MAIN MENU", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 65)
quit_button_d = Button(mid, 25*SCREEN_HEIGHT/32, "LEAVE GAME", yellow, dark_hover, int(coeff_font*55), 5, radius = 8, padding_x = 65)

continue_button_d = Button(mid, 27*SCREEN_HEIGHT/32, "CONTINUE", yellow, dark_hover, int(coeff_font*70), 8, radius = 8, padding_x = 40, padding_y = 40)
next_button_d = Button(mid, 27*SCREEN_HEIGHT/32, "NEXT SWAP", yellow, dark_hover, int(coeff_font*70), 8, radius = 8, padding_x = 40, padding_y = 40)

#create button instances - light theme
solve_button_l = Button(mid, 15*SCREEN_HEIGHT/32, "SOLVE THE GRID", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8)
best_button_l = Button(mid, 19*SCREEN_HEIGHT/32, "BEST SOLUTION", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8, padding_x = 25)
theme_button_l = Button(mid, 23*SCREEN_HEIGHT/32, "CHANGE THEME", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8, padding_x = 28)
leave_button_l = Button(mid, 27*SCREEN_HEIGHT/32, "LEAVE THE GAME", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
home_button_l = Button(mid/8, SCREEN_HEIGHT/16, "HOME", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
pause_button_l = Button(15*mid/8, SCREEN_HEIGHT/16, "PAUSE", dark_blue, light_hover, int(coeff_font*44), 4, radius = 8, padding_x = 18)
#pause buttons
resume_button_l = Button(mid, 10*SCREEN_HEIGHT/32, "RESUME GAME", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8)
change_size_button_l = Button(mid, 16*SCREEN_HEIGHT/32, "CHANGE SIZE", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 45)
menu_button_l = Button(mid, 22*SCREEN_HEIGHT/32, "MAIN MENU", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 88)
#level buttons
easy_l = Button(mid, 13*SCREEN_HEIGHT/32, "BEGINNER", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 100)
medium_l = Button(mid, 19*SCREEN_HEIGHT/32, "INTERMEDIATE", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8)
hard_l = Button(mid, 25*SCREEN_HEIGHT/32, "ADVANCED", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 100)
#end game
replay_button_l = Button(mid, 13*SCREEN_HEIGHT/32, "REPLAY GAME", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 25)
return_menu_button_l = Button(mid, 19*SCREEN_HEIGHT/32, "MAIN MENU", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 65)
quit_button_l = Button(mid, 25*SCREEN_HEIGHT/32, "LEAVE GAME", dark_blue, light_hover, int(coeff_font*55), 5, radius = 8, padding_x = 65)

continue_button_l = Button(mid, 27*SCREEN_HEIGHT/32, "CONTINUE", dark_blue, light_hover, int(coeff_font*70), 8, radius = 8, padding_x = 40, padding_y = 40)
next_button_l = Button(mid, 27*SCREEN_HEIGHT/32, "NEXT SWAP", dark_blue, light_hover, int(coeff_font*70), 8, radius = 8, padding_x = 40, padding_y = 40)


def draw_text(text, font, text_col, x, y):
  """
  This function draws a text on the screen, but the coordinates are the center of the text (not top left as usual in pygame)
  """
  img = font.render(text, True, text_col)
  xx = img.get_rect().width
  yy = img.get_rect().height
  screen.blit(img, (x - xx/2, y - yy/2))

def generate_grid(lin, col, level):
    """
    generates a random grid, based on the level : if easy, each coefficient will be in a range on 50% of the grid size, if medium 75% and 100% for hard
    """
    area = (50 + level*25)/100  #range where the coefficient will be generated around his solved position
    d_max = sqrt((lin-1)**2 + (col-1)**2)
    placed_coeff = []
    actual_coeff = 0
    grid = [[None for _ in range(col)] for _ in range(lin)]

    #place the coefficients one by one
    for i in range(lin):
        for j in range(col):
            actual_coeff += 1
            in_range = []

            #generate coordinates where the actual coefficient can go, based on the level
            for k in range(lin):
                for l in range(col):
                    if sqrt((i-k)**2 + (j-l)**2) < area * d_max and grid[k][l] is None:
                        in_range.append((k,l))
            
            #generate random coefficient in the previous list
            #case where there are available cells in the range
            if len(in_range) > 0:
                coeff = in_range[randint(0, len(in_range)-1)]
                placed_coeff.append(coeff)
                grid[coeff[0]][coeff[1]] = actual_coeff
            #case where no cell is available
            else:
                k, l = 0, 0
                while True:
                    if None in grid[k]:
                        if grid[k][l] is None:
                            grid[k][l] = actual_coeff
                            break
                        else:
                            l += 1

                    else:
                        k += 1

    return Grid(lin, col, grid)


#game loop
run = True
index = 0
time.sleep(0.2)
while run:
    index += 1
    print(0, screen.get_rect().width)
    #change variables depending on the theme
    if theme == "dark" :
        solve_button = solve_button_d
        best_button = best_button_d
        theme_button = theme_button_d
        leave_button = leave_button_d
        continue_button = continue_button_d
        bg = grey
        txt = yellow
        txt_passive = yellow_passive
        home_button = home_button_d
        pause_button = pause_button_d
        resume_button = resume_button_d 
        change_size_button = change_size_button_d 
        menu_button = menu_button_d 
        replay_button = replay_button_d
        return_menu_button = return_menu_button_d
        quit_button = quit_button_d 
        next_button = next_button_d
        easy = easy_d
        medium = medium_d
        hard = hard_d
        hover = dark_hover
        end = "light green"

    elif theme == "light" :
        solve_button = solve_button_l
        best_button = best_button_l
        theme_button = theme_button_l
        leave_button = leave_button_l
        continue_button = continue_button_l
        bg = light_blue
        txt = dark_blue
        txt_passive = blue_passive
        home_button = home_button_l
        pause_button = pause_button_l
        resume_button = resume_button_l
        change_size_button = change_size_button_l
        menu_button = menu_button_l
        replay_button = replay_button_l
        return_menu_button = return_menu_button_l
        quit_button = quit_button_l
        next_button = next_button_l
        easy = easy_l
        medium = medium_l
        hard = hard_l
        hover = light_hover
        end = "dark green"

    screen.fill(bg)

    #launch screen
    if program_state == "launch":
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        program_state = "menu"
        except:
            pass

        draw_text("Press SPACE to enter.", font, txt, SCREEN_WIDTH/2, 9*SCREEN_HEIGHT/10)
        draw_text("SWAP", font_title_1, txt, 5.9*SCREEN_WIDTH/10, 8*SCREEN_HEIGHT/20)
        draw_text("PUZZLE", font_title_2, txt, 5.9*SCREEN_WIDTH/10, 11*SCREEN_HEIGHT/20)
        screen.blit(swap_puzzle_scaled, (3*SCREEN_WIDTH/10-110, 37*SCREEN_HEIGHT/80-90))

    #menu screen
    elif program_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_text("SWAP", font_menu_1, txt, SCREEN_WIDTH/2, 3.1*SCREEN_HEIGHT/20)
        draw_text("PUZZLE", font_menu_2, txt, SCREEN_WIDTH/2, 5.9*SCREEN_HEIGHT/20)
        # click on "solve the grid"
        if solve_button.draw(screen):
            program_state = "select size"
            game = "level"
        # click on "best solution"
        elif best_button.draw(screen):
            program_state = "select size"
            game = "enter coeff"
        # click on "change theme"
        elif theme_button.draw(screen):
            time.sleep(0.2)
            if theme == "light":
                theme = "dark"
                col_col = yellow_passive
                col_lin = yellow_passive
            elif theme == "dark":
                theme = "light"
                col_col = blue_passive
                col_lin = blue_passive
        # click on "leave the game"
        elif leave_button.draw(screen):
            run = False

    # select size screen
    elif program_state == "select size":
        draw_text("COLNS", font_big, col_col, mid/2, 6*SCREEN_HEIGHT/20)
        draw_text("LINES", font_big, col_lin, 3*mid/2, 6*SCREEN_HEIGHT/20)
        if game == "enter coeff":
            draw_text("Enter small size (cols*lines < 12) to continue", font_small, "grey", SCREEN_WIDTH/2, 9.5*SCREEN_HEIGHT/10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if col_active:
                        columns = str(columns)[:-1]
                    if lin_active:
                        lines = str(lines)[:-1]
                else:
                    if col_active and len(str(columns))<1:
                        columns += event.unicode
                    if lin_active and len(str(lines))<1:
                        lines += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rectangle_columns.collidepoint(event.pos):
                    col_active, col_col = True, txt
                    lin_active, col_lin = False, txt_passive
                elif rectangle_lines.collidepoint(event.pos):
                    col_active, col_col = False, txt_passive
                    lin_active, col_lin = True, txt
                else :
                    col_active, col_col = False, txt_passive
                    lin_active, col_lin = False, txt_passive

        pygame.draw.rect(screen,col_col,rectangle_columns,10)
        pygame.draw.rect(screen,col_lin,rectangle_lines,10)

        col_surface = font_select.render(str(columns),True,col_col)
        screen.blit(col_surface, (rectangle_columns.topleft[0]+18*coeff_font, rectangle_columns.topleft[1]-18*coeff_font))
        lin_surface = font_select.render(str(lines),True,col_lin)
        screen.blit(lin_surface, (rectangle_lines.topleft[0]+18*coeff_font, rectangle_lines.topleft[1]-18*coeff_font))

        if continue_button.draw(screen) and str(columns).isdigit() and str(lines).isdigit():
            if (game == "level" or int(columns)*int(lines) <= 10) and (int(columns) > 0 and int(lines) > 0):  #if the grid is too big and we are in "best solve", A* star won't work
                program_state = game
                #select cases to swap them in the solve
                time.sleep(0.2)
                active = []
                coeff = [["" for _ in range(int(columns))] for __ in range(int(lines))]

    #screen to enter the coefficients of our grid
    elif program_state == "enter coeff":
        
        draw_text("Enter your numbers :", font_big, txt, mid, SCREEN_HEIGHT/8)

        lines, columns = int(lines), int(columns)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                time.sleep(0.2)
                x, y = event.pos
                j, i = int((x/SCREEN_WIDTH*(columns+4))//1 - 2), int((y/SCREEN_HEIGHT*(lines+4))//1 - 2) 
                if 0 <=  i <= lines-1 and 0 <= j <= columns-1:
                    active = (i,j)
                else:
                    active = None
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active:
                        coeff[active[0]][active[1]] = coeff[active[0]][active[1]][:-1]
                
                else:
                    if active and len(coeff[active[0]][active[1]]) <1:
                        coeff[active[0]][active[1]] += event.unicode

        lines, columns = int(lines), int(columns)

        for i in range(lines):
            for j in range(columns):

                #if case is selected we change its color
                if (i,j) == active:
                    pygame.draw.rect(surface=screen, color=hover,
                                rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (columns + 4),
                                                SCREEN_HEIGHT * (i + 2) / (lines + 4),
                                                SCREEN_WIDTH / (columns + 4) + 7 - columns*lines/45,
                                                SCREEN_HEIGHT / (lines + 4) + 7 - columns*lines/45),
                                width=0)
                
                #then, we draw the cells
                pygame.draw.rect(surface=screen, color=txt,
                                rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (columns + 4),
                                                SCREEN_HEIGHT * (i + 2) / (lines + 4),
                                                SCREEN_WIDTH / (columns + 4) + 7 - columns*lines/45,
                                                SCREEN_HEIGHT / (lines + 4) + 7 - columns*lines/45),
                                width=int(7 - columns*lines/45))
                font = pygame.font.SysFont('verdana bold', int(400 / max(columns, lines)))
                text = font.render(str(coeff[i][j]), True, txt)
                screen.blit(text, 
                            (SCREEN_WIDTH*(j + 5 / 2) / (columns + 4) - text.get_rect().width / 2 + (7 - columns*lines/45) / 2, 
                             SCREEN_HEIGHT * (i + 5 / 2) / (lines + 4) - text.get_rect().height / 2 + (7 - columns*lines/45) / 2))
        
        if set([str(i) for i in list(range(1,columns*lines+1))]) == set([c for line in coeff for c in line]):
            if continue_button.draw(screen):
                time.sleep(0.2)
                coeff = [[int(c) for c in line] for line in coeff]
                G = Grid(lines, columns, coeff)   
                program_state = "best"
                score = 0


    #screen to chose level of difficulty
    elif program_state == "level":
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        except:
            pass

        level = -1
        text = font_big.render("SELECT LEVEL", True, txt)
        screen.blit(text, (mid - text.get_rect().width/2, 4*SCREEN_HEIGHT/32))
        if easy.draw(screen):
            level = 0
        if medium.draw(screen):
            level = 1
        if hard.draw(screen):
            level = 2

        if level >= 0:
            time.sleep(0.2)
            G = generate_grid(int(lines), int(columns), level)
            program_state = "solve"
            score = 0

    #screen of the game
    elif program_state == "solve":

        if home_button.draw(screen):
            program_state = "menu"  
        if pause_button.draw(screen):
            program_state = "paused"       
        
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    time.sleep(0.2)
                    x, y = event.pos
                    j, i = int((x/SCREEN_WIDTH*(G.n+4))//1 - 2), int((y/SCREEN_HEIGHT*(G.m+4))//1 - 2) 
                    if 0 <= i <= G.m-1 and 0 <= j <= G.n-1:
                        if len(active) == 0 or (len(active) == 1 and ((abs(i-active[0][0]) == 1 and abs(j-active[0][1]) == 0) or (abs(i-active[0][0]) == 0 and abs(j-active[0][1]) == 1))):
                            active.append((i,j))
                        else:
                            active = [(i,j)]
        except:
            pass
        
        for i in range(G.m):
            for j in range(G.n):
                #if case is selected we change its color
                if (i,j) in active:
                    pygame.draw.rect(surface=screen, color=hover,
                                rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (G.n + 4),
                                                SCREEN_HEIGHT * (i + 2) / (G.m + 4),
                                                SCREEN_WIDTH / (G.n + 4) + G.coeff,
                                                SCREEN_HEIGHT / (G.m + 4) + G.coeff),
                                width=0)
                
                #then, we draw the cells
                pygame.draw.rect(surface=screen, color=txt,
                                rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (G.n + 4),
                                                SCREEN_HEIGHT * (i + 2) / (G.m + 4),
                                                SCREEN_WIDTH / (G.n + 4) + G.coeff,
                                                SCREEN_HEIGHT / (G.m + 4) + G.coeff),
                                width=int(G.coeff))
                font = pygame.font.SysFont('verdana bold', int(400 / max(G.m, G.n)))
                text = font.render(str(G.state[i][j]), True, txt)
                screen.blit(text, (SCREEN_WIDTH * (j + 5 / 2) / (G.n + 4) - text.get_rect().width / 2 +
                                    G.coeff / 2,
                                    SCREEN_HEIGHT * (i + 5 / 2) / (G.m + 4) - text.get_rect().height / 2 +
                                    G.coeff / 2))

        #swap if 2 cells selected
        if len(active) == 2:
            pygame.display.update()
            time.sleep(0.2)
            G.swap(active[0], active[1])
            score += 1
            active = []
        
        if G.state == [list(range(i * int(columns) + 1, (i + 1) * int(columns) + 1)) for i in range(int(lines))]:
            program_state = "end game"

    elif program_state == "paused":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if resume_button.draw(screen):
            program_state = game
        if change_size_button.draw(screen):
            program_state = "select size"
        if menu_button.draw(screen):
            program_state = "menu"
            time.sleep(0.2)
    
    #screen displayed at the end of the game
    elif program_state == "end game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if game == "level":
            draw_text("CONGRATULATIONS", font_title_end, txt, mid, 4*SCREEN_HEIGHT/32)
            draw_text(("You solved the grid in "+str(score)+" move(s)!"), font_end, end, mid, 7*SCREEN_HEIGHT/32)
        
        else:
            draw_text("GRID SOLVED", font_title_end, txt, mid, 4*SCREEN_HEIGHT/32)
            draw_text(("The grid was solved in "+str(score)+" move(s)!"), font_end, end, mid, 7*SCREEN_HEIGHT/32)

        if replay_button.draw(screen):
            program_state = "select size"
            time.sleep(0.2)
        if return_menu_button.draw(screen):
            program_state = "menu"
            time.sleep(0.2)
        if quit_button.draw(screen):
            run = False
            time.sleep(0.2)

    elif program_state == "best":
        
        path = solver.a_star(G)

        while path:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            screen.fill(bg)
            draw_text("The next swap is :", font_big, txt, mid, SCREEN_HEIGHT/8)

            for i in range(G.m):
                for j in range(G.n):
                    #if case is selected we change its color
                    if (i,j) in path[0]:
                        pygame.draw.rect(surface=screen, color=hover,
                                    rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (G.n + 4),
                                                    SCREEN_HEIGHT * (i + 2) / (G.m + 4),
                                                    SCREEN_WIDTH / (G.n + 4) + G.coeff,
                                                    SCREEN_HEIGHT / (G.m + 4) + G.coeff),
                                    width=0)
                    
                    #then, we draw the cells
                    pygame.draw.rect(surface=screen, color=txt,
                                    rect=pygame.Rect(SCREEN_WIDTH * (j + 2) / (G.n + 4),
                                                    SCREEN_HEIGHT * (i + 2) / (G.m + 4),
                                                    SCREEN_WIDTH / (G.n + 4) + G.coeff,
                                                    SCREEN_HEIGHT / (G.m + 4) + G.coeff),
                                    width=int(G.coeff))
                    font = pygame.font.SysFont('verdana bold', int(400 / max(G.m, G.n)))
                    text = font.render(str(G.state[i][j]), True, txt)
                    screen.blit(text, (SCREEN_WIDTH * (j + 5 / 2) / (G.n + 4) - text.get_rect().width / 2 +
                                        G.coeff / 2,
                                        SCREEN_HEIGHT * (i + 5 / 2) / (G.m + 4) - text.get_rect().height / 2 +
                                        G.coeff / 2))
            
            if next_button.draw(screen):
                time.sleep(0.2)
                G.swap(path[0][0], path[0][1])
                path.pop(0)
                score += 1
            
            pygame.display.update()

        program_state = "end game"


    pygame.display.update()

pygame.quit()
