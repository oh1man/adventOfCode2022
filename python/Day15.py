from utils.Stopwatch import runWithStopwatch


def part1():
    text_input = open("../input/day15.txt", "r").readlines()
    scan = Scan.__int__(text_input)
    print("Part1: " + str(scan.get_number_of_not_containing(24)))


class Sensor:
    def __int__(self, position):
        self.position: tuple = position
        self.beacon: tuple = ()
        self.scannedPositions: list[tuple] = []


class Scan:
    scannedPositions: list[tuple]
    scan: list[list[str]]

    def __int__(self, scan_input):
        self.sensors = self.parse(scan_input)
        self.scan = self.initialize()
        self.execute()

    def parse(self, scan_input):
        return [Sensor()]

    def initialize(self) -> list[list[str]]:
        ys = list(map(lambda sensor: sensor.scannedPositions[0], self.sensors))
        ys.sort()
        y0 = ys[0]  # TODO: Might need to create norm
        y1 = ys[-1]
        xs = list(map(lambda sensor: sensor.scannedPositions[1], self.sensors))
        xs.sort()
        x0 = ys[0]
        x1 = ys[-1]  # TODO: Might need to create norm
        return [[]]

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


class Element:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


class Sensor2:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


if __name__ == '__main__':
    runWithStopwatch(part1)
