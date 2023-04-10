
from pieces import king, queen, pawn, knight, rook, bishop, black, white, p_dict


class Board:
    def __init__(self):
        self.board = [0]*64

    def create(self):

        self.board[0] = black | rook
        self.board[1] = black | knight
        self.board[2] = black | bishop
        self.board[3] = black | queen
        self.board[4] = black | king
        self.board[5] = black | bishop
        self.board[6] = black | knight
        self.board[7] = black | rook

        self.board[8] = black | pawn
        self.board[9] = black | pawn
        self.board[10] = black | pawn
        self.board[11] = black | pawn
        self.board[12] = black | pawn
        self.board[13] = black | pawn
        self.board[14] = black | pawn
        self.board[15] = black | pawn

        self.board[48] = white | pawn
        self.board[49] = white | pawn
        self.board[50] = white | pawn
        self.board[51] = white | pawn
        self.board[52] = white | pawn
        self.board[53] = white | pawn
        self.board[54] = white | pawn
        self.board[55] = white | pawn

        self.board[56] = white | rook
        self.board[57] = white | knight
        self.board[58] = white | bishop
        self.board[59] = white | queen
        self.board[60] = white | king
        self.board[61] = white | bishop
        self.board[62] = white | knight
        self.board[63] = white | rook
        return self.board

    def _create(self):
        self.board[4] = black | king
        self.board[3] = black | queen
        self.board[10] = black | queen
        self.board[60] = white | king

        return self.board

    def ___create(self):
        return self.create_board_from_fen("r3r1k1/p1pqbpp1/1pn3P1/3p1b1p/3PnB1P/P2N1N1B/1PP1QP2/2KR3R")

    def create_board_from_fen(self, notation: str):
        c_square = 0
        for c in notation:
            if (c >= "0" and c <= "9"):
                c_square += int(c)
            elif c != "/":
                color = c.isupper()
                c = c.lower()
                self.board[c_square] = (white if color else black) | p_dict[c]
                c_square += 1
        return self.board
