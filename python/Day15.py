from utils.Stopwatch import runWithStopwatch


def part1():
    text_input = open("../input/day15.txt", "r").readlines()
    scan = Scan(text_input)
    print("Part1: " + str(scan.getNonScannedPosition(2000000)))


class Sensor:
    def __init__(self, sensor_input):
        self.sensor_input = sensor_input
        self.right = None
        self.left = None
        self.bot = None
        self.top = None
        self.position, self.beacon = self.parse(sensor_input)
        self.scanCorners = None

    def parse(self, sensor_input: str):
        parsed = sensor_input.strip().replace(",", "=").replace(":", "=").split("=")[1::2]
        return (int(parsed[1]), int(parsed[0])), \
               (int(parsed[3]), int(parsed[2]))

    def normalize(self, norm):
        self.position = (self.position[0] - norm, self.position[1] - norm)
        self.beacon = (self.beacon[0] - norm, self.beacon[1] - norm)

    def calculateScannedCorners(self):
        self.s = abs(self.position[0] - self.beacon[0]) + abs(self.position[1] - self.beacon[1])
        self.top = self.createPosition(self.position, 0, -self.s)
        self.bot = self.createPosition(self.position, 0, self.s)
        if self.top[1] > self.bot[1]:
            raise Exception("Error with corner calculation")
        self.left = self.createPosition(self.position, -self.s, 0)
        self.right = self.createPosition(self.position, self.s, 0)
        self.scanCorners = [self.top, self.bot, self.left, self.right]

    def createPosition(self, center, dx, dy) -> tuple:
        return center[0] + dx, \
               center[1] + dy


class Scan:
    def __init__(self, scan_input):
        self.sensors = self.parse(scan_input)
        self.norm = 0
        self.normalize()
        self.scan()
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

    def normalize(self):
        xy = []
        for sensor in self.sensors:
            xy.append(sensor.position[1])
            xy.append(sensor.beacon[1])
            xy.append(sensor.position[0])
            xy.append(sensor.beacon[0])
        xy = list(set(xy))
        xy.sort(reverse=True)
        self.norm = int(xy[0] / 2)
        for sensor in self.sensors:
            sensor.normalize(self.norm)

    def scan(self):
        for sensor in self.sensors:
            sensor.calculateScannedCorners()

    def initialize(self):
        ys = []
        for sensor in self.sensors:
            for point in [sensor.position, sensor.beacon]:
                ys.append(point[0])
        ys = list(set(ys))
        ys.sort()
        self.y0 = ys[0]
        self.y1 = ys[-1]
        xs = []
        for sensor in self.sensors:
            for point in [sensor.position, sensor.beacon]:
                xs.append(point[1])
        xs = list(set(xs))
        xs.sort()
        self.x0 = xs[0]
        self.x1 = xs[-1]

    def getNonScannedPosition(self, row):
        row = row - self.norm
        # Find potential sensors
        ps = []
        for sensor in self.sensors:
            if sensor.top[1] <= row <= sensor.bot[1]:
                ps.append(sensor)

        # Calculate how much is scanned on the row number including beacons
        xs = []
        for sensor in ps:
            match self.getScanPoint(row, sensor.position[1]):
                case -1:  # Top
                    diff = abs(sensor.top[1] - row)
                    self.createXs(diff, sensor, xs)
                case 1: # Bot
                    diff = abs(sensor.bot[1] - row)
                    self.createXs(diff, sensor, xs)
                case 0: # Same
                    self.createXs(sensor.s, sensor, xs)
        xs = list(set(xs))

        # Subtract all beacons on this row
        for sensor in ps:
            if sensor.position[0] == row and sensor.position[1] in xs:
                xs.remove(sensor.position[1])
            if sensor.beacon[0] == row and sensor.beacon[1] in xs:
                xs.remove(sensor.beacon[1])

        return len(xs)


    def createXs(self, diff, sensor, xs):
        for el in list(range(sensor.position[0] - diff, sensor.position[0] + diff + 1)):
            #if self.x0 <= el <= self.x1:
                xs.append(el)


    def getScanPoint(self, row, y):
        if y < row:
            return -1
        elif y > row:
            return 1
        else:
            return 0


if __name__ == '__main__':
    runWithStopwatch(part1)

