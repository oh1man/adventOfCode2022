from utils.Stopwatch import runWithStopwatch


class Cost:
    def __init__(self, numberOfOres, numberOfClay, numberOfObsidian):
        self.numberOfOres = numberOfOres
        self.numberOfClay = numberOfClay
        self.numberOfObsidian = numberOfObsidian


class Blueprint:
    def __init__(self, id, oreRobotCost: Cost, clayRobotCost: Cost, obsidianRobotCost: Cost, geodeRobotCost: Cost):
        self.id = id
        self.oreRobotCost = oreRobotCost
        self.clayRobotCost = clayRobotCost
        self.obsidianRobotCost = obsidianRobotCost
        self.geodeRobotCost = geodeRobotCost


class Resources:
    def __init__(self,
                 numberOfOreRobots=1,
                 numberOfClayRobots=0,
                 numberOfObsidianRobots=0,
                 numberOfGeodeRobots=0,
                 numberOfOres=0,
                 numberOfClay=0,
                 numberOfObsidian=0,
                 numberOfGeodes=0
                 ):
        self.numberOfOreRobots = numberOfOreRobots
        self.numberOfClayRobots = numberOfClayRobots
        self.numberOfObsidianRobots = numberOfObsidianRobots
        self.numberOfGeodeRobots = numberOfGeodeRobots
        self.numberOfOres = numberOfOres
        self.numberOfClay = numberOfClay
        self.numberOfObsidian = numberOfObsidian
        self.numberOfGeodes = numberOfGeodes

    def farm(self):
        self.numberOfOres = self.numberOfOres + self.numberOfOreRobots
        self.numberOfClay = self.numberOfClay + self.numberOfClayRobots
        self.numberOfObsidian = self.numberOfObsidian + self.numberOfObsidianRobots
        self.numberOfGeodes = self.numberOfGeodes + self.numberOfGeodeRobots

    def copy(self):
        return Resources(
            self.numberOfOreRobots, self.numberOfClayRobots, self.numberOfObsidianRobots, self.numberOfGeodeRobots,
            self.numberOfOres, self.numberOfClay, self.numberOfObsidian, self.numberOfGeodes
        )

    def addOreRobot(self):
        self.numberOfOreRobots = self.numberOfOreRobots + 1

    def addClayRobot(self):
        self.numberOfClayRobots = self.numberOfClayRobots + 1

    def addObsidianRobot(self):
        self.numberOfObsidianRobots = self.numberOfObsidianRobots + 1

    def addGeodeRobot(self):
        self.numberOfGeodeRobots = self.numberOfGeodeRobots + 1

    def pay(self, cost: Cost):
        self.numberOfOres = self.numberOfOres - cost.numberOfOres
        self.numberOfClay = self.numberOfClay - cost.numberOfClay
        self.numberOfObsidian = self.numberOfObsidian - cost.numberOfObsidian

    def afford(self, cost: Cost):
        return \
            self.numberOfOres >= cost.numberOfOres and \
            self.numberOfClay >= cost.numberOfClay and \
            self.numberOfObsidian >= cost.numberOfObsidian

    def hasRateOf(self, cost):
        return \
            self.numberOfOreRobots >= cost.numberOfOres and \
            self.numberOfClayRobots >= cost.numberOfClay and \
            self.numberOfObsidianRobots >= cost.numberOfObsidian


class RobotFactory:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

    def affordOreRobot(self, resource: Resources):
        return resource.afford(self.blueprint.oreRobotCost)

    def affordClayRobot(self, resource: Resources):
        return resource.afford(self.blueprint.clayRobotCost)

    def affordObsidianRobot(self, resource: Resources):
        return resource.afford(self.blueprint.obsidianRobotCost)

    def affordGeodeRobot(self, resource: Resources):
        return resource.afford(self.blueprint.geodeRobotCost)

    def hasOreRate(self, resource: Resources):
        return \
            resource.numberOfOreRobots >= self.blueprint.oreRobotCost.numberOfOres and \
            resource.numberOfOreRobots >= self.blueprint.clayRobotCost.numberOfOres and \
            resource.numberOfOreRobots >= self.blueprint.obsidianRobotCost.numberOfOres and \
            resource.numberOfOreRobots >= self.blueprint.geodeRobotCost.numberOfOres

    def hasClayRate(self, resource: Resources):
        return \
            resource.numberOfClayRobots >= self.blueprint.oreRobotCost.numberOfClay and \
            resource.numberOfClayRobots >= self.blueprint.clayRobotCost.numberOfClay and \
            resource.numberOfClayRobots >= self.blueprint.obsidianRobotCost.numberOfClay and \
            resource.numberOfClayRobots >= self.blueprint.geodeRobotCost.numberOfClay

    def hasObsidianRate(self, resource: Resources):
        return \
            resource.numberOfObsidianRobots >= self.blueprint.oreRobotCost.numberOfObsidian and \
            resource.numberOfObsidianRobots >= self.blueprint.clayRobotCost.numberOfObsidian and \
            resource.numberOfObsidianRobots >= self.blueprint.obsidianRobotCost.numberOfObsidian and \
            resource.numberOfObsidianRobots >= self.blueprint.geodeRobotCost.numberOfObsidian


    def buildOreRobot(self, resource: Resources):
        tempResource = resource.copy()
        tempResource.pay(self.blueprint.oreRobotCost)
        tempResource.farm()
        tempResource.addOreRobot()
        return tempResource

    def buildClayRobot(self, resource: Resources):
        tempResource = resource.copy()
        tempResource.pay(self.blueprint.clayRobotCost)
        tempResource.farm()
        tempResource.addClayRobot()
        return tempResource

    def buildObsidianRobot(self, resource: Resources):
        tempResource = resource.copy()
        tempResource.pay(self.blueprint.obsidianRobotCost)
        tempResource.farm()
        tempResource.addObsidianRobot()
        return tempResource

    def buildGeodeRobot(self, resource: Resources):
        tempResource = resource.copy()
        tempResource.pay(self.blueprint.geodeRobotCost)
        tempResource.farm()
        tempResource.addGeodeRobot()
        return tempResource


