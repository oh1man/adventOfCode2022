
from utils.Stopwatch import runWithStopwatch


def part1():
    lines = open("../input/day08.txt").readlines()
    forest = []
    for line in lines:
        forest.append([*line.strip()])

    numberOfVisible = 0
    for i in range(0, len(forest)):
        for j in range(0, len(forest[0])):
            tree = forest[i][j]

            left = forest[i][0:j]
            right = forest[i][(j+1):]
            vertically = [row[j] for row in forest]
            top = vertically[0:i]
            bottom = vertically[(i+1):]

            if isVisible(left, right, top, bottom, tree):
                numberOfVisible += 1

    print("Number of visible trees: " + str(numberOfVisible))


def isVisible(left, right, top, bottom, tree):
    visible_left = isDirectionalVisible(left, tree)
    visible_right = isDirectionalVisible(right, tree)
    visible_top = isDirectionalVisible(top, tree)
    visible_bottom = isDirectionalVisible(bottom, tree)
    return visible_left or visible_right or visible_top or visible_bottom


def isDirectionalVisible(left, tree):
    visible_left = True
    for blockingTree in left:
        if blockingTree >= tree:
            visible_left = False
    return visible_left


def part2():
    lines = open("../input/day08.txt").readlines()
    forest = []
    for line in lines:
        forest.append([*line.strip()])

    scenic_scores = []
    for i in range(0, len(forest)):
        for j in range(0, len(forest[0])):
            tree = forest[i][j]

            left = forest[i][0:j]
            right = forest[i][(j + 1):]
            vertically = [row[j] for row in forest]
            top = vertically[0:i]
            bottom = vertically[(i + 1):]

            scenic_scores.append(getScenicScore(left, right, top, bottom, tree))

    scenic_scores.sort(reverse=True)

    print("Number of visible trees: " + str(scenic_scores[0]))


def getScenicScore(left, right, top, bottom, tree) -> int:
    left.reverse()
    top.reverse()
    left_scenic_score = getDirectionalScenicScore(left, tree)
    right_scenic_score = getDirectionalScenicScore(right, tree)
    top_scenic_score = getDirectionalScenicScore(top, tree)
    bottom_scenic_score = getDirectionalScenicScore(bottom, tree)
    return left_scenic_score * right_scenic_score * top_scenic_score * bottom_scenic_score


def getDirectionalScenicScore(tree_line, tree):
    scenic_score = 0
    for blockingTree in tree_line:
        scenic_score += 1
        if blockingTree >= tree:
            break
    return scenic_score


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
