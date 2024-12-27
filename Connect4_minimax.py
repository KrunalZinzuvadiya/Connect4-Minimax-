import numpy as np
import pygame
import math
import random
import sys

pygame.init()

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

SQUARESIZE = 100
HEIGHT = (COLUMN_COUNT)* SQUARESIZE
WIDTH = (ROW_COUNT + 1)*SQUARESIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARESIZE / 2 - 5)

#create a screen
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect4 Game")

#load image
BOARD_IMG = pygame.image.load("img/Board_Image.png")
RED_PIECE = pygame.image.load("img/Red2.png")
YELLOW_PIECE = pygame.image.load("img/Yellow2.png")

#RESET SCALE
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (WIDTH, HEIGHT - SQUARESIZE))
RED_PIECE = pygame.transform.scale(RED_PIECE, (SQUARESIZE, SQUARESIZE))
YELLOW_PIECE = pygame.transform.scale(YELLOW_PIECE, (SQUARESIZE, SQUARESIZE))

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

board = create_board()

def drop_pieces(board, row, col, piece):
    board[row][col] = piece

def valid_location(board,col):
    return board[0][col] == EMPTY

def available_row(board, col):
    for r in range(ROW_COUNT-1, -1,-1):
        if board[r][col] == EMPTY:
            return r
        
def getEmptyPositions(self):
    #takes the current board, and returns possible positions for next chip
    ans = []
    for j in range(self.columns):
        i = self.rows - 1
        while i >= 0 and self.board[i][j] != 0:
            i -= 1
        if i >= 0:
            ans.append((i,j))
    return ans

font = pygame.font.SysFont("monospace", 75)

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            #Horizontal match
            if board[r][c]== piece and board[r][c+1]== piece and board[r][c+2]== piece and board[r][c+3]== piece:
                return True
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            #Vertical match
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            #One diagonal match
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
            
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            #another diagonal match
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    
    return False

def evalute_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 500
    elif window.count(piece)==3 and window.count(EMPTY)==1:
        score += 30
    elif window.count(piece)==2 and window.count(EMPTY)==2:
        score += 10
        
    if window.count(opp_piece)==3 and window.count(EMPTY)==1:
        score -= 25
        
    return score

def score_position(board, piece):
    score = 0

    #score center colum
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    #score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evalute_window(window, piece)

    #Vertical Score
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evalute_window(window, piece)
    
    #-45 Diagonal Score
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r+i, c+i])
            score += evalute_window(window, piece)
    
    #+45 Diagonal score
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            window = []
            for i in range(WINDOW_LENGTH):
                window.append(board[r-i, c+i])
            score += evalute_window(window, piece)
    
    return score

def terminal_node(board):
   return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board)) == 0

def get_valid_location(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if valid_location(board,col):
            valid_locations.append(col)
    return valid_locations
    
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_location(board)
    is_terminal = terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else: #Game is over and no valid move is available
                return (None, 0)
        else:
            return(None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = available_row(board, col)
            b_copy = board.copy()
            drop_pieces(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    
    else: #Minimizing Player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = available_row(board, col)
            b_copy = board.copy()
            drop_pieces(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
"""
def best_move(board, piece):
    valid_locations = get_valid_location(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = available_row(col)
        temp_board = board.copy()
        drop_pieces(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col
"""

def draw_winning_lines(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            #Horizontal match
            if board[r][c]== piece and board[r][c+1]== piece and board[r][c+2]== piece and board[r][c+3]== piece:
                start_pos = (c * SQUARESIZE + SQUARESIZE // 2, (r+1) * SQUARESIZE + SQUARESIZE // 2)
                end_pos = ((c+3) * SQUARESIZE + SQUARESIZE // 2, (r+1)* SQUARESIZE + SQUARESIZE // 2)
                pygame.draw.line(screen, BLUE, start_pos, end_pos, 4)
                return
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            #Vertical match
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                start_pos = (c * SQUARESIZE + SQUARESIZE // 2, (r+1) * SQUARESIZE + SQUARESIZE // 2)
                end_pos = ((c) * SQUARESIZE + SQUARESIZE // 2, (r+4)* SQUARESIZE + SQUARESIZE // 2)
                pygame.draw.line(screen, BLUE, start_pos, end_pos, 4)
                return
    
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            #One diagonal match
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                start_pos = (c * SQUARESIZE + SQUARESIZE // 2, (r+1) * SQUARESIZE + SQUARESIZE // 2)
                end_pos = ((c+3) * SQUARESIZE + SQUARESIZE // 2, (r+4)* SQUARESIZE + SQUARESIZE // 2)
                pygame.draw.line(screen, BLUE, start_pos, end_pos, 4)
                return
            
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            #another diagonal match
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                start_pos = (c * SQUARESIZE + SQUARESIZE // 2, (r+1) * SQUARESIZE + SQUARESIZE // 2)
                end_pos = ((c+3) * SQUARESIZE + SQUARESIZE // 2, (r-2)* SQUARESIZE + SQUARESIZE // 2)
                pygame.draw.line(screen, BLUE, start_pos, end_pos, 4)
                return
    
    #return False



def draw_board(board):
    screen.fill(WHITE)
    screen.blit(BOARD_IMG, (0, SQUARESIZE))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==PLAYER_PIECE:
                screen.blit(RED_PIECE, (c * SQUARESIZE, (r+1) * SQUARESIZE))
            elif board[r][c]==AI_PIECE:
                screen.blit(YELLOW_PIECE, (c * SQUARESIZE, (r+1) * SQUARESIZE))
    pygame.display.update()

draw_board(board)
running = True
game_over = False

turn = random.choice([AI, PLAYER])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION and not game_over:
            pygame.draw.rect(screen, WHITE, (0,0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                screen.blit(RED_PIECE, (posx - SQUARESIZE // 2, 0))
            else:
                screen.blit(YELLOW_PIECE, (posx - SQUARESIZE // 2, 0))
        
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pygame.draw.rect(screen, WHITE, (0,0, WIDTH, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = posx // SQUARESIZE

                if valid_location(board, col):
                    row = available_row(board, col)
                    drop_pieces(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        game_over = True
                        winner = PLAYER
                
                    turn = (turn + 1) % 2

                    draw_board(board)
    
    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if valid_location(board, col):
            row = available_row(board, col)
            drop_pieces(board, row, col, AI_PIECE)
            draw_board(board)
            pygame.display.update()
            pygame.time.wait(500)

            if winning_move(board, AI_PIECE):
                game_over = True
                winner = AI
            
            turn = (turn + 1) % 2

    
    if game_over:
        draw_board(board)
        if winner == PLAYER:
            # Render player red win message
            draw_winning_lines(board, PLAYER_PIECE)
            label = font.render(f"Human Player wins!", True, BLACK)
        elif winner == AI:
            # Render player yellow win message
            draw_winning_lines(board, AI_PIECE)
            label = font.render(f"AI Player wins!", True, BLACK)
        
        # Clear screen and draw label
        #screen.fill(WHITE)  # Fill screen with white
        screen.blit(label, (40, 10))  # Blit label at position (40, 10)

        # Update the display
        pygame.display.update()
        pygame.time.wait(5000)

        running = False

pygame.quit()