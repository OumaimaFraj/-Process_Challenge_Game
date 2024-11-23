import random
import time

# Définition des couleurs possibles
possibleColors = ["🔵", "🟢", "🟡", "🔴", "🟣", "🟠"]

# Initialisation de la grille de jeu
rows = 5
cols = 6
gameBoard = [["" for _ in range(cols)] for _ in range(rows)]

# Nombre de cases colorées initialement
initial_colored_squares = 8

# Fonction pour colorer aléatoirement une case


def colorRandomSquare():
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)
    color = random.choice(possibleColors)
    gameBoard[row][col] = color


# Colorer les cases initiales
for _ in range(initial_colored_squares):
    colorRandomSquare()

# Fonction pour vérifier si un mouvement est valide


def check_valid_move(color, x, y):
    # Vérifier si la couleur est déjà utilisée dans la même ligne ou colonne
    for i in range(rows):
        if gameBoard[i][y] == color and i != x:
            return False
    for j in range(cols):
        if gameBoard[x][j] == color and j != y:
            return False

    # Vérifier si les cases adjacentes ont la même couleur
    if x > 0 and gameBoard[x - 1][y] == color:
        return False
    if x < rows - 1 and gameBoard[x + 1][y] == color:
        return False
    if y > 0 and gameBoard[x][y - 1] == color:
        return False
    if y < cols - 1 and gameBoard[x][y + 1] == color:
        return False

    return True

# Approche 1: Remplissage stratégique


def strategic_fill():
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == '':
                # Trouver les couleurs déjà utilisées dans les cases adjacentes
                adjacent_colors = set()
                for i in range(max(0, x - 1), min(x + 2, rows)):
                    for j in range(max(0, y - 1), min(y + 2, cols)):
                        if gameBoard[i][j] in possibleColors:
                            adjacent_colors.add(gameBoard[i][j])

                # Choisir une couleur qui n'est pas déjà utilisée dans les cases adjacentes
                available_colors = [color for color in possibleColors if color not in adjacent_colors]
                if available_colors:
                    color = random.choice(available_colors)
                    gameBoard[x][y] = color

# Approche 2: Remplissage avec backtracking


def backtracking_fill():
    def is_board_filled():
        for row in gameBoard:
            for square in row:
                if square == '':
                    return False
        return True

    def backtrack(x, y):
        if is_board_filled():
            return True
        for color in possibleColors:
            if check_valid_move(color, x, y):
                gameBoard[x][y] = color
                next_x = x + 1 if y == cols - 1 else x
                next_y = y + 1 if y < cols - 1 else 0
                if backtrack(next_x, next_y):
                    return True
                gameBoard[x][y] = ''
        return False

    backtrack(0, 0)

# Approche 3: Remplissage dynamique


def dynamic_fill():
    def calculate_move_score(color, x, y):
        new_game_board = [row[:] for row in gameBoard]
        new_game_board[x][y] = color
        new_colors_used = len(set(color for row in new_game_board for color in row if color in possibleColors))
        elapsed_time = time.time() - start_time
        return elapsed_time + new_colors_used

    best_score = float('inf')
    best_move = None
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == '':
                for color in possibleColors:
                    if check_valid_move(color, x, y):
                        move_score = calculate_move_score(color, x, y)
                        if move_score < best_score:
                            best_score = move_score
                            best_move = (color, x, y)
    if best_move:
        color, x, y = best_move
        gameBoard[x][y] = color


def printGameBoard():
    print("\n  0  1  2  3  4  5")
    for x in range(rows):
        print(" +-----------------+")
        print(x, "|", end="")
        for y in range(cols):
            print(gameBoard[x][y] if gameBoard[x][y] else " ", "|", end="")
        print()
    print(" +-----------------+")


start_time = None


def main_game_loop():
    global start_time
    print("Bienvenue dans le jeu de coloriage de cases!")
    print("Grille de jeu initiale:")
    printGameBoard()

    # Exécuter l'approche 1 et calculer le score
    start_time = time.perf_counter()
    strategic_fill()
    score_approche_1 = time.perf_counter() - start_time
    print("Grille de jeu après remplissage stratégique:")
    printGameBoard()
    print("Score pour l'approche stratégique:", score_approche_1)

    # Réinitialiser la grille de jeu
    gameBoard = [["" for _ in range(cols)] for _ in range(rows)]
    for _ in range(initial_colored_squares):
        colorRandomSquare()

    # Exécuter l'approche 2 et calculer le score
    start_time = time.perf_counter()
    backtracking_fill()
    score_approche_2 = time.perf_counter() - start_time
    print("Grille de jeu après remplissage avec backtracking:")
    printGameBoard()
    print("Score pour l'approche avec backtracking:", score_approche_2)

    # Réinitialiser la grille de jeu pour l'approche 3
    gameBoard = [["" for _ in range(cols)] for _ in range(rows)]
    for _ in range(initial_colored_squares):
        colorRandomSquare()

    # Exécuter l'approche 3 et calculer le score
    start_time = time.perf_counter()
    dynamic_fill()
    score_approche_3 = time.perf_counter() - start_time
    print("Grille de jeu après remplissage dynamique:")
    printGameBoard()
    print("Score pour l'approche dynamique:", score_approche_3)


# Lancer la boucle principale du jeu
main_game_loop()
