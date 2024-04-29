import pygame
import random
import time
import pickle

# Initialization of Pygame
pygame.init()

# Definition of the board dimensions
width = 400
height = 300
square_size = 100

# Definition of colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)

# Creation of the game window
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Três em Linha")


# Function to draw the board
def draw_board(board):
    window.fill(white)

    # Calculate the position of the board centered in the window
    board_x = (window.get_width() - width) // 2
    board_y = (window.get_height() - height) // 2

    for row in range(3):
        for column in range(4):
            square_x = board_x + column * square_size
            square_y = board_y + row * square_size

            pygame.draw.rect(
                window,
                black,
                (
                    square_x,
                    square_y,
                    square_size,
                    square_size,
                ),
                2,
            )

            if board[row][column] == 1:
                pygame.draw.circle(
                    window,
                    green,
                    (
                        int(square_x + square_size / 2),
                        int(square_y + square_size / 2),
                    ),
                    40,
                    0,
                )
            elif board[row][column] == 2:
                pygame.draw.circle(
                    window,
                    yellow,
                    (
                        int(square_x + square_size / 2),
                        int(square_y + square_size / 2),
                    ),
                    40,
                    0,
                )
            elif board[row][column] == 3:
                pygame.draw.circle(
                    window,
                    red,
                    (
                        int(square_x + square_size / 2),
                        int(square_y + square_size / 2),
                    ),
                    40,
                    0,
                )

    pygame.display.update()


# Function to check if a player has won
def check_victory(board, player):
    for row in range(3):
        if (
            board[row][0] == player
            and board[row][1] == player
            and board[row][2] == player
        ):
            return True
    for column in range(4):
        if (
            board[0][column] == player
            and board[1][column] == player
            and board[2][column] == player
        ):
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


# Function to make a move for the human player
def make_move(board, row, column, current_player):
    if board[row][column] == 0:
        board[row][column] = 1  # Change to green color
    elif board[row][column] == 1:
        board[row][column] = 2  # Change to yellow color
    elif board[row][column] == 2:
        board[row][column] = 3  # Change to red color
    draw_board(board)

    if check_victory(board, current_player):
        game_over(current_player)

    return board


# Function to handle the game over state
def game_over(winner):
    font = pygame.font.Font(None, 100)
    if winner == 1:
        text = font.render("Green Wins!", True, green)
    elif winner == 2:
        text = font.render("Yellow Wins!", True, yellow)
    elif winner == 3:
        text = font.render("Red Wins!", True, red)
    else:
        text = font.render("It's a Tie!", True, black)

    text_rect = text.get_rect(
        center=(
            window.get_width() // 2,
            window.get_height() // 2,
        )
    )
    window.blit(text, text_rect)
    pygame.display.update()
    time.sleep(2)
    reset_game()


# Function to reset the game
def reset_game():
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    draw_board(board)


# Main game loop
def game_loop():
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    current_player = 1

    draw_board(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate the position of the board centered in the window
                board_x = (window.get_width() - width) // 2
                board_y = (window.get_height() - height) // 2

                # Calculate the clicked row and column
                row = (mouse_y - board_y) // square_size
                column = (mouse_x - board_x) // square_size

                if 0 <= row <= 2 and 0 <= column <= 3:
                    board = make_move(board, row, column, current_player)
                    current_player = 2 if current_player == 1 else 1


# Start the game loop
game_loop()
