package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File


fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part1() {
    val input = File("./input/day16_test.txt").readLines()

    // Parse into all the nodes.
    val valveMapping = parse(input)

    // Calculate the shortest path to all nodes based on start node
    val shortestPathMapping = getShortestPathMapping(valveMapping)

    // Calculate the maximal pressure
    val optimalPressures = calculateOptimalPressure(
            valveMapping["AA"]!!,
            valveMapping,
            shortestPathMapping,
            30
    )

    println("Part1: ${optimalPressures[0].second.last()}")
}

fun calculateOptimalPressure(
        startNode: Valve,
        valveMapping: HashMap<String, Valve>,
        shortestPathMapping: HashMap<String, HashMap<String, Pair<Int, String>>>,
        totalTime: Int,
        visited: List<String> = emptyList()
): List<Pair<List<String>, List<Int>>> {
    val valves = valveMapping.values

    fun getAllPermutations(
            currentValve: Valve,
            currentPath: Pair<List<String>, List<Int>>,
            minuteRemaining: Int
    ): Set<Pair<List<String>, List<Int>>> {
        // What valves are remaining to check
        val remainingValves = valves
                .filter { !visited.contains(it.key) }
                .filter { !currentPath.first.contains(it.key) }
                .filter { it.rate != 0 }
                .filter { minuteRemaining - (shortestPathMapping[currentValve.key]!![it.key]!!.first + 1) >= 0 }

        // Execute the calculation for all of them
        return if (remainingValves.isNotEmpty()) {
            remainingValves.flatMap {
                getAllPermutations(
                        it,
                        Pair(
                                currentPath.first.plus(it.key),
                                currentPath.second.plus(currentPath.second.last() + (minuteRemaining - (shortestPathMapping[currentValve.key]!![it.key]!!.first + 1)) * it.rate)
                        ),
                        minuteRemaining - (shortestPathMapping[currentValve.key]!![it.key]!!.first + 1)
                )
            }.toSet()
        } else setOf(currentPath)
    }

    val allPermutations = getAllPermutations(startNode, Pair(listOf(startNode.key), listOf(0)), totalTime)
    return allPermutations.sortedByDescending { it.second.last() }

}

private fun getShortestPathMapping(valveMapping: HashMap<String, Valve>): HashMap<String, HashMap<String, Pair<Int, String>>> {
    val shortestPath = hashMapOf<String, HashMap<String, Pair<Int, String>>>()
    for (startNode in valveMapping.values) {
        shortestPath[startNode.key] = getShortestPaths(valveMapping, startNode)
    }
    return shortestPath
}

fun getShortestPaths(
        graph: java.util.HashMap<String, Valve>,
        startNode: Valve
): java.util.HashMap<String, Pair<Int, String>> {
    val paths = hashMapOf(startNode.key to Pair(0, ""))
    val visited = mutableListOf<Valve>()
    val unvisited = graph.values.toMutableList()
    var currentNode = startNode
    while (unvisited.isNotEmpty()) {
        var cost = 0
        if (paths.contains(currentNode.key)) {
             cost = paths[currentNode.key]!!.first
        }
        for (node in currentNode.neighbors) {
            if (paths.contains(node.key)) {
                val newCost = cost + 1
                if (newCost < paths[node.key]!!.first) {
                    paths[node.key] = cost + 1 to currentNode.key
                }
            } else {
                paths[node.key] = cost + 1 to currentNode.key
            }
        }
        visited.add(currentNode)
        unvisited.remove(currentNode)
        unvisited.sortBy { if (paths.contains(it.key)) {
            return@sortBy paths[it.key]!!.first
        } else {
            return@sortBy 999999
        }}
        if (unvisited.isNotEmpty()) {
            currentNode = unvisited.first()
        }
    }
    return paths
}

private fun parse(input: List<String>): HashMap<String, Valve> {
    val valveMapping = hashMapOf<String, Valve>()
    for (line in input) {
        val key = line.split(" ")[1]
        val rate = line.replace(";", "=").split("=")[1].toInt()
        valveMapping[key] = Valve(key, rate)
    }
    for (line in input) {
        val key = line.split(" ")[1]
        val split = line.split(";")[1].replace(", ", " ").split(" ")
        val relatedValves = split.subList(5, split.size)
        for (valve in relatedValves) {
            val neighbor = valveMapping[valve]
            valveMapping[key]?.addNeighbor(neighbor)
        }
    }
    return valveMapping
}

class Valve(val key: String, val rate: Int) {
    var neighbors: MutableList<Valve> = mutableListOf()

    fun addNeighbor(valve: Valve?) {
        if (valve == null) {
            return
        }
        neighbors.add(valve)
    }
}

private fun part2() {
    val input = File("./input/day16.txt").readLines()

    // Parse into all the nodes.
    val valveMapping = parse(input)

    // Calculate the shortest path to all nodes based on start node
    val shortestPathMapping = getShortestPathMapping(valveMapping)

    // Calculate the maximal pressure
    val myPaths = calculateOptimalPressure(
            valveMapping["AA"]!!,
            valveMapping,
            shortestPathMapping,
            26
    )

    var bestValue = myPaths[0].second.last()
    val size = myPaths.size
    var iter = 0
    myPaths.forEach {
        println("Iteration $iter/$size -> BV: $bestValue")
        bestValue = calculateCombinedOptimal(it, valveMapping, shortestPathMapping, bestValue)
        iter++
    }
    println("Part2: $bestValue")
}

private fun calculateCombinedOptimal(
        path: Pair<List<String>, List<Int>>,
        valveMapping: HashMap<String, Valve>,
        shortestPathMapping: HashMap<String, HashMap<String, Pair<Int, String>>>,
        bestValue: Int
): Int {
    var bestValue1 = bestValue
    for (i in path.first.indices) {
        val v = calculateOptimalPressure(
                valveMapping["AA"]!!,
                valveMapping,
                shortestPathMapping,
                26,
                path.first.slice(1..i)
        )
        val total = v[0].second.last() + path.second[i]
        if (total > bestValue1) {
            bestValue1 = total
        }
    }
    return bestValue1
}