package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    val lines = File("./input/day12.txt").readLines()

    val heightMap = mutableListOf<MutableList<Node>>()
    val startNodes = mutableListOf<Node>()
    lateinit var endNode: Node

    for (i in lines.indices) {
        heightMap.add(i, mutableListOf())
        for (j in lines[i].indices) {
            val height = lines[i][j]
            val node = Node(i to j, height)
            heightMap[i].add(j, node)
            when (height) {
                'E' -> endNode = node
                'a' -> startNodes.add(node)
            }
        }
    }

    val endNodes = mutableListOf<Node>()
    for (startNode in startNodes) {
        val copyMap = mutableListOf<MutableList<Node>>()
        val visited = mutableListOf<Node>()
        val unvisited = mutableListOf<Node>()

        for (i in 0 until heightMap.size) {
            copyMap.add(mutableListOf())
            for (j in 0 until heightMap[i].size) {
                val node = heightMap[i][j].copy()
                copyMap[i].add(node)
                unvisited.add(node)
            }
        }

        startNode.distance = 0
        var node: Node = startNode
        repeat (unvisited.size) {
            getPotentialNodes(node.height, node.coordinates, copyMap, unvisited).forEach {
                val newDistance = node.distance + 1
                if (newDistance < it.distance) {
                    copyMap[it.coordinates.first][it.coordinates.second].distance = newDistance
                    copyMap[it.coordinates.first][it.coordinates.second].previous = node
                }
            }
            unvisited.remove(node)
            visited.add(node)
            if (unvisited.isNotEmpty()) {
                unvisited.sortBy { it.distance }
                node = unvisited[0]
            }
        }
        endNodes.add(copyMap[endNode.coordinates.first][endNode.coordinates.second])
        endNodes.sortBy { it.distance }
        println("Number of end points: ${endNodes.size} - shortest distance: ${endNodes[0].distance}")
    }
    println("Part2: ${endNodes[0].distance}")
}

private fun part1() {
    val lines = File("./input/day12.txt").readLines()

    val heightMap = mutableListOf<MutableList<Node>>()
    lateinit var startNode: Node
    lateinit var endNode: Node
    val visited = mutableListOf<Node>()
    val unvisited = mutableListOf<Node>()
    for (i in lines.indices) {
        heightMap.add(i, mutableListOf())
        for (j in lines[i].indices) {
            val height = lines[i][j]
            val node = Node(i to j, height)
            heightMap[i].add(j, node)
            when (height) {
                'S' -> startNode = node
                'E' -> endNode = node
            }
            unvisited.add(node)
        }
    }

    startNode.distance = 0
    var node: Node = startNode
    repeat (unvisited.size) {
        getPotentialNodes(node.height, node.coordinates, heightMap, unvisited).forEach {
            val newDistance = node.distance + 1
            if (newDistance < it.distance) {
                heightMap[it.coordinates.first][it.coordinates.second].distance = newDistance
                heightMap[it.coordinates.first][it.coordinates.second].previous = node
            }
        }
        unvisited.remove(node)
        visited.add(node)
        if (unvisited.isNotEmpty()) {
            unvisited.sortBy { it.distance }
            node = unvisited[0]
        }
    }
    println("Part1: ${endNode.distance}")

    val visualizationOfPath = mutableListOf<MutableList<Char>>()
    for (i in 0 until heightMap.size) {
        visualizationOfPath.add(mutableListOf())
        for (j in 0 until heightMap[i].size) {
            val n = heightMap[i][j]
            if (n.previous != null) {
                visualizationOfPath[i].add(n.height.uppercaseChar())
            } else {
                visualizationOfPath[i].add(n.height)
            }
        }
    }
    for (line in visualizationOfPath) {
        println(String(line.toCharArray()))
    }

    /*
    val visualizationOfPath = mutableListOf<MutableList<Char>>()
    for (i in 0 until heightMap.size) {
        visualizationOfPath.add(mutableListOf())
        for (j in 0 until heightMap[i].size) {
            visualizationOfPath[i].add('.')
        }
    }

     */

    /*
    node = endNode
    do {
        visualizationOfPath[node.coordinates.first][node.coordinates.second] = '*'
        node = node.previous!!
        for (line in visualizationOfPath) {
            println(line.toString())
        }
        println("Next step:")
    } while (node.previous != null)

     */

}

fun getPotentialNodes(
        height: Char,
        coordinates: Pair<Int, Int>,
        heightMap: MutableList<MutableList<Node>>,
        unvisited: MutableList<Node>
): MutableList<Node> {
    return mutableListOf(
            coordinates.first - 1 to coordinates.second,
            coordinates.first + 1 to coordinates.second,
            coordinates.first to coordinates.second - 1,
            coordinates.first to coordinates.second + 1
    )
            .asSequence()
            .filter { it.first >= 0 && it.first < heightMap.size && it.second >= 0 && it.second < heightMap[1].size }
            .map { heightMap[it.first][it.second] }
            .filter { isReachable(it.height, height) }
            .filter { unvisited.contains(it) }
            .toMutableList()
}

private fun isReachable(stepHeight: Char, height: Char) = stepHeight - height <= 1

class Node(var coordinates: Pair<Int, Int>, height: Char) {
    var height = height
        get() = when (field) {
            'E' -> 'z'
            'S' -> 'a'
            else -> field
        }
    var distance: Int = 999999999
    var previous: Node? = null

    constructor(coordinates: Pair<Int, Int>, height: Char, distance: Int, previous: Node?) : this(coordinates, height) {
        this.distance = distance
        this.previous = previous

    }

    fun copy(): Node {
        return Node(this.coordinates, this.height, this.distance, this.previous)
    }
}
