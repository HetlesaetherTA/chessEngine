import copy 
import os 
import string
import time

def parseNotation(string):
    if len(string) != 2:
        return 0
    # checks if string is tuple, inwhich it is already parsed
    if isinstance(string, tuple):
        return string
    else:
        return 8-int(string[1]), ord(string[0].upper()) - ord('A')
def isWithinBounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8

class Game:
    def __init__(self):
        self.board = [[Empty() for _ in range(8)] for _ in range(8)]
    
    def printBoard(self):

        for i in range(10):
            if i < 8:
                print(8-i, end='>') # arrow right
            elif i == 8:
                print('', end='  ')
            else:
                print('  ', end='')
            for j in range(8):
                if i < 8:
                    if type(self.board[i][j]) is not str:
                        print(self.board[i][j].alias, end='') 
                    else:
                        print(self.board[i][j], end='')
                elif i == 8:
                    print('^', end='') # arrow up
                else:
                    print(string.ascii_uppercase[j], end='')
            print()

        print()
    def getPossition(self, piece):
        # returns the position of a piece when called though 'itself' 
        # ex: Game[x][y].getLegalMoves -> getLegalMoves(): pos = getPossition(self)
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == piece:
                    return row,col

    def initalize(self):
        self.board[0][0] = Rook(white=False, game=self)
        self.board[0][1] = Knight(white=False, game=self)
        self.board[0][2] = Bishop(white=False, game=self)
        self.board[0][3] = Queen(white=False, game=self)
        self.board[0][4] = King(white=False, game=self)
        self.board[0][5] = Bishop(white=False, game=self)
        self.board[0][6] = Knight(white=False, game=self)
        self.board[0][7] = Rook(white=False, game=self)

        self.board[7][0] = Rook(white=True, game=self)
        self.board[7][1] = Knight(white=True, game=self)
        self.board[7][2] = Bishop(white=True, game=self)
        self.board[7][3] = Queen(white=True, game=self)
        self.board[7][4] = King(white=True, game=self)
        self.board[7][5] = Bishop(white=True, game=self)
        self.board[7][6] = Knight(white=True, game=self)
        self.board[7][7] = Rook(white=True, game=self)
        for i in range(8):
            self.board[1][i] = Pawn(white=False, game=self)
            self.board[6][i] = Pawn(white=True, game=self)
    def getKingPos(self):
        returnVal = {}
        for row in range(8):
            for col in range(8):
                if isinstance(self.board[row][col], King):
                    returnVal[self.board[row][col].white] = (row, col)
                if len(returnVal.keys()) == 2:
                    break
        return returnVal

    def move(self, oldPos, newPos, turn):
        white = True if turn == 'white' else False
        p_newPos = parseNotation(newPos)# p = parsed
        p_oldPos = parseNotation(oldPos)# p = parsed
         
        if p_newPos in self.board[p_oldPos[0]][p_oldPos[1]].getLegalMoves() and self.board[p_oldPos[0]][p_oldPos[1]].white == white:
            if  isinstance(self.board[p_oldPos[0]][p_oldPos[1]], Pawn):
                if self.board[p_oldPos[0]][p_oldPos[1]].white and self.board[p_newPos[0]] == 0:
                    self.board[0][p_newPos[1]] = Queen(white=True, game=self)
                    self.board[p_oldPos[0]][p_oldPos[1]] = Empty()
                if not self.board[p_oldPos[0]][p_oldPos[1]].white and self.board[p_newPos[0]] == 7:
                    self.board[7][p_newPos[1]] = Queen(white=True, game=self)
                    self.board[p_oldPos[0]][p_oldPos[1]] = Empty()

            self.board[p_newPos[0]][p_newPos[1]] =  self.board[p_oldPos[0]][p_oldPos[1]] 
            self.board[p_oldPos[0]][p_oldPos[1]] = Empty()
            return 0

        return 1

    def isUnderAttack(self, pos, white):
        r_dir = ((1,0), (0,1), (-1,0), (0,-1))
        b_dir = ((1,1), (1,-1), (-1,1), (-1, -1))
        n_dir = ((2,1), (2,-1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        # rook + queen check
        for i in r_dir:
            row, col = parseNotation(pos)
            while isWithinBounds(row+i[0], col+i[1]):
                if isinstance(self.board[row+i[0]][col+i[1]], Empty):
                    row += i[0]
                    col += i[1]
                    continue
                if self.board[row+i[0]][col+i[1]].white is white:
                    break
                elif (isinstance(self.board[row+i[0]][col+i[1]], Rook) or isinstance(self.board[row+i[0]][col+i[1]], Queen)):
                    return True
                else:
                    break
        # bishop + queen check
        for i in b_dir:
            row, col = parseNotation(pos)
            while isWithinBounds(row+i[0], col+i[1]):
                if isinstance(self.board[row+i[0]][col+i[1]], Empty):
                    row += i[0]
                    col += i[1]
                    continue
                if self.board[row+i[0]][col+i[1]].white is white:
                    break
                elif (isinstance(self.board[row+i[0]][col+i[1]], Bishop) or isinstance(self.board[row+i[0]][col+i[1]], Queen)):
                    return True
                else:
                    break

        
        # from this point on row, col won't need to change
        row, col = parseNotation(pos)

        # knite check
        for i in n_dir:
            if isWithinBounds(row+i[0],col+i[1]):
                if isinstance(self.board[row+i[0]][col+i[1]], Knight) and self.board[row+i[0]][col+i[1]].white is not white: 

                    return True
       # pawn check
        if isWithinBounds(row+1, col+1):
            if isinstance(self.board[row+1][col+1], Pawn) and self.board[row+1][col+1].white is not white and self.board[row+1][col+1].white is True: 
                return True
        if isWithinBounds(row+1, col-1):
            if isinstance(self.board[row+1][col-1], Pawn) and self.board[row+1][col-1].white is not white and self.board[row+1][col-1].white is True: 
                return True
        if isWithinBounds(row-1, col+1):
            if isinstance(self.board[row-1][col+1], Pawn) and self.board[row-1][col-1].white is not white and self.board[row-1][col-1].white is False: 
                return True
        if isWithinBounds(row-1, col-1):
            if isinstance(self.board[row-1][col-1], Pawn) and self.board[row-1][col+1].white is not white and self.board[row-1][col+1].white is False: 
                return True

        # king check
        dir = ((0,1), (1,1), (1,0), (1, -1), (0, -1), (-1,-1), (-1,0))
        for i in dir:
            if isWithinBounds(row+i[0], col+i[1]) and isWithinBounds(row, col):
                if isinstance(self.board[row+i[0]][col+i[1]], King) and self.board[row+i[0]][col+i[1]].white is not white:
                    return True

        return False

    def checkCheck(self, color):
        white = True if color == 'white' else False
        
        pos = (self.getKingPos())[white]
        if self.isUnderAttack(pos, white):
            return True
        return False
    def checkCheckmate(self):
        pos = (self.getKingPos()) 
        for i in pos.keys():
            if self.checkCheck(i) and len(self.board[pos[i][0]][pos[i][1]].getLegalMoves()) == 0:
                return True
        return False


class Empty: 
    def __init__(self):
        self.alias = ' '
        self.white = None
    def getLegalMoves(self):
        return []
    def printLegalMoves(self):
        pass # function not needed for empty, but might still be ran


class Piece:
    def __init__(self, game):
        self.game = game
    def validateDirection(self, dir):
        listOfMoves = []
        for i in dir:
            row, col = self.game.getPossition(self)
            while isWithinBounds(row+i[0], col+i[1]):
                if isinstance(self.game.board[row+i[0]][col+i[1]], Empty):
                    listOfMoves.append((row+i[0], col+i[1]))
                elif self.game.board[row+i[0]][col+i[1]].white is not self.white:
                    listOfMoves.append((row+i[0], col+i[1]))
                    break
                else:
                    break
                row+=i[0]
                col+=i[1]
        return listOfMoves
    def getLegalMoves(self):
        raise NotImplementedError('overwritten by subclass')

    def printLegalMoves(self):
        temp = copy.deepcopy(self.game) 
        legalMoves = self.getLegalMoves()
        if legalMoves is not None:
            for move in legalMoves:
                temp.board[move[0]][move[1]] = '.'
            temp.printBoard()
class Pawn(Piece):
    def __init__(self, white, game):
        self.white = white
        self.moved = False
        self.alias = 'P' if white else 'p'
        self.game = game # Game class
    
    def getLegalMoves(self): # runs though game.board[pos].getLegalMoves
        row, col = self.game.getPossition(self) 
        listOfMoves = []

        if self.alias == 'P':  # White pawn moves upward on the board
            if isWithinBounds(row - 1, col) and isinstance(self.game.board[row - 1][col], Empty):
                listOfMoves.append((row - 1, col))
            
            # Initial double move for white pawn
            if row == 6 and isinstance(self.game.board[row - 1][col], Empty) and isinstance(self.game.board[row - 2][col], Empty):
                listOfMoves.append((row - 2, col))
                
            # Capture diagonally for white pawn
            if isWithinBounds(row - 1, col + 1) and not isinstance(self.game.board[row - 1][col + 1], Empty) and self.game.board[row - 1][col + 1].white != self.white:
                listOfMoves.append((row - 1, col + 1))
            if isWithinBounds(row - 1, col - 1) and not isinstance(self.game.board[row - 1][col - 1], Empty) and self.game.board[row - 1][col - 1].white != self.white:
                listOfMoves.append((row - 1, col - 1))

        elif self.alias == 'p':  # Black pawn moves downward on the board
            if isWithinBounds(row + 1, col) and isinstance(self.game.board[row + 1][col], Empty):
                listOfMoves.append((row + 1, col))

            # Initial double move for black pawn
            if row == 1 and isinstance(self.game.board[row + 1][col], Empty) and isinstance(self.game.board[row + 2][col], Empty):
                listOfMoves.append((row + 2, col))
                
            # Capture diagonally for black pawn
            if isWithinBounds(row + 1, col + 1) and not isinstance(self.game.board[row + 1][col + 1], Empty) and self.game.board[row + 1][col + 1].white != self.white:
                listOfMoves.append((row + 1, col + 1))
            if isWithinBounds(row + 1, col - 1) and not isinstance(self.game.board[row + 1][col - 1], Empty) and self.game.board[row + 1][col - 1].white != self.white:
                listOfMoves.append((row + 1, col - 1))

        return listOfMoves

class Bishop(Piece):
    def __init__(self, white, game):
        self.moved = False
        self.white = white
        self.alias = 'B' if white else 'b'
        self.game = game
    
    def getLegalMoves(self):
        dir = ((1,1), (1,-1), (-1,1), (-1, -1))
        return self.validateDirection(dir)

class Rook(Piece):
    def __init__(self, white, game):
        self.moved = False
        self.white = white
        self.alias = 'R' if white else 'r'
        self.game = game

    
    def getLegalMoves(self):
        dir = ((1,0), (0,1), (-1,0), (0,-1))
        return self.validateDirection(dir)

class Knight(Piece):
    def __init__(self, white, game):
        self.moved = False
        self.white = white
        self.alias = 'N' if white else 'n'
        self.game = game

    
    def getLegalMoves(self):
        listOfMoves = []
        row, col = self.game.getPossition(self)
        dir = ((2,1), (2,-1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for i in dir:
            if isWithinBounds(row+i[0], col+i[1]):
                if isinstance(self.game.board[row+i[0]][col+i[1]], Empty) or self.game.board[row+i[0]][col+i[1]].white is not self.white:
                    listOfMoves.append((row+i[0], col+i[1]))
        return listOfMoves
class Queen(Piece):
    def __init__(self, white, game):
        self.moved = False
        self.white = white
        self.alias = 'Q' if white else 'q'
        self.game = game

    
    def getLegalMoves(self):
        dir = ((1,1), (1,-1), (-1,1), (-1, -1), (1,0), (0,1), (-1,0), (0,-1))
        return self.validateDirection(dir)

class King(Piece):
    def __init__(self, white, game):
        self.moved = False
        self.white = white
        self.alias = 'K' if white else 'k'
        self.game = game

         
    def getLegalMoves(self):
        listOfMoves = []
        row, col = self.game.getPossition(self)
        dir = ((0,1), (1,1), (1,0), (1, -1), (0, -1), (-1,-1), (-1,0))
        for i in dir:
            if not isWithinBounds(row,col) or not isWithinBounds(row+i[0], col+i[1]):
                continue
            if not self.game.isUnderAttack((row+i[0],col+i[1]), self.white):
                if isinstance(self.game.board[row+i[0]][col+i[1]], Empty) or self.game.board[row+i[0]][col+i[1]].white is not self.game.board[row][col].white:
                    listOfMoves.append((row+i[0], col+i[1])) 
        return listOfMoves

def main():
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen

    chess = Game()
    chess.initalize()

    # chess.printBoard()
    moves= [
    "d2:d4", "c7:c5",
    "d4:d5", "e7:e6",
    "b1:c3", "e6:d5",
    "c3:d5", "g8:e7",
    "c1:g5", "h7:h6",
    "g5:h4", "d8:a5",
    "c2:c3", "e7:f5",
    "d1:a4", "a5:a4",
    # "d5:c7", #checkmatec
]
    move = 0
    turn = 'white'

    while not chess.checkCheckmate():
        turn = 'white' if move % 2 == 0 else 'black'
        

        print('player: ', turn) 
        if int(move) < len(moves):
            i = moves[int(move)]
            time.sleep(0.1)
        else:
            if move == 16:
                print('Can you find the mate in one?')
            i = input('input [E2] or [E2:E4] (without quotes): ' if move <= 3 else 'input [E2] or [E2:E4]: ')

        os.system('cls' if os.name == 'nt' else 'clear')        
        # parsing i (input)
        i = i.split(':') 

        try:
            # if split = len 1 ie: E3
            if len(i) == 1:
                pos = parseNotation(i[0])
                if isinstance(chess.board[pos[0]][pos[1]], Empty):
                    raise Exception
                chess.board[pos[0]][pos[1]].printLegalMoves()
                continue 
            elif len(i) == 2:
                moveLegal = chess.move(i[0],i[1], turn)
                if moveLegal == 1:
                    raise Exception
                chess.printBoard()
        except Exception as e: # Input invalid? try again, unless input is form a testcase, then return
            if int(move) < len(moves):
                move+=1
                continue
            chess.printBoard()
            print('invalid move')
            continue
        move += 1
    print('white' if move % 2 == 0 else 'black', ' wins!')
    
main()
