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


def doCombinatoric():
    board_dimensions = (5, 5)
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

    print(
        f"\n\nCOMBINATORIC STATISTICS FOR {board_dimensions[0]}x{board_dimensions[1]} BOARD:"
    )
    print(f"TOTAL COMBINATIONS: {total_combinations}")

    print(f"ALICE WINS: {alice_wins}")
    print(f"BOB WINS: {bob_wins}")
    print(f"DRAWS: {draws}")

    increased_odds = (alice_wins / bob_wins) - 1

    print(f"ODDS DIFFERENCE: {increased_odds:.2%}")


def doMonteCarlo():
    ITERATIONS = 1_050_000

    board_dimensions = (5, 5)

    alice_wins = 0
    bob_wins = 0
    draws = 0

    for iteration in range(0, ITERATIONS):
        boxes = generateBoxes(board_dimensions)
        winners = simulate(boxes, board_dimensions)
        if winners[0] == winners[1]:
            draws += 1
        alice_wins += winners[0]
        bob_wins += winners[1]

    print(
        f"\n\nMONTE CARLO STATISTICS FOR {board_dimensions[0]}x{board_dimensions[1]} BOARD WITH {ITERATIONS} ITERATIONS:"
    )
    print(f"ALICE WINS: {alice_wins}")
    print(f"BOB WINS: {bob_wins}")
    print(f"DRAWS: {draws}")

    increased_odds = (alice_wins / bob_wins) - 1

    print(f"ODDS DIFFERENCE: {increased_odds:.2%}")


def simulate(boxes: list[list[str]], dimensions: tuple[int, int]) -> tuple[int, int]:
    alice_won = 0
    bob_won = 0

    board_area = dimensions[0] * dimensions[1]

    for position in range(0, board_area, 1):
        winner: bool = False

        # Row-major: (0,0) -> (0,1) -> (0,2) ...
        alice_pos = (position // dimensions[1], position % dimensions[1])

        # Column-major: (0,0) -> (1,0) -> (2,0) -> (0, 1)
        bob_pos = (position % dimensions[0], position // dimensions[0])

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


def generateBoxes(dimensions: tuple[int, int]) -> list[list[str]]:
    boxes: list[list[str]] = []
    for row in range(0, dimensions[0]):
        boxes.append([])
        for col in range(0, dimensions[1]):
            boxes[row].append("NONE")

    # Add goat 1
    boxes[random.randint(0, dimensions[0] - 1)][
        random.randint(0, dimensions[1] - 1)
    ] = "GOAT"

    # Add goat 2
    while True:
        position = (
            random.randint(0, dimensions[0] - 1),
            random.randint(0, dimensions[1] - 1),
        )

        if boxes[position[0]][position[1]] == "GOAT":
            continue
        else:
            boxes[position[0]][position[1]] = "GOAT"
            break

    return boxes


doMonteCarlo()

doCombinatoric()
