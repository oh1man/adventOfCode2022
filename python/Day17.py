from utils.Stopwatch import runWithStopwatch


def part1():
    jetstream = open("../input/day17_test.txt", "r").read().strip()
    chamber = Chamber(7, jetstream, 2, 3)
    for i in range(10):
        chamber.drop()
    print("Part1: " + str(1), end="\n")

# This is the main simulator class
# Owns the physics for the dropping.
class Chamber:
    def __init__(self, width, jetstream, leftDiff, verticalDiff):
        self.width = width
        self.jetstream = jetstream
        self.rocks: list[tuple] = []
        self.rockGenerator = RockGenerator()
        self.leftDiff = leftDiff
        self.verticalDiff = verticalDiff

    def drop(self):
        bot = self.getHeight() + self.verticalDiff
        left = self.leftDiff
        rock = self.rockGenerator.getNextRock(left, bot)

        # TODO: What height do we start at?
        # Do the simulation?
        print("test")
        # TODO: When at rest save the coordingates in the chamber
        for coor in rock.coordinates:
            self.rocks.append(coor)

    def getHeight(self):
        if len(self.rocks) == 0:
            return 0
        else:
            self.rocks.sort(key=lambda p: p[1])
            return self.rocks[0][1]



class Rock:
    def __init__(self, pattern, left, bot):
        self.coordinates, self.shape = pattern(left, bot)

    def moveDown(self):
        """
        Moves the rock coordinates down.
        """
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            self.coordinates[i] = (x, y - 1)

    def moveRight(self):
        """
        Moves the rock coordinates to the right.
        """
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            self.coordinates[i] = (x + 1, y)

    def moveLeft(self):
        """
        Moves the rock coordinates to the left.
        """
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            self.coordinates[i] = (x - 1, y)


class RockGenerator:
    rockOrder = [
        lambda left, bot: (
            [(left, bot), (left + 1, bot), (left + 2, bot), (left + 3, bot)],
            "-"
        ),
        lambda left, bot: (
            [(left, bot + 1), (left + 1, bot), (left + 1, bot + 1), (left + 1, bot + 2), (left + 2, bot + 1)],
            "+"
        ),
        lambda left, bot: (
            [(left, bot), (left + 1, bot), (left + 2, bot), (left + 2, bot + 1), (left + 2, bot + 2)],
            "_|"
        ),
        lambda left, bot: (
            [(left, bot), (left, bot + 1), (left, bot + 2), (left, bot + 3)],
            "|"
        ),
        lambda left, bot: (
            [(left, bot), (left, bot + 1), (left + 1, bot), (left + 1, bot + 1)],
            "#"
        )
    ]

    def __init__(self):
        self.generatorIndex = 0

    def getNextRock(self, left, bot):
        """
        Returns a rock of an arbitrary structure
        """
        rock = Rock(RockGenerator.rockOrder[self.generatorIndex], left, bot)
        self.updateGeneratorIndex()
        return rock

    def updateGeneratorIndex(self):
        """
        Updates the generator index
        """
        self.generatorIndex += 1
        if self.generatorIndex > len(RockGenerator.rockOrder) - 1:
            self.generatorIndex = 0


if __name__ == '__main__':
    runWithStopwatch(part1)
