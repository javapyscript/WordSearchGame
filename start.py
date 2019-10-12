import pygame
from createwordgrid import WordGrid
import copy
import string
import random

pygame.init()

string.letters = 'abcdefghijklmnopqrstuvwxyz'
RED = (255,0,0)
ORANGE = (255,127,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
GREY = (96, 95, 93)
BLACK = (0,0,0)
DARKGREEN = (75, 175, 179)
LIGHTGREEN = (93, 223, 227)

fullsize = (600, 700)
size = (600,600)

screen = pygame.display.set_mode(fullsize)
pygame.display.set_caption('Word Search')
font = pygame.font.Font("RobotoCondensed-Regular.ttf", 20)
wordsfont = pygame.font.Font("RobotoCondensed-Regular.ttf", 15)
lettersfont = pygame.font.Font("RobotoCondensed-Light.ttf", 20)

done = False
#clock = pygame.time.Clock()

mouse_state = 0
mouse_x = 0
mouse_y = 0

cColumns = 15
cRows = 15
cWords = 0

all_words = {}
all_words_list = []
found_words = {}
board = []

'''Helper class to create a button. Provides functions to check mouse states and act accordingly'''
class Button():
    def __init__(self):
        pass

    '''Define what constitutes a click'''
    def clicked(self, x, y, width, height):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 1 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True


    '''Define what constitutes a hover'''
    def hover(self, x, y, width, height):
        global mouse_state, mouse_x, mouse_y
        if mouse_state == 0 and mouse_x >= x and mouse_x <= (x + width) and mouse_y >= y and mouse_y <= (y + height):
            return True

    '''Define behaviour when a button is clicked'''
    def clickButton(self, x, y, width, height, normalColor, hoverColor, textFont, text, textColor, stateHolding=False,
                    stateVariable=0, state=1):
        if not self.clicked(x, y, width, height) and not self.hover(x, y, width, height):
            pygame.draw.rect(screen, normalColor, (x, y, width, height))
        elif self.hover(x, y, width, height):
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        if stateHolding == True and stateVariable == state:
            pygame.draw.rect(screen, hoverColor, (x, y, width, height))
        buttonText = textFont.render(text, True, textColor)
        buttonText_x = buttonText.get_rect().width
        buttonText_y = buttonText.get_rect().height
        screen.blit(buttonText, (((x + (width / 2)) - (buttonText_x / 2)), ((y + (height / 2)) - (buttonText_y / 2))))
        if self.clicked(x, y, width, height):
            return True

button = Button()

'''Define what happens when all the words are found. Shows the win message'''
def success():
    global found_words, all_words, all_words_list
    if len(found_words) == len(all_words_list) and len(all_words) == 0:
        pygame.draw.rect(screen, BLACK, (0, size[0]/2, 600, 100))
        text = font.render("You win!!", True, LIGHTGREEN)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        #pygame.draw.rect(screen, GREY, (0, 600, 600, 700))
        screen.blit(text, ((size[0]/2 - (text_x / 2)), (size[1]/2 - (text_y / 2) + 50)))

'''Defines and displays the top bar that has the three buttons for show/hide solution and check word'''
def topBar():
    global found_words, done
    pygame.draw.rect(screen, GREY, (0, 0, 600, 100))
    pygame.draw.line(screen, BLACK, (0, 100), (600, 100), 4)
    pygame.draw.rect(screen, GREY, (0, 600, 600, 700))

    if button.clickButton(360, 620, 160, 50, DARKGREEN, LIGHTGREEN, font, "Reset", WHITE):
        game.reset(cColumns, cRows)

    if button.clickButton(20, 25, 160, 50, DARKGREEN, LIGHTGREEN, font, "Show solution", WHITE):
        for row in board:
            for tile in row:
                if not tile.isaletter:
                    tile.letter = '.'

    if button.clickButton(190, 25, 160, 50, DARKGREEN, LIGHTGREEN, font, "Hide solution", WHITE):
        for row in board:
            for tile in row:
                if not tile.isaletter:
                    tile.letter = tile.actual_letter


    if button.clickButton(360, 25, 160, 50, DARKGREEN, LIGHTGREEN, font, "Check word", WHITE):
        new_possible_words = {}
        possible_words = {}
        tiles_found = 0
        for row in board:
            for tile in row:
                if tile.selected:
                    x = tile.x
                    y = tile.y
                    found = False
                    if not possible_words:
                        for key, value in all_words.items():
                            if (x,y) in value:
                                found = True
                                tiles_found += 1
                                possible_words[key] = value

                    else:
                        for key, value in possible_words.items():
                            if (x,y) in value:
                                found = True
                                tiles_found += 1
                                new_possible_words[key] = value


                        if found:
                            possible_words = copy.deepcopy(new_possible_words)
                    if not found:
                        for row in board:
                            for tile in row:
                                if tile.selected:
                                    tile.selected = False
                        return False
        if len(possible_words) == 1 and tiles_found == len(list(possible_words.values())[0]):
            for row in board:
                for tile in row:
                    if tile.selected:
                        tile.selected = False
            for pos in list(possible_words.values())[0]:
                pos_x = pos[0]
                pos_y = pos[1]
                for row in board:
                    for tile in row:
                        if tile.x == pos_x and tile.y == pos_y:
                            tile.found = True
            found_words[list(possible_words.keys())[0]] = all_words.pop(list(possible_words.keys())[0])

        for row in board:
            for tile in row:
                if tile.selected:
                    tile.selected = False
            #return True


    start_x = 50
    start_y = 620
    for word in all_words_list:
        if word in found_words:
            text = wordsfont.render(word , True, LIGHTGREEN)
        else:
            text = wordsfont.render(word, True, WHITE)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((start_x - (text_x / 2)), (start_y - (text_y / 2))))
        start_y = start_y + text_y + 2
        if start_y > 700:
            start_y = 620
            start_x = start_x + 100



