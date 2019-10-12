import random

#Creates a word grid using a random list from the words_list. The rest of the characters in the grid are filled as '.'
class WordGrid():


    def __init__(self, rows, columns, size):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.grid = self.createGrid(rows, columns)
        self.allwords = {}
        words_list = [["sofa", "chair", "bookshelf", "television", "drapes", "books", "curtain", "desk"],
                 ["salad", "sandwich", "break", "steak", "tuna", "fish", "rice", "spaghetti"],
                 ["kyoto", "florence", "barcelona", "sanfrancisco", "boston", "mumbai", "santiago", "rome"],
                 ["pandabear", "fish", "snake", "porcupine", "dog", "tiger", "cat", "leopard", "horse", "alligator"],
                 ["baidu", "reddit", "instagram", "facebook", "google", "gmail", "whatsapp", "amazon", "youtube"],
                 ["apple", "samsung", "nokia", "blackberry", "huawei", "lenovo", "motorola", "sony", "oneplus"],
                 ["inception", "titanic", "avatar", "godfather", "dunkirk", "rocky", "chuck", "gravity", "interstellar"],
                 ["supernatural", "office", "westworld", "sopranos", "chuck", "daredevil", "dexter", "seinfield"]]
        #words_list = [['battlestarships']]
        words = words_list[random.randint(0, len(words_list) - 1)]
        for word in words:
            self.placeWord(self.grid, word)

    '''Returns the grid of characters and their co-ordinates on the screen.'''
    def getGrid(self):
        return self.grid, self.allwords

    '''Creates a skeleton grid with "." character'''
    def createGrid(self, rows, columns):
        grid = []
        for row in range(rows):
            grid.append([])
            for column in range(columns):
                x = (row * (self.size[0] / self.columns))
                y = (column * ((self.size[1] - 100) / self.rows)) + 100
                grid[row].append((".", x, y))
        return grid




    '''Tries to place the word in the grid. Returns true if successful'''
    def tryToPlaceWord(self, grid, word):
        # Find the direction of the word.
        direction = random.randrange(0, 8)
        if (direction == 0):
            x_change = -1
            y_change = -1
        if (direction == 1):
            x_change = 0
            y_change = 1
        if (direction == 2):
            x_change = 1
            y_change = -1
        if (direction == 3):
            x_change = 1
            y_change = 0
        if (direction == 4):
            x_change = 1
            y_change = 1
        if (direction == 5):
            x_change = 0
            y_change = 1
        if (direction == 6):
            x_change = -1
            y_change = 1
        if (direction == 7):
            x_change = -1
            y_change = 0

        # Find the length and height of the grid
        height = len(grid)
        width = len(grid[0])

        # Create a random start point
        column = random.randrange(width)
        row = random.randrange(height)

        # Check if the word doesn't extend beyond the edge of the grid.
        # If yes, return False
        if (x_change < 0 and column < len(word)):
            return False
        if (x_change > 0 and column > width - len(word)):
            return False
        if (y_change < 0 and row < len(word)):
            return False
        if (y_change > 0 and row > height - len(word)):
            return False

        # Check if there isn't another letter on the way
        current_column = column
        current_row = row
        for letter in word:
            # Make sure it is blank, or already the correct letter.
            if grid[current_row][current_column][0] == letter or grid[current_row][current_column][0] == '.':
                current_row += y_change
                current_column += x_change
            else:
                # Oh! A different letter is already here. Fail.
                return False

        #Place the letters in the location
        current_column = column
        current_row = row
        word_locations = []
        for letter in word:
            x = (current_row * (self.size[0] / self.columns))
            y = (current_column * ((self.size[1] - 100) / self.rows)) + 100
            grid[current_row][current_column] = (letter, x, y)
            word_locations.append((x,y))
            current_row += y_change
            current_column += x_change
        self.allwords[word] = word_locations
        return True

    '''Calls the method to place the word on the grid'''
    def placeWord(self, grid, word):
        counter = 0
        success = False

        while not (success):
            counter += 1
            if counter > 10000:
                return
            success = self.tryToPlaceWord(grid, word)
