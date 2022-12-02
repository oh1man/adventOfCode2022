import time
from enum import Enum, IntEnum


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


def convertToHand(opponentHand: Hand, strategy: str) -> Hand:
    match strategy:
        case "X":
            return opponentHand.getWinningHand().getWinningHand()
        case "Y":
            return opponentHand
        case "Z":
            return opponentHand.getWinningHand()


if __name__ == '__main__':
    startTime = time.time_ns()

    file = open("../input/day02.txt", "r")
    lines = file.readlines()
    wrongPoints = 0
    correctPoints = 0
    for line in lines:
        split = line.strip().split(" ")
        opponentHand = Hand.of(split[0])
        wrongPoints += play(opponentHand, Hand.of(split[1]))
        correctPoints += play(opponentHand, convertToHand(opponentHand, split[1]))

    print("Total wrong points: " + str(wrongPoints))
    print("Total correct points: " + str(correctPoints))

    endTime = time.time_ns()
    print("Elapsed time: " + str((endTime - startTime) / 1000000000) + " sec")
