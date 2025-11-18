import random


class Combination:
    def __init__(self, goat_1: tuple[int, int], goat_2: tuple[int, int], board_dimensions: tuple[int, int] = (3,5)):
        self.winner = None
        self.goat_1 = goat_1
        self.goat_2 = goat_2
        self.board_dimensions = board_dimensions

    def getWinner(self):
        if self.winner is not None:
            return self.winner
        else: return self.calculateWinner()

    def calculateWinner(self) -> str:


def doPuzzle():
    ITERATIONS = 1_000_000

    alice_wins = 0
    bob_wins = 0
    draws = 0

    for iteration in range(0, ITERATIONS):
        boxes = generateBoxes()
        winners = simulate(boxes)
        if winners[0] == winners[1]:
            draws += 1
        else:
            alice_wins += winners[0]
            bob_wins += winners[1]

    print(f"Alice wins: {alice_wins}")
    print(f"Bob wins: {bob_wins}")
    print(f"Draws: {draws}")

    increased_odds = (alice_wins / bob_wins) - 1

    print(f"Increased odds of Alice winning: {increased_odds:.2%}")


def simulate(boxes: list[list[str]]) -> tuple[int, int]:
    alice_won = 0
    bob_won = 0

    for position in range(0, 15, 1):
        winner: bool = False

        # Row-major: (0,0) -> (0,1) -> (0,2) ...
        alice_pos = (position // 5, position % 5)

        # Column-major: (1,0) -> (1,0) -> (2,0) -> (0, 1)
        bob_pos = (position % 3, position // 3)

        # Alice wins
        if boxes[alice_pos[0]][alice_pos[1]] == "GOAT":
            alice_won = 1
            winner = True

        # Maybe bob wins too
        if boxes[bob_pos[0]][bob_pos[1]] == "GOAT":
            bob_won = 1
            winner = True

        # If either won, we're done
        if winner:
            break

    return (alice_won, bob_won)


def generateBoxes() -> list[list[str]]:
    boxes: list[list[str]] = [[], [], []]
    for row in range(0, 3, 1):
        for col in range(0, 5, 1):
            boxes[row].append("NONE")

    # Add goat 1
    boxes[random.randint(0, 2)][random.randint(0, 4)] = "GOAT"

    # Add goat 2
    while True:
        position = (random.randint(0, 2), random.randint(0, 4))
        if boxes[position[0]][position[1]] == "GOAT":
            continue
        else:
            boxes[position[0]][position[1]] = "GOAT"
            break

    return boxes


def generateCombinations() -> list[list[list[str]]]:
    return


doPuzzle()
