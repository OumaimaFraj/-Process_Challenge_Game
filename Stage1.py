import random
import time

print("Welcome to  Stage 1 ")
print("---------------------------------------------")
# ============Initialization :The board’s size, the maximum number of colors, the number of initially colored squares =========
#I1
possibleColors = ["🔵", "🟢", "🟡", "🔴", "🟣", "🟠"]
#I2
gameBoard = [["" for _ in range(6)] for _ in range(5)]

rows = 5
cols = 6
#I3
initial_colored_squares = 8
#==================================================================================================
def colorRandomSquare():
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)
    color = random.choice(possibleColors)
    gameBoard[row][col] = color

# Color the initially specified number of squares
for _ in range(initial_colored_squares):
    colorRandomSquare()
#==================================================================================================
# =================== track start time and end time===============================
start_time = None
end_time = None

# ============================= track number of colors used by each player===============
player1_colors_used = 0
player2_colors_used = 0

#============================= Function to start the timer============================
def start_timer():
    global start_time
    start_time = time.time()

# ====================================Function to stop the timer======================
def stop_timer():
    global end_time
    end_time = time.time()

# ================================Function to calculate the elapsed time====================
def calculate_elapsed_time():
    if start_time is None or end_time is None:
        return 0
    return end_time - start_time
#===============================calculate score==================================================
def calculate_score(elapsed_time, colors_used):

    score = (elapsed_time, colors_used)
    return score
# ===============================Function to update the number of colors used by each player=============
def update_colors_used(player, colors):
    global player1_colors_used, player2_colors_used
    if player == 1:
        player1_colors_used = colors
    elif player == 2:
        player2_colors_used = colors

# ===============================Function to get the score for player 1==============================
def get_player1_score():
    elapsed_time = calculate_elapsed_time()
    return calculate_score(elapsed_time, player1_colors_used)

# ========================Function to get the score for player 2================================
def get_player2_score():
    elapsed_time = calculate_elapsed_time()
    return calculate_score(elapsed_time, player2_colors_used)
#========================================Print game board==================================

def printGameBoard():
    print("\n     0    1    2    3    4    5   6 ", end="")
    for x in range(rows):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(cols):
            if gameBoard[x][y] in possibleColors:
                print("", gameBoard[x][y], end=" |")
            else:
                print(" ", gameBoard[x][y], end="  |")
    print("\n   +----+----+----+----+----+----+----+")

#====================Fonction check Valid Move==================================

def check_valid_move(color, x, y):
    # Check if color is already used in the same row or column : CONDITION 1
    for i in range(rows):
        if gameBoard[i][y] == color and i != x:
            return False
    for j in range(cols):
        if gameBoard[x][j] == color and j != y:
            return False

    # Check if adjacent squares have the same color : CONDITION 2
    if x > 0 and gameBoard[x-1][y] == color:
        return False
    if x < rows - 1 and gameBoard[x+1][y] == color:
        return False
    if y > 0 and gameBoard[x][y-1] == color:
        return False
    if y < cols - 1 and gameBoard[x][y+1] == color:
        return False

    return True

#===========================================two functions of remplissage===============================
#=========================================Coloring a square==================================

def color_square(player, color, x, y):
    if gameBoard[x][y] != '':
        print("Square already colored!")
        return False
    #conditions
    if not check_valid_move(color, x, y):
        print("Invalid move!")
        return False
    gameBoard[x][y] = color
    return True

#==========================================Coloring a column OR a row==================================

def color_row_column(player, color, axis, index):
    if axis == 'row':
        for i in range(cols):
            if gameBoard[index][i] != '':
                print("Row already colored!")
                return False
            if not check_valid_move(color, index, i):
                print("Invalid move!")
                return False
            gameBoard[index][i] = color
    elif axis == 'column':
        for i in range(rows):
            if gameBoard[i][index] != '':
                print("Column already colored!")
                return False
            if not check_valid_move(color, i, index):
                print("Invalid move!")
                return False
            gameBoard[i][index] = color
    return True

#======================================= Approach 1: Strategic Thinking ==================================================
def strategic_thinking_player_input():
    # Analyze the game board to find the zone with the fewest colors already used
    min_colors = float('inf')
    target_zone = None
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == '':
                # Count the unique colors in the adjacent squares
                colors_count = len(set(gameBoard[i][j] for i in range(max(0, x-1), min(x+2, rows)) for j in range(max(0, y-1), min(y+2, cols)) if gameBoard[i][j] != ''))
                if colors_count < min_colors:
                    min_colors = colors_count
                    target_zone = (x, y)
    
    # Choose a color that is not already used in the target zone
    available_colors = [color for color in possibleColors if color not in set(gameBoard[i][j] for i in range(max(0, target_zone[0]-1), min(target_zone[0]+2, rows)) for j in range(max(0, target_zone[1]-1), min(target_zone[1]+2, cols)))]
    color = random.choice(available_colors)

    # Decide on the coloring strategy (individual square or entire row/column)
    if random.random() < 0.5:  # Randomly choose between coloring individual square or entire row/column
        # Color individual square
        return color, target_zone[0], target_zone[1]
    else:
        # Randomly choose between coloring entire row or column
        if random.random() < 0.5:  # Randomly choose between row or column
            axis = 'row'
            index =int(target_zone[0])
        else:
            axis = 'column'
            index = int(target_zone[1])
        return color, axis, index

# ===============================================Approach 2: Backtracking =====================================================
def is_game_board_filled():
    for row in gameBoard:
        for square in row:
            if square == '':
                return False
    return True
