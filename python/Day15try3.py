from collections import defaultdict

LIMIT_P2 = 4000000
LIMIT_P1 = 2000000


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        return (self.x + other.x, self.y + other.y)

    def delta(self, x=0, y=0):
        return Point(self.x + x, self.y + y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(f"{self.x},{self.y}")

    def __repr__(self):
        return f"Point({self.x},{self.y})"


def part1(str_data: str, y: int):
    sensors, beacons, pairs = get_map(str_data)
    locations = set()

    for s, b in pairs:
        locations.update(get_marks_at_y_axis(s, b, y))

    for s in sensors:
        if s.y == y:
            locations.remove(s.x)

    for b in beacons:
        if b.y == y:
            locations.remove(b.y)

    print(y, len(locations))


def part2(str_data: str, limit_tl: Point, limit_dr: Point):
    sensors, beacons, pairs = get_map(str_data)
    store = defaultdict(lambda: 0)

    sensor_id = 0
    sensor_total = len(sensors)
    for sensor, beacon in pairs:
        sensor_id += 1

        dist = manhattan_distance(sensor, beacon) + 1
        print(f"{sensor_id} of {sensor_total}: sensor {sensor} with beacon {beacon} (distance={dist})")
        vertical = -1

        xmin = max(limit_tl.x, sensor.x - dist)
        xmax = min(limit_dr.x, sensor.x + dist)

        for x in range(xmin, xmax + 1):

            if x <= sensor.x:
                vertical += 1
            else:
                vertical -= 1

            cu = (x, sensor.y - vertical)
            cd = (x, sensor.y + vertical)

            if cu == cd:
                store[cu] += 1
            else:
                store[cu] += 1
                store[cd] += 1

            if store[cu] == 4:
                print(cu)

            if store[cd] == 4:
                print(cd)


def get_marks_at_y_axis(sensor: Point, beacon: Point, y):
    distance = manhattan_distance(sensor, beacon)
    distance_from_axis = abs(y - sensor.y)
    limit = max(distance - distance_from_axis, 0)
    return set(range(sensor.x - limit, sensor.x + limit + 1))


def manhattan_distance(s: Point, b: Point):
    return abs(b.x - s.x) + abs(b.y - s.y)


def get_map(str_data: str):
    sensors = set()
    beacons = set()
    pairs = []

    for l in str_data.strip().split('\n'):
        pieces = (l + ';').split(' ')
        pieces_chosen = [pieces[x][:-1].split('=')[-1] for x in (2, 3, 8, 9)]
        x1, y1, x2, y2 = map(int, pieces_chosen)
        sensors.add(Point(x1, y1))
        beacons.add(Point(x2, y2))
        pairs.append((Point(x1, y1), Point(x2, y2)))

    return sensors, beacons, pairs


def main():
    real = open('../input/day15.txt').read().strip()
    part1(real, LIMIT_P1)
    part2(real, Point(0, 0), Point(LIMIT_P2, LIMIT_P2))


if __name__ == '__main__':
    main()