def getOptimalNumberOfGeodes(factory: RobotFactory, resource: Resources, timeLeft: int):
    if timeLeft == 0:
        return resource.numberOfGeodes

    # Based on the resources check if we can build a robot or not.
    numberOfGeodes = []
    if factory.affordGeodeRobot(resource) and timeLeft >= 2:
        numberOfGeodes.append(getOptimalNumberOfGeodes(factory, factory.buildGeodeRobot(resource), timeLeft - 1))
    else:
        if factory.affordOreRobot(resource) and not factory.hasOreRate(resource) and timeLeft >= 2:
            numberOfGeodes.append(getOptimalNumberOfGeodes(factory, factory.buildOreRobot(resource), timeLeft - 1))

        if factory.affordClayRobot(resource) and not factory.hasClayRate(resource) and timeLeft >= 2:
            numberOfGeodes.append(getOptimalNumberOfGeodes(factory, factory.buildClayRobot(resource), timeLeft - 1))

        if factory.affordObsidianRobot(resource) and not factory.hasObsidianRate(resource) and timeLeft >= 2:
            numberOfGeodes.append(getOptimalNumberOfGeodes(factory, factory.buildObsidianRobot(resource), timeLeft - 1))

        if len(numberOfGeodes) == 0 or shouldWait(factory, resource):
            resource.farm()
            numberOfGeodes.append(getOptimalNumberOfGeodes(factory, resource.copy(), timeLeft - 1))

    numberOfGeodes.sort(reverse=True)
    return numberOfGeodes[0]


def hasRateToBuildAll(resource):
    return resource.numberOfOreRobots > 0 and resource.numberOfClayRobots > 0 and resource.numberOfObsidianRobots


def shouldWait(factory, resource):
    if resource.numberOfOreRobots > 0:
        return not hasHighestOre(factory, resource)

    if resource.numberOfClayRobots > 0:
        return not hasHighestClay(factory, resource)

    if resource.numberOfObsidianRobots > 0:
        return not hasHighestObsidian(factory, resource)

    return False


def hasHighestObsidian(factory, resource):
    highest = [
        factory.blueprint.oreRobotCost.numberOfObsidian,
        factory.blueprint.clayRobotCost.numberOfObsidian,
        factory.blueprint.obsidianRobotCost.numberOfObsidian,
        factory.blueprint.geodeRobotCost.numberOfObsidian
    ]
    highest.sort(reverse=True)
    return resource.numberOfObsidian >= highest[0]


def hasHighestClay(factory, resource):
    highest = [
        factory.blueprint.oreRobotCost.numberOfClay,
        factory.blueprint.clayRobotCost.numberOfClay,
        factory.blueprint.obsidianRobotCost.numberOfClay,
        factory.blueprint.geodeRobotCost.numberOfClay
    ]
    highest.sort(reverse=True)
    return resource.numberOfClay >= highest[0]


def hasHighestOre(factory, resource):
    highest = [
        factory.blueprint.oreRobotCost.numberOfOres,
        factory.blueprint.clayRobotCost.numberOfOres,
        factory.blueprint.obsidianRobotCost.numberOfOres,
        factory.blueprint.geodeRobotCost.numberOfOres
    ]
    highest.sort(reverse=True)
    return resource.numberOfOres >= highest[0]


def parse(input_text):
    blueprints = []
    for line in input_text:
        line = line.strip().replace(":", " ").split(" ")
        blueprints.append(Blueprint(
            int(line[1]),
            Cost(int(line[7]), 0, 0),
            Cost(int(line[13]), 0, 0),
            Cost(int(line[19]), int(line[22]), 0),
            Cost(int(line[28]), 0, int(line[31]))
        ))
    return blueprints


def part1():
    input_text = open("../input/day19.txt", "r").readlines()
    blueprints = parse(input_text)

    totalQualityLevel = 0
    for blueprint in blueprints:
        geodes = getOptimalNumberOfGeodes(RobotFactory(blueprint), Resources(), 24)
        qualityLevel = blueprint.id * geodes
        totalQualityLevel = totalQualityLevel + qualityLevel
        print("Blueprint " + str(blueprint.id) + ": " + str(qualityLevel))

    print("Part1: " + str(totalQualityLevel), end="\n")


def part2():
    input_text = open("../input/day19.txt", "r").readlines()
    blueprints = parse(input_text)

    answer = 1
    for blueprint in blueprints[0:3]:
        geodes = getOptimalNumberOfGeodes(RobotFactory(blueprint), Resources(), 32)
        answer = answer * geodes
        print("Blueprint " + str(blueprint.id) + ": " + str(geodes))

    print("Part2: " + str(answer), end="\n")


if __name__ == '__main__':
    runWithStopwatch(part1)
    runWithStopwatch(part2)