def backtracking_player_input():
    # Initialize variables to keep track of the best solution
    best_solution = None
    best_colors_used = float('inf')

    def backtrack(color_count, colors_used):
        nonlocal best_solution, best_colors_used

        # If the current number of colors used is greater than the best found so far, prune the search
        if colors_used >= best_colors_used:
            return

        if is_game_board_filled():
            # If all squares are filled, update the best solution if a better one is found
            if color_count < best_colors_used:
                best_solution = [row[:] for row in gameBoard]  # Copy the current game board
                best_colors_used = color_count
            return

        # Iterate over possible moves
        for color in possibleColors:
            for x in range(rows):
                for y in range(cols):
                    if gameBoard[x][y] == '' and check_valid_move(color, x, y):
                        # Apply the move
                        gameBoard[x][y] = color
                        # Recur to explore further
                        backtrack(color_count + 1, max(colors_used, len(set(color for row in gameBoard for color in row if color in possibleColors))))
                        # Undo the move
                        gameBoard[x][y] = ''  # Undo the move here, before exploring further

    # Start the backtracking search
    backtrack(0, 0)

    # Use the best found solution
    return best_solution

# ===============================================Approach 3: Dynamic programming =====================================================
def dynamic_programming_player_input():
    # Define a function to calculate the score of a move
    def calculate_move_score(color, x, y):
        # Calculate the number of colors used after the move
        new_game_board = [row[:] for row in gameBoard]
        new_game_board[x][y] = color
        new_colors_used = len(set(color for row in new_game_board for color in row if color in possibleColors))
        # Calculate the time elapsed after the move (assuming one unit of time per move)
        elapsed_time = calculate_elapsed_time()
        
        # Calculate the score (time + number of colors used)
        return elapsed_time + new_colors_used

    # Initialize variables to keep track of the best move and its score
    best_move = None
    best_score = float('inf')

    # Iterate over possible moves
    for color in possibleColors:
        for x in range(rows):
            for y in range(cols):
            
                if gameBoard[x][y] == '' and check_valid_move(color, x, y):
                    
                    # Calculate the score of the move
                    move_score = calculate_move_score(color, x, y)
                    
                    # Update the best move if the score of the current move is better
                    if move_score < best_score:
                        best_move = (color, x, y)
                        best_score = move_score

    return best_move

#============================================= Asking user for approaches====================================================
def select_approach(player):
    print(f"Select an approach for Player {player}:")
    print("1. Dynamic Programming")
    print("2. Backtracking")
    print("3. Strategic Thinking \n")
    while True:
        choice = input("Enter your choice (1/2/3): \n")
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")
#============================================= Player input============================================
def player_input(player, approach):
    if approach == 1:  # Dynamic Programming
        return dynamic_programming_player_input()
    elif approach == 2:  # Backtracking
        return backtracking_player_input()
    elif approach == 3:  # Strategic Thinking
        return strategic_thinking_player_input()
    else:
        print("Invalid approach!")
        return None
#=======================================================main game loop========================================================

def main_game_loop():
    # Initialize game board
    print("Initializing game board...")
    printGameBoard()

    # Start the timer
    start_timer()

    # Ask the user to select an approach for each player
    player1_approach = select_approach(1)
    player2_approach = select_approach(2)

    # Main game loop
    turn = 1
    while True:
        print("\nTurn", turn)
        print("Player 1's turn:")
        player1_move = player_input(1, player1_approach)
        if player1_move:
            if len(player1_move) == 3:
                color, x, y = player1_move
                success = color_square(1, color, int(x), int(y))
                if success:
                    print("Player 1 colored square", (x, y), "with color", color)
                    update_colors_used(1, len(set(color for row in gameBoard for color in row if color in possibleColors)))
                else:
                    print("Player 1's move was invalid.")
            else:
                color, axis, index = player1_move
                success = color_row_column(1, color, axis, index)
                if success:
                    print("Player 1 colored entire", axis, index, "with color", color)
                    update_colors_used(1, len(set(color for row in gameBoard for color in row if color in possibleColors)))
                else:
                    print("Player 1's move was invalid.")

        printGameBoard()

        if is_game_board_filled() or not any(check_valid_move(color, x, y) for color in possibleColors for x in range(rows) for y in range(cols)):
            print("Game Over! Board is filled or no valid moves can be made.")
            break
        
# player 2 turn
        print("\nPlayer 2's turn:")
        player2_move = player_input(2, player2_approach)
        if player2_move:
            if len(player2_move) == 3:
                color, x, y = player2_move
                # Ensure x and y are integers
                x = int(x)
                y = int(y)
                success = color_square(2, color, int(x), int(y))
                if success:
                    print("Player 2 colored square", (x, y), "with color", color)
                    update_colors_used(2, len(set(color for row in gameBoard for color in row if color in possibleColors)))
                else:
                    print("Player 2's move was invalid.")
            else:
                color, axis, index = player2_move
                success = color_row_column(2, color, axis, index)
                if success:
                    print("Player 2 colored entire", axis, index, "with color", color)
                    update_colors_used(2, len(set(color for row in gameBoard for color in row if color in possibleColors)))
                else:
                    print("Player 2's move was invalid.")

        printGameBoard()
        if is_game_board_filled() or not any(check_valid_move(color, x, y) for color in possibleColors for x in range(rows) for y in range(cols)):
            print("Game Over! Board is filled or no valid moves can be made.")
            break

        turn += 1

    # Stop the timer
    stop_timer()

    # Calculate scores for each player
    player1_score = get_player1_score()
    player2_score = get_player2_score()

    print("\nPlayer 1 Score:", player1_score)
    print("Player 2 Score:", player2_score)

# Call the main game loop function

main_game_loop()