class Tile():
    def __init__(self, y, x, columns, rows):
        self.columns = columns
        self.rows = rows
        self.x = (x * (size[0] / self.columns))
        self.y = (y * ((size[1] - 100) / self.rows)) + 100
        self.visible = True
        self.letter = ''
        self.selected = False
        self.found = False
        self.isaletter = False
        self.actual_letter = ''

    def update(self):
        if mouse_state == 1 and mouse_x >= self.x and mouse_x <= (self.x + (size[0] / self.columns)) and mouse_y >= self.y and mouse_y <= (
            self.y + ((size[1] - 100) / self.rows)):

            self.selected = not self.selected

    def show(self):

        text = lettersfont.render(self.letter, True, BLACK)
        text_x = text.get_rect().width
        text_y = text.get_rect().height
        screen.blit(text, ((self.x + ((size[0] / self.columns) / 2) - (text_x / 2)),
                           (self.y + (((size[1] - 100) / self.rows) / 2) - (text_y / 2))))

        if self.found:
            pygame.draw.rect(screen, LIGHTGREEN, (self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)))
            text = lettersfont.render(self.letter, True, BLACK)
            text_x = text.get_rect().width
            text_y = text.get_rect().height
            screen.blit(text, ((self.x + ((size[0] / self.columns) / 2) - (text_x / 2)),
                               (self.y + (((size[1] - 100) / self.rows) / 2) - (text_y / 2))))
            pygame.draw.rect(screen, BLACK, (self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)),
                             2)
        if self.selected:
            pygame.draw.rect(screen, RED, (self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)),
                             2)
        else:
            pygame.draw.rect(screen, BLACK, (self.x, self.y, (size[0] / self.columns), ((size[1] - 100) / self.rows)), 2)


class Game():
    def __init__(self, columns, rows):
        global all_words
        global board
        global all_words_list
        self.columns = columns
        self.rows = rows
        self.board = []

        # creating board
        for y in range(self.rows):
            self.board.append([])
            for x in range(self.columns):
                self.board[y].append(Tile(x, y, self.columns, self.rows))

        wordgridobj = WordGrid(rows, columns, size)
        wordgrid, all_words = wordgridobj.getGrid()
        all_words_list = list(all_words.keys())

        for x_index, row in enumerate(wordgrid):
            for y_index, value in enumerate(row):
                if wordgrid[x_index][y_index][0] != '.':
                    self.board[x_index][y_index].isaletter = True
                    self.board[x_index][y_index].letter = wordgrid[x_index][y_index][0]
                    self.board[x_index][y_index].actual_letter = wordgrid[x_index][y_index][0]
                else:
                    temp_letter = random.choice(string.letters)
                    self.board[x_index][y_index].letter = temp_letter
                    self.board[x_index][y_index].actual_letter = temp_letter

        board = self.board


    def render(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.board[y][x].update()
                self.board[y][x].show()

    '''Resets the game'''
    def reset(self, columns, rows):
        global game, all_words, all_words_list, found_words, board
        all_words = {}
        all_words_list = []
        found_words = {}
        board = []
        if columns != 0 and rows != 0:
            self.columns = columns
            self.rows = rows
        self.board = []

        # creating board
        for y in range(self.rows):
            self.board.append([])
            for x in range(self.columns):
                self.board[y].append(Tile(x, y, self.columns, self.rows))

        game = Game(cRows, cColumns)

game = Game(cRows, cColumns)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_state = event.button
            pygame.mouse.set_pos(mouse_x, mouse_y + 1)
        else:
            mouse_state = 0

    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    if not done:
        screen.fill(WHITE)
        game.render()
        topBar()
        success()

        pygame.display.flip()

        #clock.tick(60)

pygame.display.quit()
pygame.quit()
