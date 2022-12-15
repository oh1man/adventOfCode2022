from utils.Stopwatch import runWithStopwatch


def part1():
    text_input = open("../input/day15.txt", "r").readlines()
    scan = Scan(text_input)
    print("Part1: " + str(scan.get_number_of_not_containing(24)))


class Sensor:
    position: tuple
    beacon: tuple
    scannedPositions: list[tuple]

    def __init__(self, sensor_input):
        self.position, self.beacon = self.parse(sensor_input)
        self.scannedPositions = []

    def parse(self, sensor_input: str):
        parsed = sensor_input.strip().replace(",", "=").replace(":", "=").split("=")[1::2]
        return (int(parsed[1]), int(parsed[0])), (int(parsed[3]), int(parsed[2]))


class Scan:
    sensors: list[Sensor]
    scan: list[list[str]]

    def __init__(self, scan_input):
        self.sensors = self.parse(scan_input)
        self.scan = self.initialize()
        self.execute()

    def parse(self, scan_input):
        temp = []
        for line in scan_input:
            temp.append(Sensor(line))
        return temp

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


if __name__ == '__main__':
    runWithStopwatch(part1)

