
from enum import Enum

from utils.Stopwatch import runWithStopwatch


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    @staticmethod
    def of(code: str):
        match code:
            case "A" | "X":
                return Hand.ROCK
            case "B" | "Y":
                return Hand.PAPER
            case "C" | "Z":
                return Hand.SCISSOR
            case other:
                return 0

    def getWinningHand(self):
        match self:
            case Hand.ROCK:
                return Hand.PAPER
            case Hand.PAPER:
                return Hand.SCISSOR
            case Hand.SCISSOR:
                return Hand.ROCK
            case other:
                return 0


def play(opponent: Hand, hand: Hand):
    if opponent.getWinningHand() == hand:
        return 6 + hand.value
    elif opponent == hand:
        return 3 + hand.value
    return hand.value


def convertToHand(opponent_hand: Hand, strategy: str) -> Hand:
    match strategy:
        case "X":
            return opponent_hand.getWinningHand().getWinningHand()
        case "Y":
            return opponent_hand
        case "Z":
            return opponent_hand.getWinningHand()


def day02():
    file = open("../input/day02.txt", "r")
    lines = file.readlines()
    wrong_points = 0
    correct_points = 0
    for line in lines:
        split = line.strip().split(" ")
        opponent_hand = Hand.of(split[0])
        wrong_points += play(opponent_hand, Hand.of(split[1]))
        correct_points += play(opponent_hand, convertToHand(opponent_hand, split[1]))
    print("Total wrong points: " + str(wrong_points))
    print("Total correct points: " + str(correct_points))


if __name__ == '__main__':
    runWithStopwatch(day02)
