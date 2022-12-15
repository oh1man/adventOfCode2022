from utils.Stopwatch import runWithStopwatch


def part1():
    text_input = open("../input/day15.txt", "r").readlines()
    scan = Scan(text_input)
    print("Part1: " + str(scan.get_number_of_not_containing(24)))


class Sensor:
    def __init__(self, sensor_input):
        self.position, self.beacon = self.parse(sensor_input)
        self.scanCorners: list[tuple] = self.calculateScannedCorners()

    def parse(self, sensor_input: str):
        parsed = sensor_input.strip().replace(",", "=").replace(":", "=").split("=")[1::2]
        return (int(parsed[1]), int(parsed[0])), \
               (int(parsed[3]), int(parsed[2]))

    def calculateScannedCorners(self):
        s = abs(self.position[0] - self.beacon[0]) + abs(self.position[1] - self.position[1])
        return [
            self.createPosition(self.position, s, 0),
            self.createPosition(self.position, -s, 0),
            self.createPosition(self.position, 0, s),
            self.createPosition(self.position, 0, -s)
        ]

    def createPosition(self, center, dx, dy) -> tuple:
        return center[0] + dx, \
               center[1] + dy


class Scan:
    def __init__(self, scan_input):
        self.sensors = self.parse(scan_input)
        self.y0 = None
        self.x0 = None
        self.y1 = None
        self.x1 = None
        self.initialize()

    def parse(self, scan_input):
        temp = []
        for line in scan_input:
            temp.append(Sensor(line))
        return temp

    def initialize(self):
        ys = []
        for sensor in self.sensors:
            for point in sensor.scanCorners:
                ys.append(point[0])
        ys = list(set(ys))
        ys.sort()
        self.y0 = ys[0]  # TODO: Might need to create norm
        self.y1 = ys[-1]
        xs = []
        for sensor in self.sensors:
            for point in sensor.scanCorners:
                ys.append(point[1])
        xs = list(set(xs))
        xs.sort()
        self.x0 = ys[0]
        self.x1 = ys[-1]  # TODO: Might need to create norm

    def execute(self):
        for sensor in self.sensors:
            for scannedPos in sensor.scannedPositions:
                if scannedPos == sensor.position:
                    self.scan[scannedPos[0]][scannedPos[1]] = "S"
                elif scannedPos == sensor.beacon:
                    self.scan[scannedPos[0]][scannedPos[1]] = "B"
                else:
                    self.scan[scannedPos[0]][scannedPos[1]] = "#"

    def get_number_of_not_containing(self, row_number):
        number = 0
        for pos in self.scan[row_number]:
            match pos:
                case "#" | "S" | "B":
                    number += 1
                case _:
                    continue
        return number


if __name__ == '__main__':
    runWithStopwatch(part1)

