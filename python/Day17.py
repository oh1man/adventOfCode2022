from utils.Stopwatch import runWithStopwatch


def part1():
    jetstream = open("../input/day17.txt", "r").read().strip()
    chamber = Chamber(7, jetstream, 2, 3)
    for i in range(2022):
        chamber.drop()
    print("Part1: " + str(chamber.getHeight()), end="\n")

def part2():
    jetstream = open("../input/day17.txt", "r").read().strip()
    chamber = Chamber(7, jetstream, 2, 3)
    numberOfRocks = 0
    oldNumberOfRocks = 0
    investigation = []
    oldHeight = 0
    oldDelta = 0

    pairsOccurring = dict()
    pairs = []
    oldSize = 0

    while True:
        numberOfRocks += 1
        chamber.drop()
        """
        pairs.append((chamber.j, chamber.rockGenerator.generatorIndex))
        pairs = list(set(pairs))
        if len(pairs) == 
        print(len(pairs), end="\n")
        o = (chamber.j, chamber.rockGenerator.generatorIndex)
        pairs.append(o)
        pairs = list(set(pairs))
        if o in pairsOccurring.keys():
            pairsOccurring[o] += 1
        else:
            pairsOccurring[o] = 1
        """

        if chamber.j == 123 and chamber.rockGenerator.generatorIndex == 0:
            newHeight = chamber.getHeight()
            delta = newHeight - oldHeight
            deltaRocks = numberOfRocks - oldNumberOfRocks
            pairs.append((numberOfRocks, deltaRocks, newHeight, delta))
            if delta == oldDelta:
                break
            else:
                oldHeight = newHeight
                oldDelta = delta
                oldNumberOfRocks = numberOfRocks

    initialHeight = pairs[0][2]
    rocksLeft = 1000000000000 - pairs[0][0]
    factor = int(rocksLeft / pairs[1][1])
    sim_height = pairs[1][3] * factor
    totalHeight = initialHeight + sim_height
    print("Part2: " + str(totalHeight), end="\n")

# This is the main simulator class
# Owns the physics for the dropping.
class Chamber:
    def __init__(self, width, jetstream, leftDiff, verticalDiff):
        self.j = 0
        self.width = width
        self.rightWall = 8
        self.leftWall = 0
        self.jetstream = jetstream
        self.rocks: list[tuple] = []
        self.rockGenerator = RockGenerator()
        self.leftDiff = leftDiff
        self.verticalDiff = verticalDiff
        self.floor = []
        self.floorLevel = 0
        for i in range(1, width + 1):
            self.floor.append((i, self.floorLevel))

    def drop(self):
        bot = self.getHeight() + self.verticalDiff + 1
        left = self.leftWall + self.leftDiff + 1
        rock = self.rockGenerator.getNextRock(left, bot)
        falling = True
        while falling:
            # Step sideways
            stream = self.jetstream[self.j]
            match stream:
                case ">":
                    if not rock.isLeftOf(self.rightWall, self.rocks):
                        rock.moveRight()
                case "<":
                    if not rock.isRightOf(self.leftWall, self.rocks):
                        rock.moveLeft()
            self.j += 1
            if self.j == len(self.jetstream):
                self.j = 0

            # Step down
            if not rock.isOver(self.floor, self.rocks):
                rock.moveDown()
            else:
                falling = False

        for el in rock.coordinates:
            self.rocks.append(el)
        self.rocks.sort(key=lambda x: x[1])

    def getHeight(self):
        if len(self.rocks) == 0:
            return self.floorLevel
        else:
            self.rocks.sort(key=lambda p: p[1], reverse=True)
            return self.rocks[0][1]


class Rock:
    def __init__(self, pattern, left, bot):
        self.coordinates, self.shape = pattern(left, bot)

    def moveDown(self):
        """
        Moves the rock coordinates down.
        """
        under = self.getCoordinatesUnder()
        for i in range(len(under)):
            self.coordinates[i] = under[i]

    def getCoordinatesUnder(self):
        under = []
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            under.append((x, y - 1))
        return under

    def isOver(self, floor, rocks):
        """
        Checks if coordinates is under the rock formation
        """
        under = self.getCoordinatesUnder()
        return self.isIn(under, floor) or self.isIn(under, rocks)

    def moveRight(self):
        """
        Moves the rock coordinates to the right.
        """
        right = self.getCoordinatesToRight()
        for i in range(len(right)):
            self.coordinates[i] = right[i]

    def getCoordinatesToRight(self):
        right = []
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            right.append((x + 1, y))
        return right

    def isLeftOf(self, wall, rocks):
        right = self.getCoordinatesToRight()
        right_x = list(map(lambda t: t[0], right))
        return wall in right_x or self.isIn(right, rocks)

    def moveLeft(self):
        """
        Moves the rock coordinates to the left.
        """
        left = self.getCoordinatesToLeft()
        for i in range(len(left)):
            self.coordinates[i] = left[i]

    def getCoordinatesToLeft(self):
        left = []
        for i in range(len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            left.append((x - 1, y))
        return left

    def isRightOf(self, wall, rocks):
        left = self.getCoordinatesToLeft()
        left_x = list(map(lambda t: t[0], left))
        return wall in left_x or self.isIn(left, rocks)

    def isIn(self, points, rocks):
        for el in rocks:
            if el in points:
                return True
        return False


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
    runWithStopwatch(part2)
