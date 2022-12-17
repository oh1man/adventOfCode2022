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

    print("Part1: ")
    // For each unvisited calculation, calculate cost of the shortest path to each node.
    // TODO: Dijkstra again for each node

}

private fun calculateOptimalPressure(
        startNode: Valve,
        valveMapping: HashMap<String, Valve>,
        shortestPathMapping: HashMap<String, HashMap<String, Pair<Int, String>>>,
        totalTime: Int
): HashMap<String, Triple<Int, Int, MutableList<String>>> {
    var paths = hashMapOf(startNode.key to Triple(0, 0, mutableListOf<String>())) // First: Cost, Second: Total Pressure, Third: Previous node
    val visited = mutableListOf<Valve>()
    val unvisited = valveMapping.values.toMutableList()
    var currentNode = startNode
    while (unvisited.isNotEmpty()) {
        var timeSpent = 0
        if (paths.contains(currentNode.key)) {
            timeSpent = paths[currentNode.key]!!.first
        }
        val currentPath = paths[currentNode.key]?.third
        val currentPressure = paths[currentNode.key]?.second
        for (node in valveMapping.values) {
            if (node == currentNode) {
                continue
            }
            if (currentPath != null && currentPath.contains(node.key)) {
                continue
            }
            val cp = currentPath!!.toMutableList()
            cp.add(currentNode.key)
            val shortestPath = shortestPathMapping[currentNode.key]!![node.key]!!.first
            val newTimeSpent = timeSpent + shortestPath + 1
            val timeLeft = totalTime - newTimeSpent
            if (timeLeft < 0) {
                continue
            }
            val totalPressure = paths[currentNode.key]!!.second + timeLeft * node.rate
            if (paths.contains(node.key)) {
                if (totalPressure > currentPressure!!) {
                    paths[node.key] = Triple(newTimeSpent, totalPressure, cp)
                }
            } else {
                paths[node.key] = Triple(newTimeSpent, totalPressure, cp)
            }
        }
        val sortedPaths = paths.toList().sortedByDescending { (_, value) -> value.second }.toMap()
        visited.add(currentNode)
        unvisited.remove(currentNode)
        unvisited.sortByDescending { if (paths.contains(it.key)) {
            return@sortByDescending paths[it.key]!!.second
        } else {
            return@sortByDescending 0
        }}
        if (unvisited.isNotEmpty()) {
            currentNode = unvisited.first()
        }
    }
    return paths
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
    val input = File("./input/day16_test.txt").readLines()
}