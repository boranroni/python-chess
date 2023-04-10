import pygame
import sys
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
from settings import W_SIZE, GRID, DARK, LIGHT, GREY
from pieces import Piece
from board import Board
import time
import pprint
# TODO:
# Main to do list:
# write perft debug fucntion
# then
# calculate perft


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        # chess icon by Freepik from flaticon.com
        programIcon = pygame.image.load('img\\icon.png')
        pygame.display.set_icon(programIcon)
        self.screen = pygame.display.set_mode(
            W_SIZE, HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.clock = pygame.time.Clock()
        self.clicked_square = None
        self.board = Board().create()
        self.check = False
        self.white_turn = True

        self.en_passant_sqr = None
        self.en_passant_color = None

        # Available castles
        self.wr_c = True
        self.wl_c = True
        self.br_c = True
        self.bl_c = True

        self.white_king = 60
        self.black_king = 4

        self.possible_moves = self.all_possible_moves()

    # Graphical function
    def create_graphical_board(self, flip=False):
        dark = True if flip else False
        y = 0
        for file in range(8):
            x = 0
            for rank in range(8):
                pygame.draw.rect(self.screen, DARK if dark else LIGHT, [
                                 x, y, GRID, GRID])

                dark = False if dark else True
                x += GRID
            dark = False if dark else True
            y += GRID

    def render_piece(self, piece: int, square: int):
        if piece == 0:
            return
        white = True if piece < 15 else False
        piece = piece & ((1 << 3) - 1)
        x, y = sqr_to_cart(square)
        return Piece(piece, x, y, white, GRID)

    def render_move_circle(self):
        # Circle rendered on the available square.
        s = pygame.Surface((W_SIZE))
        s.set_colorkey((0, 0, 0))
        half = GRID//2
        if not self.clicked_square or self.clicked_square not in self.possible_moves:
            return s
        for move in self.possible_moves[self.clicked_square]:
            pygame.draw.circle(s, GREY, tuple((i + half)
                               for i in sqr_to_cart(move)), GRID//4)
        return s

    def window_resize(self, new_size: tuple):
        global GRID, W_SIZE
        self.screen = pygame.display.set_mode(
            new_size, HWSURFACE | DOUBLEBUF | RESIZABLE)
        W_SIZE = new_size
        GRID = min(new_size)//8

    # Movement function
    def king_move(self, sqr: int, white: bool):

        if sqr % 8 == 0:
            m = [sqr+1,  sqr+8, sqr-8, sqr+9, sqr-7]
        elif sqr % 8 == 7:
            m = [sqr-1, sqr+8, sqr-8, sqr-9, sqr+7]
        else:
            m = [sqr+1, sqr-1, sqr+8, sqr-8, sqr+9, sqr-9, sqr+7, sqr-7]
        if ((white and self.wl_c) or (not white and self.bl_c)):
            # Checking if the squares is controlled
            if not (self.board[sqr+1] or self.board[sqr+2]):
                if not (self.is_king_checked(self.white_turn, sqr+1) or self.is_king_checked(self.white_turn, sqr+2)):
                    m.append(sqr + 2)

        if (white and self.wr_c) or (not white and self.br_c):
            # Checking if the squares is controlled
            if not (self.board[sqr-1] or self.board[sqr-2] or self.board[sqr-3]):
                if not (self.is_king_checked(self.white_turn, sqr+1) or self.is_king_checked(self.white_turn, sqr) or self.is_king_checked(self.white_turn, sqr-1)):
                    m.append(sqr - 2)
        mf = []
        for move in m:
            if move > 63 or move < 0:
                continue
            if self.board[move]:
                if self.right_color(self.board[move]):
                    continue
            mf.append(move)

        return mf

    def pawn_move(self, square: int, white: bool):
        m = []
        if white:
            if 47 < square < 56 and not self.board[square-8] and not self.board[square-16]:
                m.append(square-16)

            if (self.board[square-7] and self.board[square-7] > 14) or square-7 == self.en_passant_sqr:
                m.append(square - 7)

            if (self.board[square-9] and self.board[square-9] > 14) or square-9 == self.en_passant_sqr:
                m.append(square - 9)

            if not self.board[square-8]:
                m.append(square-8)

            return m
        else:
            if 7 < square < 16 and not self.board[square+8] and not self.board[square+16]:

                m.append(square+16)

            if (self.board[square+7] and self.board[square+7] < 14) or square+7 == self.en_passant_sqr:
                m.append(square + 7)

            if (self.board[square+9] and self.board[square+9] < 14) or square+9 == self.en_passant_sqr:
                m.append(square + 9)

            if not self.board[square+8]:
                m.append(square+8)

            return m

    def knight_move(self, square: int):
        # this is so bad holy hell
        m = []
        x, y = sqr_to_xy(square)

        top = y
        down = 8-y
        left = x
        right = 8-x-1

        if right >= 2:
            m.append(square+2-8)
            m.append(square+2+8)

        if left >= 2:
            m.append(square-2+8)
            m.append(square-2-8)

        if top >= 2:
            if right > 0:
                m.append(square-16+1)
            if left > 0:
                m.append(square-16-1)

        if down >= 2:
            if right > 0:
                m.append(square+16+1)
            if left > 0:
                m.append(square+16-1)
        mf = []
        for move in m:
            if move > 63 or move < 0:
                continue
            elif self.board[move]:
                if not self.right_color(self.board[move]):
                    mf.append(move)
            else:
                mf.append(move)

        return mf

    def bishop_move(self, square: int):
        m = []
        x, y = sqr_to_xy(square)

        top = y
        down = 8-y
        left = x
        right = 8-x-1

        for i in range(min(right, top)):
            if self.board[(square-((i+1)*7))]:
                if not self.right_color(self.board[(square-((i+1)*7))]):
                    m.append((square-((i+1)*7)))
                break
            m.append((square-((i+1)*7)))

        for i in range(min(left, top)):
            if self.board[(square-((i+1)*9))]:
                if not self.right_color(self.board[(square-((i+1)*9))]):
                    m.append((square-((i+1)*9)))
                break
            m.append((square-((i+1)*9)))

        for i in range(min(left, down-1)):
            if self.board[(square+((i+1)*7))]:
                if not self.right_color(self.board[(square+((i+1)*7))]):
                    m.append((square+((i+1)*7)))
                break
            m.append((square+((i+1)*7)))

        for i in range(min(right, down-1)):
            if self.board[(square+((i+1)*9))]:
                if not self.right_color(self.board[(square+((i+1)*9))]):
                    m.append((square+((i+1)*9)))
                break
            m.append((square+((i+1)*9)))
        return m

    def rook_move(self, square: int):
        m = []
        x, y = sqr_to_xy(square)
        top = y
        down = 8-y
        left = x
        right = 8-x-1
        for i in range(top):
            if self.board[square-((i+1)*8)]:
                if not self.right_color(self.board[square-((i+1)*8)]):
                    m.append(square-((i+1)*8))
                break
            m.append(square-((i+1)*8))
        for i in range(down-1):
            if self.board[square+((i+1)*8)]:
                if not self.right_color(self.board[square+((i+1)*8)]):
                    m.append(square+((i+1)*8))
                break
            m.append(square+((i+1)*8))
        for i in range(right):
            if self.board[square+((i+1)*1)]:
                if not self.right_color(self.board[square+((i+1)*1)]):
                    m.append(square+((i+1)*1))
                break
            m.append(square+((i+1)*1))
        for i in range(left):
            if self.board[square-((i+1)*1)]:
                if not self.right_color(self.board[square-((i+1)*1)]):
                    m.append(square-((i+1)*1))
                break
            m.append(square-((i+1)*1))

        return m

    def queen_move(self, square: int):
        return self.rook_move(square) + self.bishop_move(square)

    def move_piece(self, clicked: int):
        # If rooks moves disable castle for that side:
        if self.board[self.clicked_square] == 13 or self.board[self.clicked_square] == 21:
            if self.clicked_square % 8 == 0:
                if self.board[self.clicked_square] == 13:
                    self.wr_c = False
                else:
                    self.br_c = False

            elif self.clicked_square % 8 == 7:
                if self.board[self.clicked_square] == 13:
                    self.wl_c = False
                else:
                    self.bl_c = False

        # Special cases for KING
        if self.board[self.clicked_square] == 9 or self.board[self.clicked_square] == 17:
            # Castles:
            if (clicked-self.clicked_square) == -2:
                self.board[clicked + 1] = self.board[clicked-2]
                self.board[clicked - 2] = 0

            elif (clicked-self.clicked_square) == 2:
                self.board[clicked - 1] = self.board[clicked+1]
                self.board[clicked + 1] = 0

            # Disable Castles
            if self.board[self.clicked_square] == 9:
                self.wl_c = False
                self.wr_c = False

            else:
                self.bl_c = False
                self.br_c = False

        # Special cases for PAWN
        if self.board[self.clicked_square] == 10 or self.board[self.clicked_square] == 18:
            dist = clicked-self.clicked_square
            match dist:
                # En passant:
                # if en passant, take the pawn
                case 9 | 7:
                    if self.en_passant_sqr:
                        self.board[clicked-8] = 0
                case -9 | -7:
                    if self.en_passant_sqr:
                        self.board[clicked+8] = 0

                # Set en_passant square for double pawn move
                case 16:
                    self.en_passant_sqr = clicked-8
                    self.en_passant_color = True
                case -16:
                    self.en_passant_sqr = clicked+8
                    self.en_passant_color = False

        # Disable en passant square if
        if self.en_passant_sqr and self.en_passant_color == self.white_turn:
            self.en_passant_sqr = None
            self.en_passant_color = None

        # Moving the piece
        self.board[clicked] = self.board[self.clicked_square]
        self.board[self.clicked_square] = 0

    def right_color(self, piece):
        # One case in the world where xor is actually useful, I think...
        # if piece color is white and white's turn, returns true same for black
        return not ((piece < 15) ^ (self.white_turn))

    def is_king_checked(self, white: bool, king_pos=None):
        if not king_pos:
            king_pos = (self.board.index(9 if white else 17))
            # king_pos = (self.white_king if white else self.black_king)
        m = self.bishop_move(king_pos)
        for move in m:
            color, piece = num_to_piece(self.board[move])
            if (piece == 6 or piece == 4) and color != white:
                return True
        m = self.rook_move(king_pos)
        for move in m:
            color, piece = num_to_piece(self.board[move])
            if (piece == 6 or piece == 5) and color != white:
                return True

        m = self.knight_move(king_pos)
        for move in m:
            color, piece = num_to_piece(self.board[move])
            if piece == 3 and color != white:
                return True

        if white:
            if self.board[king_pos-7] == 18 or self.board[king_pos-9] == 18:
                return True
        else:
            if self.board[king_pos+7] == 10 or self.board[king_pos+9] == 10:
                return True

        return False

    def calc_move_squares(self, square: int):
        white, piece = num_to_piece(self.board[square])

        match piece:
            case 1:
                return self.king_move(square, white)
            case 2:
                return self.pawn_move(square, white)
            case 3:
                return self.knight_move(square)
            case 4:
                return self.bishop_move(square)
            case 5:
                return self.rook_move(square)
            case 6:
                return self.queen_move(square)

    def check_sudo_legal(self, moves: list):

        old_enp = self.en_passant_sqr
        old_enp_c = self.en_passant_color

        # Available castles
        old_wrc = self.wr_c
        old_wlc = self.wl_c
        old_brc = self.br_c
        old_blc = self.bl_c

        possible = {}
        for piece in moves:
            possible[piece] = []
            for move in moves[piece]:
                self.clicked_square = piece
                past = self.board.copy()
                self.move_piece(move)
                if not self.is_king_checked(self.white_turn):
                    possible[piece].append(move)

                self.board = past

        self.clicked_square = None
        self.en_passant_sqr = old_enp
        self.en_passant_color = old_enp_c

        # Available castles
        self.wr_c = old_wrc
        self.wl_c = old_wlc
        self.br_c = old_brc
        self.bl_c = old_blc

        return possible

    def all_possible_moves(self):
        possible = {}
        for square in range(64):
            if not self.board[square]:
                continue

            if self.board[square] == 9:
                self.white_king = square
            if self.board[square] == 17:
                self.black_king = square

            w, piece = num_to_piece(self.board[square])
            if self.white_turn == w:
                possible[square] = self.calc_move_squares(square)
        possible = self.check_sudo_legal(possible)
        for p in possible:
            if possible[p]:
                return possible
        return None
        # return (possible)

    def perft_driver(self, depth: int):
        totalmoves = 0
        n_moves = self.all_possible_moves()
        if depth == 1:
            t = 0
            for key, val in n_moves.items():
                t += len(val)
            return t
        for piece in n_moves:
            for move in n_moves[piece]:
                self.clicked_square = piece
                past = self.board.copy()
                self.move_piece(move)
                self.white_turn = False if self.white_turn else True
                c = self.perft_driver(depth-1)
                self.white_turn = False if self.white_turn else True
                totalmoves += c
                self.board = past

        """
        if depth == 3:
            pprint.pprint(n_moves)

        if depth == 2:
            print(f" {totalmoves}")
        """
        return totalmoves

    def perft(self, depth):
        s = ["0", "20", "400", "8.902", "197.281", "4.865.609"]
        st = time.time()
        res = self.perft_driver(depth)
        et = time.time()
        print(
            f"depth = {depth}, should = {s[depth]}, test = {res}, runtime = {et-st}")
        self.possible_moves = self.all_possible_moves()

    def debug(self):
        self.perft(5)

    def run(self):
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    # Resize the window
                    self.window_resize(event.dict["size"])

                if event.type == pygame.KEYDOWN:
                    # For debug
                    self.debug()
                    # pprint.pprint(self.all_possible_moves())

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = clicked_to(event.pos)

                    if self.board[clicked] and self.right_color(self.board[clicked]):
                        self.clicked_square = clicked

                    else:
                        if self.clicked_square and self.possible_moves[self.clicked_square] and (clicked in self.possible_moves[self.clicked_square]):
                            self.move_piece(clicked)
                            self.white_turn = False if self.white_turn else True
                            self.possible_moves = self.all_possible_moves()
                            if not self.possible_moves:
                                if self.is_king_checked(self.white_turn):
                                    print("check mate")
                                else:
                                    print("stale mate")

                        self.clicked_square = None

                if event.type == pygame.MOUSEBUTTONUP:
                    pass

            # rendering the pieces
            piece_sprites = pygame.sprite.Group()
            for i in range(64):
                if self.board[i]:
                    piece_sprites.add(self.render_piece(self.board[i], i))

            self.create_graphical_board()
            self.screen.blit(self.render_move_circle(), (0, 0))
            piece_sprites.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


def num_to_piece(num: int):
    # Returns the color and piece value from int representation.
    white = True if num < 15 else False
    piece = num & ((1 << 3) - 1)
    return white, piece


def sqr_to_cart(square: int):
    return ((square % 8)*GRID, (square//8)*GRID)


def sqr_to_xy(square: int):
    # Returns x,y coordinates of a square.
    return ((square % 8), (square//8))


def sqr_to_not(square: int):
    alf = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return (alf[square % 8] + str(8-(square//8)))


def clicked_to(coord: tuple):
    # Return which square is clicked based on x,y coordinates.
    return ((coord[0]//GRID) + (coord[1]//GRID)*8)


if __name__ == "__main__":
    game = Game()
    game.run()
