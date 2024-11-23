import time
import random
import math

class Zombie:
    def __init__(self, name, treasure_value, combat_power):
        self.name = name
        self.treasure_value = treasure_value
        self.combat_power = combat_power

def maximize_profit_dynamic(zombies, time_limit):
    dp = [0] * (time_limit + 1)
    for t in range(1, time_limit + 1):
        for i in range(len(zombies)):
            if zombies[i].combat_power <= t:
                dp[t] = max(dp[t], dp[t - zombies[i].combat_power] + zombies[i].treasure_value)
    return dp[time_limit]

def maximize_profit_backtracking(zombies, time_limit, idx=0, remaining_time=0):
    if idx == len(zombies) or remaining_time <= 0:
        return 0
    profit_take = 0
    if zombies[idx].combat_power <= remaining_time:
        profit_take = zombies[idx].treasure_value + maximize_profit_backtracking(zombies, time_limit, idx+1, remaining_time - zombies[idx].combat_power)
    profit_skip = maximize_profit_backtracking(zombies, time_limit, idx+1, remaining_time)
    return max(profit_take, profit_skip)

def choose_zombies():
    combat_power1 = random.randint(3, 12)
    combat_power2 = random.randint(3, 12)
    combat_power3 = random.randint(3, 12)
    combat_power4 = random.randint(3, 12)
    combat_power5 = random.randint(3, 12)
    zombies = [
        Zombie("Zombie 1", combat_power1 + math.trunc(combat_power1 / 2), combat_power1),
        Zombie("Zombie 2", combat_power2 + math.trunc(combat_power2 / 2), combat_power2),
        Zombie("Zombie 3", combat_power3 + math.trunc(combat_power3 / 2), combat_power3),
        Zombie("Zombie 4", combat_power4 + math.trunc(combat_power4 / 2), combat_power4),
        Zombie("Zombie 5", combat_power5 + math.trunc(combat_power5 / 2), combat_power5)
    ]
    return zombies

def print_zombies(zombies):
    print("Liste des zombies:")
    for i, zombie in enumerate(zombies):
        print(f"{i+1}. {zombie.name} - Valeur du trésor: {zombie.treasure_value}, Puissance de combat: {zombie.combat_power}")

def player_turn(player_num, total_points, zombies):
    start_time = time.time()  # Temps de début du tour du joueur
    time_limit = 6  # Limite de temps en secondes

    print(f"Joueur {player_num}, c'est à votre tour.")
    approach = input(f"Choisissez votre approche de résolution de problèmes ('dynamic programming', 'backtracking') : ")

    if approach not in ["dynamic programming", "backtracking"]:
        print("Approche de résolution de problèmes invalide. Choisissez parmi 'dynamic programming', 'backtracking'.")
        return total_points

    turn_count = 0  # Compteur de tours
    while True:  # Exécutez une boucle infinie pour vérifier le temps écoulé à chaque tour
        start_turn_time = time.time()  # Temps de début du tour actuel
        elapsed_time = 0  # Initialisation du temps écoulé pour ce tour
        while elapsed_time < time_limit:
            if approach == "dynamic programming":
                total_points = maximize_profit_dynamic(zombies, total_points)
            elif approach == "backtracking":
                total_points = maximize_profit_backtracking(zombies, total_points, 0, total_points)

            # Calculer le temps écoulé pour ce tour
            elapsed_time = time.time() - start_turn_time

            turn_count += 1  # Incrémenter le compteur de tours

            if elapsed_time > time_limit:
                print(f"Le temps est écoulé pour le Joueur {player_num}.")
                break  # Sortir de la boucle de tour si le temps est écoulé

        if elapsed_time > time_limit:
            break  # Sortir de la boucle infinie si le temps est écoulé

    end_time = time.time()  # Temps de fin du tour du joueur
    print(f"Temps pour le joueur {player_num} avec l'approche '{approach}': {end_time - start_time} secondes")

    return total_points





if __name__ == "__main__":
    total_points_player1 = int(input("Entrez le total de points du Joueur 1 : "))
    total_points_player2 = int(input("Entrez le total de points du Joueur 2 : "))

    zombies = choose_zombies()  # Générer la liste de zombies une seule fois

    print("Joueur 1, c'est à vous !")
    total_points_player1 = player_turn(1, total_points_player1, zombies[:])  # Passer une copie de la liste de zombies

    print("Joueur 2, c'est à vous !")
    total_points_player2 = player_turn(2, total_points_player2, zombies[:])  # Passer une copie de la liste de zombies

    print("Score final du Joueur 1:", total_points_player1)
    print("Score final du Joueur 2:", total_points_player2)
