
from utils.Stopwatch import runWithStopwatch

def part1():
    scan = Scan(open("../input/day15.txt", "r").readlines())
    print("Part1: " + str(scan.getAnswer1(2000000)))


def part2():
    scan = Scan(open("../input/day15.txt", "r").readlines())
    # Create the search space.

    scan.getAnswer2(0, 4_000_000)

    print("Part2: " + str(scan.getAnswer2(2000000)))


class Sensor:
    def __init__(self, input):
        self.input = input
        self.position, self.beacon = self.parse(input)
        self.s = abs(self.position[0] - self.beacon[0]) + abs(self.position[1] - self.beacon[1])
        self.vertical = range(self.position[0] - self.s, self.position[0] + self.s + 1)

    def parse(self, input: str):
        parsed = input.strip().replace(",", "=").replace(":", "=").split("=")[1::2]
        return (int(parsed[1]), int(parsed[0])), (int(parsed[3]), int(parsed[2]))

    def getHorizontal(self, row):
        diff = abs(abs(row - self.position[0]) - self.s)
        return list(range(self.position[1] - diff, self.position[1] + diff + 1))

    def getHorizontalPoints(self, row):
        diff = abs(abs(row - self.position[0]) - self.s)
        return (self.position[1] - diff, self.position[1] + diff)

class Scan:
    def __init__(self, input):
        self.answer = None
        self.input = input
        self.sensors = []
        for line in input:
            self.sensors.append(Sensor(line))
        xs = []
        for sensor in self.sensors:
            for point in [sensor.position, sensor.beacon]:
                xs.append(point[1])
        xs = list(set(xs))
        xs.sort()
        self.x0 = xs[0]
        self.x1 = xs[-1]

    def getAnswer1(self, row):
        ps = []
        for sensor in self.sensors:
            if row in sensor.vertical:
                ps.append(sensor)

        onRow = []
        for sensor in ps:
            horizontal = sensor.getHorizontal(row)
            for el in horizontal:
                #if self.x0 <= el <= self.x1:
                onRow.append(el)

        for sensor in ps:
            if sensor.position[0] == row and sensor.position[1] in onRow:
                onRow.remove(sensor.position[1])
            if sensor.beacon[0] == row and sensor.beacon[1] in onRow:
                onRow.remove(sensor.beacon[1])

        return len(set(onRow))

    def getAnswer2(self, x0, x1):

        for row in range(x1 + 1):
            onRow = []
            for sensor in self.sensors:
                horizontal = sensor.getHorizontalPoints(row)
                for el in horizontal:
                    if x0 <= el <= x1:
                        onRow.append(el)
            onRow = set(onRow)
            if len(onRow) != x1 + 1:
                print("I got it!")

        """
        for sensor in ps:
            if sensor.position[0] == row and sensor.position[1] in onRow:
                onRow.remove(sensor.position[1])
            if sensor.beacon[0] == row and sensor.beacon[1] in onRow:
                onRow.remove(sensor.beacon[1])
        """

        return set(onRow)


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)