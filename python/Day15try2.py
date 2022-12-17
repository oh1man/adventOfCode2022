
from utils.Stopwatch import runWithStopwatch

def part1():
    scan = Scan(open("../input/day15.txt", "r").readlines())
    print("Part1: " + str(scan.getAnswer1(2000000)))


def part2():
    scan = Scan(open("../input/day15.txt", "r").readlines())
    # Create the search space.

    val = scan.getAnswer2(0, 4_000_000)
    print("Part2: " + str(val))


class Span:
    def __init__(self, intervals: list[list[int]]):
        """
        A one dimensional interval with opening and closing points.
        Example: [(x1, x2), (x3, x4)]
        """
        self.intervals = intervals

    def intersection(self, span):
        """
        Creates the intersecting span between two spans.
        """
        intersection = []
        for interval in self.intervals:

            # Intersect opening
            opening = None
            target = span.intervals[0]
            if target[0] <= interval[0] <= target[1]:
                opening = interval[0]
            elif interval[0] <= target[0] <= interval[1]:
                opening = target[0]
            else:
                continue

            # Intersect closing
            closing = None
            if target[0] <= interval[1] <= target[1]:
                closing = interval[1]
            elif interval[0] <= target[1] <= interval[1]:
                closing = target[1]
            else:
                continue

            intersection.append([opening, closing])

        return Span(intersection)

    def isEmpty(self):
        return len(self.intervals) == 0

    def overlaps(self, p):
        for interval in self.intervals:
            return interval[0] <= p <= interval[1]

    def union(self, span):
        for i in range(1, len(self.intervals)):
            interval = self.intervals[i]
            span.union(Span([[interval[0], interval[1]]]))
        return span

    def antiIntersection(self):
        if not len(self.intervals) == 2:
            raise Exception("Something is wrong!")
        openings = [self.intervals[0][0], self.intervals[1][0]]
        openings.sort()
        closing = [self.intervals[0][1], self.intervals[1][1]]
        closing.sort()
        return Span([[closing[0], openings[1]]])




class Sensor:
    def __init__(self, input):
        self.input = input
        self.position, self.beacon = self.parse(input)
        self.s = abs(self.position[0] - self.beacon[0]) + abs(self.position[1] - self.beacon[1])
        self.vertical = range(self.position[0] - self.s, self.position[0] + self.s + 1)
        self.verticalSpan = Span([[self.position[0] - self.s, self.position[0] + self.s]])

    def parse(self, input: str):
        parsed = input.strip().replace(",", "=").replace(":", "=").split("=")[1::2]
        return (int(parsed[1]), int(parsed[0])), (int(parsed[3]), int(parsed[2]))

    def getHorizontal(self, row):
        diff = abs(abs(row - self.position[0]) - self.s)
        return list(range(self.position[1] - diff, self.position[1] + diff + 1))

    def getHorizontalPoints(self, row):
        diff = abs(abs(row - self.position[0]) - self.s)
        return (self.position[1] - diff, self.position[1] + diff)

    def getHorizontalSpan(self, x0, x1, row):
        points = self.getHorizontalPoints(row)
        return Span([[x0, x1]]).intersection(Span([[points[0], points[1]]]))


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
                onRow.append(el)

        for sensor in ps:
            if sensor.position[0] == row and sensor.position[1] in onRow:
                onRow.remove(sensor.position[1])
            if sensor.beacon[0] == row and sensor.beacon[1] in onRow:
                onRow.remove(sensor.beacon[1])

        return len(set(onRow))

    def getAnswer2(self, x0, x1):
        verticalSpan = Span([[x0, x1]])
        ps = []
        for sensor in self.sensors:
            if not sensor.verticalSpan.intersection(verticalSpan).isEmpty():
                ps.append(sensor)

        for row in range(3186981, x1 + 1):
            print(row, end="\n")
            spans = []
            for sensor in self.sensors:
                if sensor.verticalSpan.overlaps(row):
                    spans.append(sensor.getHorizontalSpan(x0, x1, row))

            spans.sort(key=lambda x: x.intervals[0][0])

            unionSpan = spans[0]
            for i in range(1, len(spans)):
                target = spans[i]
                opening = target.intervals[0][0]
                if unionSpan.overlaps(opening):
                    if unionSpan.intervals[0][1] < target.intervals[0][1]:
                        newClosing = target.intervals[0][1]
                    else:
                        newClosing = unionSpan.intervals[0][1]
                    unionSpan = Span([[unionSpan.intervals[0][0], newClosing]])
                else:
                    x = unionSpan.intervals[0][1] + 1
                    return 4000000 * x + row
        return None


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)