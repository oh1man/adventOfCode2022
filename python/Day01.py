from utils.Stopwatch import runWithStopwatch


def day01():
    f = open("../input/day01.txt", "r")
    calories = f.readlines()
    f.close()
    index = 0
    elvesInCalories = [0]
    for element in calories:
        if element.__eq__("\n"):
            index += 1
            elvesInCalories = elvesInCalories + [0]
            continue
        elvesInCalories[index] += int(element)
    topThree = sorted(elvesInCalories, reverse=True)[0:3]
    print("Elves with largest calories: " + str(max(elvesInCalories)))
    print("Total calories of top three: " + str(sum(topThree)))


if __name__ == '__main__':
    runWithStopwatch(day01)

