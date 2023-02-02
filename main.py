import pygame
import pieces

# --- constants --- 

SCREEN_WIDTH = 904
SCREEN_HEIGHT = 904

BLACK = (186, 85, 72)
WHITE = (240, 216, 191)
RED   = (255,   0,   0)
GREY  = (128, 128, 128)
LIGHT_GREY  = (217, 167, 108)
LIGHT_GREEN = (244, 232, 169)
YELLOW = (246, 246, 105)


FPS = 30


TILESIZE = 113 


# --- functions ---
def mouse_position(event_pos):
    eventx, eventy = event_pos 
    tile_x = eventx//TILESIZE
    tile_y = eventy//TILESIZE
    return tile_x, tile_y 


def create_empty_board():
    board = []
    for x in range(8):
        board.append([])
        for y in range(8):
            board[x].append(None)
    return board


def draw_chessboard():
    board_surf = pygame.Surface((TILESIZE*8, TILESIZE*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, (BLACK if dark else WHITE), rect)
            dark = not dark
        dark = not dark
    return board_surf


def print_chessboard():
    for y in range(8):
        for x in range(8):
            if chess_board[x][y]:
                print(f"[{chess_board[x][y].name}] ", end="")
            else:
                print("[Empty] ", end="")
        print()


def draw_moves(moves: list[tuple[int,int]]):
    possible_surf = pygame.Surface((TILESIZE*8, TILESIZE*8)) 
    possible_surf.set_colorkey((0,0,0))
    for move in moves:
        pygame.draw.circle(possible_surf, LIGHT_GREY,((move[0])*113 + 56,(move[1])*113+1 + 56),22)
        #pygame.draw.rect(possible_surf, LIGHT_GREY,(move[0]*TILESIZE, move[1]*TILESIZE, TILESIZE, TILESIZE))
    return possible_surf


def move_king(chosen_piece, mouse_x, mouse_y,chess_board):
    subtitute_board = chess_board
    global turn, possible_moves 
    #clear current position
    chess_board[chosen_piece.tile_position[0]][chosen_piece.tile_position[1]] = None
    #move the piece to the cliked tile
    old_coordiantes = chosen_piece.img_position
    if chosen_piece.not_moved:
        if mouse_x == 0:
            mouse_x += 2

            rook = chess_board[0][mouse_y] 
            chess_board[0][mouse_y] = None
            rook.move((3,mouse_y))
            chess_board[3][mouse_y] = rook

        elif mouse_x == 7:
            mouse_x -= 1 

            rook = chess_board[7][mouse_y] 
            chess_board[7][mouse_y] = None
            rook.move((5,mouse_y))
            chess_board[5][mouse_y] = rook


    chosen_piece.move((mouse_x, mouse_y))
    #move to piece to the board
    chess_board[mouse_x][mouse_y] = chosen_piece 
    
    if check_state:
        if is_check(update_controlled_squares(chess_board)):
            chess_board[mouse_x][mouse_y] = None 
            chess_board[chosen_piece.old_tile_position[0]][chosen_piece.old_tile_position[1]] = chosen_piece
            chosen_piece.return_old()
            return 
 
    if chosen_piece.not_moved:
        chosen_piece.not_moved = False
    chosen_piece = None
    possible_moves = []
    turn = next(turn)



def move_piece(chosen_piece, mouse_x, mouse_y, chess_board):
    subtitute_board = chess_board
    global turn, possible_moves 
    #clear current position
    chess_board[chosen_piece.tile_position[0]][chosen_piece.tile_position[1]] = None
    #move the piece to the cliked tile
    old_coordiantes = chosen_piece.img_position
    chosen_piece.move((mouse_x, mouse_y))
    #move to piece to the board
    chess_board[mouse_x][mouse_y] = chosen_piece 
    
    if check_state:
        if is_check(update_controlled_squares(chess_board)):
            chess_board[mouse_x][mouse_y] = None 
            chess_board[chosen_piece.old_tile_position[0]][chosen_piece.old_tile_position[1]] = chosen_piece
            chosen_piece.return_old()
            return 
 
    if chosen_piece.not_moved:
        chosen_piece.not_moved = False
    chosen_piece = None
    possible_moves = []
    turn = next(turn)


def move_pawn(chosen_piece, mouse_x, mouse_y,chess_board):
    subtitute_board = chess_board
    old_coordiantes = chosen_piece.img_position
    global turn, possible_moves, dragging, en_passant_target
    #clear current position
    chess_board[chosen_piece.tile_position[0]][chosen_piece.tile_position[1]] = None
    #move the piece to the cliked tile
    if abs(chosen_piece.tile_position[1] - mouse_y) == 2:
        if chess_board[mouse_x-1][mouse_y] and chess_board[mouse_x-1][mouse_y].color != chosen_piece.color and chess_board[mouse_x-1][mouse_y].name == "pawn": 
            chess_board[mouse_x-1][mouse_y].en_passant = 1
            en_passant_target = chess_board[mouse_x-1][mouse_y]
        if chess_board[mouse_x+1][mouse_y] and chess_board[mouse_x+1][mouse_y].color != chosen_piece.color and chess_board[mouse_x+1][mouse_y].name == "pawn": 
            chess_board[mouse_x+1][mouse_y].en_passant = -1 
            en_passant_target = chess_board[mouse_x+1][mouse_y]
    if  abs(chosen_piece.tile_position[0]-mouse_x) == 1 and abs(chosen_piece.tile_position[1]-mouse_y) == 1:
        chess_board[mouse_x][mouse_y + 1 if chosen_piece.color == "white" else mouse_y - 1] = None

    chosen_piece.move((mouse_x, mouse_y))

    #move to piece to the board
    if chosen_piece.color == "white" and mouse_y == 0 or chosen_piece.color == "black" and mouse_y == 7:
        dragging = False
        

        chosen_piece = pieces.Queen( tile_position = chosen_piece.tile_position, color=chosen_piece.color, img= (pieces.W_QUEEN_IMG if chosen_piece.color == "white" else pieces.QUEEN_IMG),  img_position=(chosen_piece.tile_position[0]*113+1, chosen_piece.tile_position[1]*113 +1))
        

    chess_board[mouse_x][mouse_y] = chosen_piece 
    

    if check_state:
        if is_check(update_controlled_squares(chess_board)):
            chess_board[mouse_x][mouse_y] = None 
            chess_board[chosen_piece.old_tile_position[0]][chosen_piece.old_tile_position[1]] = chosen_piece
            chosen_piece.return_old()
            return 

    blit_chessboard(chess_board)
    chosen_piece = None
    possible_moves = []
    turn = next(turn)


def next(turn):
    global en_passant_target
    if en_passant_target and en_passant_target.color == turn:
        en_passant_target.en_passant = 0 
        en_passant_target = None

    return  "white" if turn == "black" else "black"


def blit_chessboard(chess_board):
    for row in chess_board:
        for piece in row:
            if piece:
                if piece == chosen_piece: continue #this will be drawn down bellow
                screen.blit(piece.img,(piece.img_position))
   
    if chosen_piece and dragging:
        screen.blit(chosen_piece.img, tuple(- 55 + elem for elem in pygame.mouse.get_pos()))
    elif chosen_piece:
        screen.blit(chosen_piece.img, chosen_piece.img_position)


def update_controlled_squares(chess_board):
    cs_w = []
    cs_b = []
    for row in chess_board:
        for piece in row:
            if piece:
                if piece.name == "pawn":
                    if piece.color == "white":
                        if piece.tile_position[0]-1 > -1 and piece.tile_position[1]-1 > -1:
                            cs_w.append((piece.tile_position[0]-1, piece.tile_position[1]-1))
                        if piece.tile_position[0]+1 < 8 and piece.tile_position[1]-1 > -1:
                            cs_w.append((piece.tile_position[0]+1, piece.tile_position[1]-1))
                    else:
                        if piece.tile_position[0]-1 > -1 and piece.tile_position[1]+1 < 8:
                            cs_b.append((piece.tile_position[0]-1, piece.tile_position[1]+1))
                        if piece.tile_position[0]+1 < 8 and piece.tile_position[1]+1 < 8:
                            cs_b.append((piece.tile_position[0]+1, piece.tile_position[1]+1))
                else:
                    if piece.color == "white":
                        cs_w = cs_w + piece.possible_moves(check_state, chess_board, controlled_squares)
                    else:
                        cs_b = cs_b + piece.possible_moves(check_state, chess_board, controlled_squares)
    return [cs_w, cs_b]

  
def is_check(board):
    global check_state
    for squares in board[0]:
        if chess_board[squares[0]][squares[1]] and chess_board[squares[0]][squares[1]].name == "king" and chess_board[squares[0]][squares[1]].color == "black":
            check_state = True
            return True
    for squares in board[1]:
        if chess_board[squares[0]][squares[1]] and chess_board[squares[0]][squares[1]].name == "king" and chess_board[squares[0]][squares[1]].color == "white":
            check_state = True
            return  True
    check_state = False 
    return False 
# - init -

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hopefully a Chess Game")


clock = pygame.time.Clock()

running = True

dragging = False

chosen_piece = None

check_state = False

possible_moves = []

controlled_squares = []

en_passant_target = None 

current_tile = (200, 200)
move_square = pygame.Rect(TILESIZE, TILESIZE, TILESIZE, TILESIZE)
past_tile = (200, 200)

turn = "white" 



# -- CREATE CHESSBOARD --
chess_board = pieces.create_pieces()

"""
chess_board = pieces.debug_board()
chess_board = pieces.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
"""



# - mainloop -
while running:  
   
    # - events - 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:            
                dragging = True
                mouse_x, mouse_y = mouse_position(event.pos)
                if chosen_piece and chosen_piece.color == turn:
                    if (mouse_x, mouse_y) in possible_moves:
                        
                        current_tile = (mouse_x,mouse_y)
                        past_tile = chosen_piece.tile_position

                        if chosen_piece.name == "pawn": move_pawn(chosen_piece, mouse_x, mouse_y, chess_board)
                        elif chosen_piece.name == "king": move_king(chosen_piece, mouse_x, mouse_y, chess_board)
                        else: move_piece(chosen_piece, mouse_x, mouse_y, chess_board)

                    elif chess_board[mouse_x][mouse_y] and chess_board[mouse_x][mouse_y].color == turn:

                        chosen_piece = chess_board[mouse_x][mouse_y]
                        possible_moves = chosen_piece.possible_moves(check_state, chess_board, controlled_squares[1 if turn == "white" else 0])
                    else:
                        chosen_piece = None
                        possible_moves = []
                else:
                    if chosen_piece != chess_board[mouse_x][mouse_y]:
                        
                        chosen_piece = chess_board[mouse_x][mouse_y]
                        if chosen_piece and chosen_piece.color == turn:
                            dragging = True
                            possible_moves = chosen_piece.possible_moves(check_state, chess_board, controlled_squares[1 if turn == "white" else 0])
   
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if chosen_piece and chosen_piece.color == turn:
                mouse_x, mouse_y = mouse_position(event.pos)
                if (mouse_x, mouse_y) in possible_moves:
                    
                   move_piece(chosen_piece, mouse_x, mouse_y,chess_board)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            chosen_piece = None
            possible_moves = []
    

    # empty
    board = draw_chessboard()
    
    controlled_squares = update_controlled_squares(chess_board)
    #possible_surface = draw_moves(possible_moves)
    #possible_surface = draw_moves(controlled_squares[0])
    #possible_surface = draw_moves(controlled_squares[1])
    check_state = is_check(controlled_squares)
   
    screen.fill(GREY)
    screen.blit(board, (0,0))
    #screen.blit(possible_surface,(0,0))
    current_square = pygame.Rect(current_tile[0]*TILESIZE, current_tile[1]*TILESIZE, TILESIZE, TILESIZE)
    past_square = pygame.Rect(past_tile[0]*TILESIZE, past_tile[1]*TILESIZE, TILESIZE, TILESIZE)
   
    pygame.draw.rect(screen, LIGHT_GREEN if((current_tile[0]%2 == 0 and current_tile[1]%2 == 0) or (current_tile[0]%2 != 0 and current_tile[1]%2 != 0)) else LIGHT_GREY , current_square)
    pygame.draw.rect(screen, LIGHT_GREEN if((past_tile[0]%2 == 0 and past_tile[1]%2 == 0) or (past_tile[0]%2 != 0 and past_tile[1]%2 != 0))else LIGHT_GREY , past_square)
    blit_chessboard(chess_board) 

    pygame.display.flip()
    clock.tick(FPS)
    
    #print(check_state)
# - end -

pygame.quit()
