from pickle import load
import pygame

class Piece():

#    def __init__(self, position, color, img):
    def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
        self.tile_position = tile_position
        self.img_position = img_position
        self.color = color
        self.img = img
        self.old_tile_position = tile_position
        self.old_img_position = img_position

    def move(self, move_to: tuple[int, int]) -> None:
        self.old_tile_position = self.tile_position
        self.old_img_position = self.img_position
        self.img_position = move_to[0]*113, move_to[1]*113+1
        self.tile_position = move_to 

    def return_old(self):
       self.img_position = self.old_img_position 
       self.tile_position = self.old_tile_position

    def is_move_possible(self,move:tuple[int, int], check_state: bool, board: list[list])-> bool:
        if -1>=move[1] or move[1]>=8 or -1>=move[0] or move[0]>=8:
            return False 
        elif board[move[0]][move[1]] == None:
            return True 
        elif board[move[0]][move[1]]:
            if board[move[0]][move[1]].color != self.color: 
                return True
            else:
                return False
        return False

class King(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "king"
            self.not_moved = True
            

        def check_around(self, tile_position, check_state, board):
            
            if self.is_move_possible((tile_position[0]-1, tile_position[1]) ,check_state, board) and board[tile_position[0]-1][tile_position[1]] != None and  board[tile_position[0]-1][tile_position[1]].name == "king": 
                return False
            if self.is_move_possible((tile_position[0]-1, tile_position[1]-1) ,check_state, board)and board[tile_position[0]-1][tile_position[1]-1] != None and  board[tile_position[0]-1][tile_position[1]-1].name == "king": 
                return False
            if self.is_move_possible((tile_position[0]-1, tile_position[1]+1) ,check_state, board) and board[tile_position[0]-1][tile_position[1]+1] != None and  board[tile_position[0]-1][tile_position[1]+1].name == "king":
                return False
            if self.is_move_possible((tile_position[0]+1, tile_position[1]) ,check_state, board) and board[tile_position[0]+1][tile_position[1]] != None and  board[tile_position[0]+1][tile_position[1]].name == "king": 
                return False
            if  self.is_move_possible((tile_position[0]+1, tile_position[1]-1) ,check_state, board) and board[tile_position[0]+1][tile_position[1]-1] != None and  board[tile_position[0]+1][tile_position[1]-1].name == "king": 
                return False
            if self.is_move_possible((tile_position[0]+1, tile_position[1]+1) ,check_state, board) and board[tile_position[0]+1][tile_position[1]+1] != None and  board[tile_position[0]+1][tile_position[1]+1].name == "king": 
                return False
            if self.is_move_possible((tile_position[0], tile_position[1]-1) ,check_state, board) and board[tile_position[0]][tile_position[1]-1] != None and  board[tile_position[0]][tile_position[1]-1].name == "king": 
                return False
            if  self.is_move_possible((tile_position[0], tile_position[1]+1) ,check_state, board) and board[tile_position[0]][tile_position[1]+1] != None and  board[tile_position[0]][tile_position[1]+1].name == "king": 
                return False
            
            return True 

        def possible_moves(self, check_state: bool, board: list[list], controlled_squares ) ->list[tuple[int, int]]:
            pm = []
            
 

            if self.is_move_possible((self.tile_position[0] - 1, self.tile_position[1]), check_state, board) and self.check_around((self.tile_position[0] - 1, self.tile_position[1]), check_state, board):
                pm.append((self.tile_position[0] - 1, self.tile_position[1]))
            if self.is_move_possible((self.tile_position[0] - 1, self.tile_position[1] + 1), check_state, board) and self.check_around((self.tile_position[0] - 1, self.tile_position[1] + 1), check_state, board):
                pm.append((self.tile_position[0] - 1, self.tile_position[1] + 1))
            if self.is_move_possible((self.tile_position[0] - 1, self.tile_position[1] - 1), check_state, board) and self.check_around((self.tile_position[0] - 1, self.tile_position[1] - 1), check_state, board):
                pm.append((self.tile_position[0] - 1, self.tile_position[1] - 1))
            if self.is_move_possible((self.tile_position[0] + 1, self.tile_position[1]), check_state, board) and self.check_around((self.tile_position[0] + 1, self.tile_position[1]), check_state, board):
                pm.append((self.tile_position[0] + 1, self.tile_position[1]))
            if self.is_move_possible((self.tile_position[0] + 1, self.tile_position[1] + 1), check_state, board) and self.check_around((self.tile_position[0] + 1, self.tile_position[1] + 1), check_state, board):
                pm.append((self.tile_position[0] + 1, self.tile_position[1] + 1))
            if self.is_move_possible((self.tile_position[0] + 1, self.tile_position[1] - 1), check_state, board) and self.check_around((self.tile_position[0] + 1, self.tile_position[1] - 1), check_state, board):
                pm.append((self.tile_position[0] + 1, self.tile_position[1] - 1))
            if self.is_move_possible((self.tile_position[0], self.tile_position[1] - 1), check_state, board) and self.check_around((self.tile_position[0], self.tile_position[1] - 1), check_state, board):
                pm.append((self.tile_position[0], self.tile_position[1] - 1))
            if self.is_move_possible((self.tile_position[0], self.tile_position[1] + 1), check_state, board) and self.check_around((self.tile_position[0], self.tile_position[1] + 1), check_state, board):
                pm.append((self.tile_position[0], self.tile_position[1] + 1))

            
            #castles
            if self.not_moved:
                if board[0][self.tile_position[1]] and board[0][self.tile_position[1]].name == "rook" and board[0][self.tile_position[1]].not_moved:
                    if self.check_castle((0, self.tile_position[1]), board, controlled_squares):
                        pm.append((0, self.tile_position[1]))
            
                if board[7][self.tile_position[1]] and board[7][self.tile_position[1]].name == "rook" and board[7][self.tile_position[1]].not_moved:
                    if self.check_castle((7, self.tile_position[1]), board, controlled_squares):
                        pm.append((7, self.tile_position[1]))

            return pm
        
        def check_castle(self, position:tuple[int, int], board:list[list], controlled_squares: list) ->bool:
            if position[0] > self.tile_position[0]:
                for i in range(self.tile_position[0]+1,position[0]):
                    if board[i][position[1]] != None or (i, position[1]) in controlled_squares:
                        return False
            else:
                for i in range(position[0]+1, self.tile_position[0]):
                    if board[i][position[1]] != None or (i, position[1]) in controlled_squares:
                        return False
            return True

class Queen(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "queen"
            self.not_moved = True

        def can_move(self, move_to: tuple[int,int], piece: Piece) -> bool: 
            if not piece or  piece.color != self.color: 
                return (move_to[0] == self.tile_position[0]) or (move_to[1] == self.tile_position[1]) or (abs(self.tile_position[0] - move_to[0]) == abs(self.tile_position[1] - move_to[1])) 

        def possible_moves(self, check_state: bool, board: list[list],controlled_squares) ->list[tuple[int, int]]:
            pm = Bishop.possible_moves(self, check_state, board, controlled_squares) + Rook.possible_moves(self, check_state, board, controlled_squares)
            return pm


class Bishop(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "bishop"
            self.not_moved = True

        def can_move(self, move_to: tuple[int,int], piece: Piece) -> bool: 
            if not piece or  piece.color != self.color: 
                return (abs(self.tile_position[0] - move_to[0]) == abs(self.tile_position[1] - move_to[1])) 
        
        def possible_moves(self, check_state: bool, board: list[list],controlled_squares) ->list[tuple[int, int]]:
            pm = []
            

            #why this code looks so awful?
            #probably can be improved
            x, y = self.tile_position[0] + 1, self.tile_position[1] + 1
            while x < 8 and y < 8:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        pm.append((x, y))
                    break
                pm.append((x,y))
                x+=1
                y+=1
            
            x, y = self.tile_position[0] + 1, self.tile_position[1] - 1
            while x < 8 and y > -1:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        pm.append((x, y))
                    break
                pm.append((x,y))
                x+=1
                y-=1
            
            x, y = self.tile_position[0] - 1, self.tile_position[1] + 1
            while x > -1 and y < 8:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        pm.append((x, y))
                    break
                pm.append((x,y))
                x-=1
                y+=1
            
            x, y = self.tile_position[0] - 1, self.tile_position[1] - 1
            while x >- 1 and y > -1:
                if board[x][y]:
                    if board[x][y].color != self.color:
                        pm.append((x, y))
                    break
                pm.append((x,y))
                x-=1
                y-=1
            return pm

class Knight(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "knight"
            self.not_moved = True

        def can_move(self, move_to: tuple[int,int], piece: Piece) -> bool: 
            if not piece or  piece.color != self.color: 
                return ((abs(self.tile_position[0] - move_to[0]) == 1) and (abs(self.tile_position[1] - move_to[1]) == 2)) or ((abs(self.tile_position[0] - move_to[0]) == 2) and (abs(self.tile_position[1] - move_to[1]) == 1))  


        
        def possible_moves(self, check_state: bool, board: list[list],controlled_squares) ->list[tuple[int, int]]:

            pm = []
            if self.tile_position[0] -2 > -1 and self.tile_position[1] -1 > -1: 
                if (board[self.tile_position[0] - 2][self.tile_position[1] - 1] and board[self.tile_position[0] - 2][self.tile_position[1] - 1].color != self.color) or  board[self.tile_position[0] - 2][self.tile_position[1] - 1] == None:
                    pm.append((self.tile_position[0] - 2, self.tile_position[1] - 1))

            if self.tile_position[0] -2 > -1 and self.tile_position[1] + 1 < 8: 
                if (board[self.tile_position[0] - 2][self.tile_position[1] + 1] and board[self.tile_position[0] - 2][self.tile_position[1] + 1].color != self.color) or  board[self.tile_position[0] - 2][self.tile_position[1] + 1] == None:
                    pm.append((self.tile_position[0] - 2, self.tile_position[1] + 1))
                    
            if self.tile_position[0]  +2 < 8 and self.tile_position[1] -1 > -1:
                if (board[self.tile_position[0] + 2][self.tile_position[1] - 1] and board[self.tile_position[0] + 2][self.tile_position[1] - 1].color != self.color) or  board[self.tile_position[0] + 2][self.tile_position[1] - 1] == None:
                    pm.append((self.tile_position[0] + 2, self.tile_position[1] - 1))

            if self.tile_position[0] + 2 < 8 and self.tile_position[1] + 1 < 8:
                if (board[self.tile_position[0] + 2][self.tile_position[1] + 1] and board[self.tile_position[0] + 2][self.tile_position[1] + 1].color != self.color) or  board[self.tile_position[0] + 2][self.tile_position[1] + 1] == None:
                    pm.append((self.tile_position[0] + 2, self.tile_position[1] + 1))
            
            if self.tile_position[0] - 1 > -1 and self.tile_position[1] + 2 < 8:
                if (board[self.tile_position[0] - 1][self.tile_position[1] + 2] and board[self.tile_position[0] - 1][self.tile_position[1] + 2].color != self.color) or  board[self.tile_position[0] - 1][self.tile_position[1] + 2] == None:
                    pm.append((self.tile_position[0] - 1, self.tile_position[1] + 2))
                
            if self.tile_position[0] + 1 > -1  and self.tile_position[1] - 2 > -1:
                if (board[self.tile_position[0] - 1][self.tile_position[1] - 2] and board[self.tile_position[0] - 1][self.tile_position[1] - 2].color != self.color) or  board[self.tile_position[0] - 1][self.tile_position[1] - 2] == None:
                    pm.append((self.tile_position[0] - 1, self.tile_position[1] - 2))
                
            if self.tile_position[0] + 1 < 8 and self.tile_position[1] + 2 < 8:
                if (self.tile_position[0] + 1 < 8 and self.tile_position[1] + 2 < 8 and board[self.tile_position[0] + 1][self.tile_position[1] + 2] and board[self.tile_position[0] + 1][self.tile_position[1] + 2].color != self.color) or  board[self.tile_position[0] + 1][self.tile_position[1] + 2] == None:
                    pm.append((self.tile_position[0] + 1, self.tile_position[1] + 2))
                
            if self.tile_position[0] + 1 < 8 and self.tile_position[1] - 2 > -1:
                if (board[self.tile_position[0] + 1][self.tile_position[1] - 2] and board[self.tile_position[0] + 1][self.tile_position[1] - 2].color != self.color) or  board[self.tile_position[0] + 1][self.tile_position[1] - 2] == None:
                    pm.append((self.tile_position[0] + 1, self.tile_position[1] - 2))
            return pm




        


class Rook(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "rook"
            self.not_moved= True

        def can_move(self, move_to: tuple[int,int], piece: Piece) -> bool: 
            if not piece or  piece.color != self.color: 
                return (move_to[0] == self.tile_position[0]) or (move_to[1] == self.tile_position[1])
        



        def possible_moves(self, check_state: bool, board: list[list],controlled_squares) -> list[tuple[int, int]]:
            pm = []
            x = self.tile_position[0] + 1
            while x < 8:
                if board[x][self.tile_position[1]]:
                    if board[x][self.tile_position[1]].color != self.color:
                        pm.append((x, self.tile_position[1]))
                    break
                pm.append((x, self.tile_position[1]))
                x += 1
            x = self.tile_position[0] - 1
            while x > -1:
                if board[x][self.tile_position[1]]:
                    if board[x][self.tile_position[1]].color != self.color:
                        pm.append((x, self.tile_position[1]))
                    break
                pm.append((x, self.tile_position[1]))
                x -= 1
            y = self.tile_position[1] + 1
            while y < 8:
                if board[self.tile_position[0]][y]:
                    if board[self.tile_position[0]][y].color != self.color:
                        pm.append((self.tile_position[0], y))
                    break
                pm.append((self.tile_position[0], y))
                y += 1
            y = self.tile_position[1] - 1 
            while y > -1:
                if board[self.tile_position[0]][y]:
                    if board[self.tile_position[0]][y].color != self.color:
                        pm.append((self.tile_position[0], y))
                    break
                pm.append((self.tile_position[0], y))
                y -= 1
            return pm


"""

                if board[self.tile_position[1]][y] != None:
                    if board[self.tile_position[1]][y].color != self.color:
                        pm.append((self.tile_position[0], y))
                    break




"""
class Pawn(Piece):

        def __init__(self, tile_position: tuple[int, int], color: str, img: pygame.image, img_position: tuple[int, int]) -> None:
            super().__init__(tile_position, color, img, img_position)
            self.name = "pawn"
            self.en_passant = 0 
            self.not_moved = True

        def can_move(self, move_to: tuple[int,int], piece: Piece) -> bool: 
            empty = piece == None
            if self.color == "white":
                return (not empty and (abs(self.tile_position[0] - move_to[0])) == 1 and self.tile_position[1] - move_to[1] == 1) or (self.tile_position[1] - move_to[1] == 1 and self.tile_position[0] == move_to[0] and empty) 
            else:
                return (not empty and (abs(self.tile_position[0] - move_to[0])) == 1 and self.tile_position[1] - move_to[1] == -1) or (self.tile_position[1] - move_to[1] == -1 and self.tile_position[0] == move_to[0] and empty)
      

        def possible_moves(self, check_state: bool, board: list[list],controlled_squares) -> list[tuple[int,int]]:
            pm = []
            if self.color == "white":
                if board[self.tile_position[0]][self.tile_position[1] - 1] == None:
                    pm.append((self.tile_position[0], self.tile_position[1] - 1))
                if self.tile_position[1] == 6:
                    pm.append((self.tile_position[0], self.tile_position[1] - 2))
                if self.tile_position[0] - 1 > -1 and self.tile_position[1] - 1 > -1: 
                    if board[self.tile_position[0] - 1][self.tile_position[1] - 1] != None:
                        if board[self.tile_position[0] - 1][self.tile_position[1] - 1].color == "black" :
                            pm.append((self.tile_position[0] - 1, self.tile_position[1] - 1))
                  

                if self.tile_position[0] + 1 < 7 and self.tile_position[1] - 1 > -1: 
                    if board[self.tile_position[0] + 1][self.tile_position[1] - 1] != None:
                        if board[self.tile_position[0] + 1][self.tile_position[1] - 1].color == "black" :
                            pm.append((self.tile_position[0] + 1, self.tile_position[1] - 1))
                
                if self.en_passant != 0:
                    pm.append((self.tile_position[0] + self.en_passant, self.tile_position[1] - 1))
            else:
                if board[self.tile_position[0]][self.tile_position[1] + 1] == None:
                    pm.append((self.tile_position[0], self.tile_position[1] + 1)) 
                
                if self.tile_position[1] == 1:
                    pm.append((self.tile_position[0], self.tile_position[1] + 2))
                
                if self.tile_position[0] - 1 > -1 and self.tile_position[1] + 1 < 7: 
                    if board[self.tile_position[0] - 1][self.tile_position[1] + 1] != None:
                        if board[self.tile_position[0] - 1][self.tile_position[1] + 1].color == "white" :
                            pm.append((self.tile_position[0] - 1, self.tile_position[1] + 1))
                
                if self.tile_position[0] + 1 < 7 and self.tile_position[1] + 1 < 7: 
                    if board[self.tile_position[0] + 1][self.tile_position[1] + 1] != None:
                        if board[self.tile_position[0] + 1][self.tile_position[1] + 1].color == "white" :
                            pm.append((self.tile_position[0] + 1, self.tile_position[1] + 1))

                if self.en_passant != 0:
                    pm.append((self.tile_position[0] + self.en_passant, self.tile_position[1] + 1))

            return pm


#king
image = pygame.image.load("img/king1.png") 
KING_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/king.png") 
W_KING_IMG= pygame.transform.scale(image, (110, 110))

#queen
image = pygame.image.load("img/queen1.png") 
QUEEN_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/queen.png") 
W_QUEEN_IMG= pygame.transform.scale(image, (110, 110))
    
#bishop
image = pygame.image.load("img/bishop1.png") 
BISHOP_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/bishop.png") 
W_BISHOP_IMG = pygame.transform.scale(image, (110, 110))

#knight
image = pygame.image.load("img/knight1.png") 
KNIGHT_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/knight.png") 
W_KNIGHT_IMG= pygame.transform.scale(image, (110, 110))
    
#rook
image = pygame.image.load("img/rook1.png") 
ROOK_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/rook.png") 
W_ROOK_IMG= pygame.transform.scale(image, (110, 110))
    
#pawn
image = pygame.image.load("img/pawn1.png") 
PAWN_IMG = pygame.transform.scale(image, (110, 110))
image = pygame.image.load("img/pawn.png")  
W_PAWN_IMG= pygame.transform.scale(image,(110, 110))


def create_pieces():
    
    is_player_white = True

    
#--- Create Pieces ---
    #empty board
    board = []
    for x in range(8):
        board.append([])
        for y in range(8):
            board[x].append(None)


    if is_player_white:
    #Black pieces
        #    [x][y]                          (x,y)
        board[0][0] = Rook(  tile_position = (0,0), color="black", img= ROOK_IMG,   img_position=(0,       1))
        board[1][0] = Knight(tile_position = (1,0), color="black", img= KNIGHT_IMG, img_position=(1*113+1, 1))
        board[2][0] = Bishop(tile_position = (2,0), color="black", img= BISHOP_IMG, img_position=(2*113+1, 1))
        board[3][0] = Queen( tile_position = (3,0), color="black", img= QUEEN_IMG,  img_position=(3*113+1, 1))
        board[4][0] = King(  tile_position = (4,0), color="black", img= KING_IMG,   img_position=(4*113+1, 1))
        board[5][0] = Bishop(tile_position = (5,0), color="black", img= BISHOP_IMG, img_position=(5*113+1, 1))
        board[6][0] = Knight(tile_position = (6,0), color="black", img= KNIGHT_IMG, img_position=(6*113+1, 1))
        board[7][0] = Rook(  tile_position = (7,0), color="black", img= ROOK_IMG,   img_position=(7*113+1, 1))

        #    [x][y]                     
        board[0][1] = Pawn(  tile_position = (0,1), color="black", img= PAWN_IMG, img_position=(0,       114))
        board[1][1] = Pawn(  tile_position = (1,1), color="black", img= PAWN_IMG, img_position=(1*113+1, 114))
        board[2][1] = Pawn(  tile_position = (2,1), color="black", img= PAWN_IMG, img_position=(2*113+1, 114))
        board[3][1] = Pawn(  tile_position = (3,1), color="black", img= PAWN_IMG, img_position=(3*113+1, 114))
        board[4][1] = Pawn(  tile_position = (4,1), color="black", img= PAWN_IMG, img_position=(4*113+1, 114))
        board[5][1] = Pawn(  tile_position = (5,1), color="black", img= PAWN_IMG, img_position=(5*113+1, 114))
        board[6][1] = Pawn(  tile_position = (6,1), color="black", img= PAWN_IMG, img_position=(6*113+1, 114))
        board[7][1] = Pawn(  tile_position = (7,1), color="black", img= PAWN_IMG, img_position=(7*113+1, 114))
    
    #White pieces
        #    [x][y]                          (x,y)
        board[0][7] = Rook(  tile_position = (0,7), color="white", img= W_ROOK_IMG,   img_position=(0,       792))
        board[1][7] = Knight(tile_position = (1,7), color="white", img= W_KNIGHT_IMG, img_position=(1*113+1, 792))
        board[2][7] = Bishop(tile_position = (2,7), color="white", img= W_BISHOP_IMG, img_position=(2*113+1, 792))
        board[3][7] = Queen( tile_position = (3,7), color="white", img= W_QUEEN_IMG,  img_position=(3*113+1, 792))
        board[4][7] = King(  tile_position = (4,7), color="white", img= W_KING_IMG,   img_position=(4*113+1, 792))
        board[5][7] = Bishop(tile_position = (5,7), color="white", img= W_BISHOP_IMG, img_position=(5*113+1, 792))
        board[6][7] = Knight(tile_position = (6,7), color="white", img= W_KNIGHT_IMG, img_position=(6*113+1, 792))
        board[7][7] = Rook(  tile_position = (7,7), color="white", img= W_ROOK_IMG,   img_position=(7*113+1, 792))

        #    [x][y]                     
        board[0][6] = Pawn(  tile_position = (0,6), color="white", img= W_PAWN_IMG, img_position=(0,       679))
        board[1][6] = Pawn(  tile_position = (1,6), color="white", img= W_PAWN_IMG, img_position=(1*113+1, 679))
        board[2][6] = Pawn(  tile_position = (2,6), color="white", img= W_PAWN_IMG, img_position=(2*113+1, 679))
        board[3][6] = Pawn(  tile_position = (3,6), color="white", img= W_PAWN_IMG, img_position=(3*113+1, 679))
        board[4][6] = Pawn(  tile_position = (4,6), color="white", img= W_PAWN_IMG, img_position=(4*113+1, 679))
        board[5][6] = Pawn(  tile_position = (5,6), color="white", img= W_PAWN_IMG, img_position=(5*113+1, 679))
        board[6][6] = Pawn(  tile_position = (6,6), color="white", img= W_PAWN_IMG, img_position=(6*113+1, 679))
        board[7][6] = Pawn(  tile_position = (7,6), color="white", img= W_PAWN_IMG, img_position=(7*113+1, 679))
    

    return board


def debug_board():


    board = []
    for x in range(8):
        board.append([])
        for y in range(8):
            board[x].append(None)
        
    board[0][1] = Pawn(  tile_position = (0,1), color="white", img= W_PAWN_IMG, img_position=(0,    1*113 + 1))
    board[7][6] = Pawn(  tile_position = (7,6), color="black", img= PAWN_IMG, img_position=(7*113+1, 6*113 + 1))
    
    return board

def fen_to_board(fen: str):

    board = []
    for x in range(8):
        board.append([])
        for y in range(8):
            board[x].append(None)

    rows = fen.split("/")

    
    x = 0
    y = 0
    for row in rows:
        for c in row:
            try:
                c = int(c)
                x += c
            except:
                color = "black" if c.islower() else "white"
                c = c.lower()
                match c:

                        case "k":#King
                            board[x][y] = King(  tile_position = (x,y), color=color, img= (W_KING_IMG if color == "white" else KING_IMG),   img_position=(x*113+1, y*113 +1))
                        case "q":#Queen
                            board[x][y] = Queen(  tile_position = (x,y), color=color, img= (W_QUEEN_IMG if color == "white" else QUEEN_IMG),   img_position=(x*113+1, y*113 +1))
                        case "n":#Knight
                            board[x][y] = Knight(  tile_position = (x,y), color=color, img= (W_KNIGHT_IMG if color == "white" else KNIGHT_IMG),   img_position=(x*113+1, y*113 +1))
                        case "b":#Bishop
                            board[x][y] = Bishop(  tile_position = (x,y), color=color, img= (W_BISHOP_IMG if color == "white" else BISHOP_IMG),   img_position=(x*113+1, y*113 +1))
                        case "r":#Rook
                            board[x][y] = Rook(  tile_position = (x,y), color=color, img= (W_ROOK_IMG if color == "white" else ROOK_IMG),   img_position=(x*113+1, y*113 +1))
                        case "p":#Pawn
                            board[x][y] = Pawn(  tile_position = (x,y), color=color, img= (W_PAWN_IMG if color == "white" else PAWN_IMG),   img_position=(x*113+1, y*113 +1))
                x+=1
            print(x,y)

        y += 1
        x = 0

    return board
