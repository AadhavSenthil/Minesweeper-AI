
import random
import re


class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #making the board
        self.board = self.make_new_board()
        self.assign_value_to_board()

        # initializing a set to keep track of locations uncovered
        # saving (row,col) tuples in the set
        self.dug = set()
        self.flagged = set()


    def get_dim_size(self):
        return self.dim_size
    def get_num_bombs(self):
        return self.num_bombs


    def make_new_board(self):
           # making a board that is based on the dim size and num bombs
           # I plan on using a list of lists
        board = [[None for _ in range(self.dim_size)]for _ in range(self.dim_size)]

        #plant bombs
        bombs_planted = 0
        while bombs_planted <self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1)
            # we want the number of times dim_size goes into loc to tell us what row to look at
            row = loc // self.dim_size
            # the remainder of loc % dim_size to give us the col
            col = loc % self.dim_size

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue
            board[row][col] = '*' #plant the bomb
            bombs_planted +=1
        return board
    
    
    def assign_value_to_board(self):
        # this function is going to assign the values of 0-8 to all 
        # spaces without bombs. this represents the number of neighboring
        #bombs there are
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if there is a bomb we don't wanna overwrite it
                    continue
                self.board[r][c]= self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self, row, col):
        # iterates through each position and sums up the neighboring bombs
        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    #our original location
                    continue
                if self.board[r][c]== '*':
                    num_neighboring_bombs +=1
        return num_neighboring_bombs

    def place_flag(self, row, col):
        # this function is going to place a flag where you think there is a bomb
        self.flagged.add((row, col))         

    def dig(self, row, col):
        # return True if good dig
        # return False if bomb is hit
        
        #scenarios:
        #hit a bomb --> game over
        #dig at a location with neighboring bombs --> finish dig
        # dig at location with no neighboring bombs --> recursively dig neighbors
        self.dug.add((row, col))  # keep track of where we dug

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col ] > 0:
            return True
        
        #self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # don't dig where you've already dug
                self.dig(r,c)
                self.dug.add((r,c))

        # if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        # it'll print out what this function returns
        # return a string that shows the board to the player
        
        #create a new array that represeents what the user sees
        visible_board = [[None for _ in range(self.dim_size)]for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                elif(row,col) in self.flagged:
                    visible_board[row][col] = 'F'
                else:
                    visible_board[row][col]= ' '

        #put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size=10, num_bombs = 10):
    board = Board(dim_size, num_bombs)

    safe = True
    while len(board.dug) < board.dim_size**2 -num_bombs:
        print(board)
        user_decision = input("Would you like to add a flag or dig?")
        if user_decision == "dig":
            user_input = re.split(',(\\s)*' , input("Where would you like to dig? Input as row,col: "))  #2,8
            row, col = int(user_input[0]), int(user_input[-1])
            if row <0 or row>= board.dim_size or col<0 or col>= dim_size:
                print("Invalid location. Tray again!")
                continue

            #if its valid
            safe = board.dig(row, col)
            if not safe:
                # dug a bomb
                break #(game over)
        elif user_decision == "flag":
            user_input = re.split(',(\\s)*' , input("Where would you like to dig? Input as row,col: "))  #2,8
            row, col = int(user_input[0]), int(user_input[-1])
            if row <0 or row>= board.dim_size or col<0 or col>= dim_size:
                print("Invalid location. Tray again!")
                continue
            #if its valid
            safe = board.place_flag(row, col)
        else:
            print("Invalid location. Tray again!")
            continue

    if safe:
        print("CONGRATULATIONS!!!!! YOU WON!")
    else:
        print("sorry game over :(")
        # let's reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


safe = True
def generate_loc(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)

    safe = True
    while len(board.dug) < board.dim_size**2 -num_bombs:
        print(board)
        loc = random.randint(0, dim_size**2 -1)
        # we want the number of times dim_size goes into loc to tell us what row to look at
        row = loc // board.dim_size
        # the remainder of loc % dim_size to give us the col
        col = loc % board.dim_size
        print(row,col)
        if (row, col) in board.dug:
            continue
        else:
            safe = board.dig(row, col)
        if row <0 or row>= board.dim_size or col<0 or col>= dim_size:
            print("Invalid location. Tray again!")
            continue        
        if not safe:
            # the random generator dug a bomb
            break
    if safe:
        print("CONGRATULATIONS!!!!! YOU WON!")
    else:
        print("sorry game over :(")
        # let's reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)


safe = True
def intelligent_solver(dim_size= 10, num_bombs=10):
 pass
# check the surroundings of a bomb to check for a 1. If the 1 has no mines around it
# the tile we are on is a mine. if we know a for sure mine is somewhere we can decrement the values around it
# if a 0 tile is touching an uncovered tile that means it doesn't have a bomb
#implements basically reasoning
#create a list of safe coordinates. if its empty then i need to randomly check
#create basically another board and hold boolean values like has it been dug, is it flagged, and is it safe
if __name__ == '__main__':
 generate_loc()