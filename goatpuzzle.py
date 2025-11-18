import pprint
import random


class Combination:
    def __init__(
        self,
        goat_1: tuple[int, int],
        goat_2: tuple[int, int],
        board_dimensions: tuple[int, int] = (3, 5),
    ):
        self.winner = None
        self.goat_1 = goat_1
        self.goat_2 = goat_2
        self.board_dimensions = board_dimensions

    def getWinner(self):
        if self.winner is not None:
            return self.winner
        else:
            return self.calculateWinner()

    def calculateWinner(self) -> str:
        alice_dists = self.aliceDistancesToGoats()
        bob_dists = self.bobDistancesToGoats()

        min_alice = min(alice_dists[0], alice_dists[1])
        min_bob = min(bob_dists[0], bob_dists[1])

        if min_alice < min_bob:
            return "ALICE"
        elif min_bob < min_alice:
            return "BOB"
        else:
            return "DRAW"

    def aliceDistancesToGoats(self) -> tuple[int, int]:
        dist1: int = (self.goat_1[0] * self.board_dimensions[1]) + self.goat_1[1]
        dist2: int = (self.goat_2[0] * self.board_dimensions[1]) + self.goat_2[1]
        return (dist1, dist2)

    def bobDistancesToGoats(self) -> tuple[int, int]:
        dist1: int = self.goat_1[0] + (self.goat_1[1] * self.board_dimensions[0])
        dist2: int = self.goat_2[0] + (self.goat_2[1] * self.board_dimensions[0])
        return (dist1, dist2)


def doPuzzleWithClasses():
    board_dimensions = (3, 8)
    board_area = board_dimensions[0] * board_dimensions[1]

    alice_wins = 0
    bob_wins = 0
    draws = 0

    total_combinations = 0

    for outer in range(0, board_area):
        row1 = outer // board_dimensions[1]
        col1 = outer % board_dimensions[1]
        for inner in range(outer + 1, board_area):
            row2 = inner // board_dimensions[1]
            col2 = inner % board_dimensions[1]

            winner = Combination(
                goat_1=(row1, col1),
                goat_2=(row2, col2),
                board_dimensions=board_dimensions,
            ).getWinner()
            if winner == "ALICE":
                alice_wins += 1
            elif winner == "BOB":
                bob_wins += 1
            else:
                alice_wins += 1
                bob_wins += 1
                draws += 1

            total_combinations += 1

    print(f"STATISTICS FOR {board_dimensions[0]}x{board_dimensions[1]} BOARD:")
    print(f"TOTAL COMBINATIONS: {total_combinations}")

    print(f"ALICE WINS: {alice_wins}")
    print(f"BOB WINS: {bob_wins}")
    print(f"DRAWS: {draws}")


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

        # Column-major: (0,0) -> (1,0) -> (2,0) -> (0, 1)
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
        if winner is True:
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


# doPuzzle()

doPuzzleWithClasses()
