package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
}

private fun part1() {
    val lines = File("./input/day12_test.txt").readLines()


    val heightMap = mutableListOf<MutableList<Node>>()
    lateinit var startNode: Node
    lateinit var endNode: Node
    val visited = mutableListOf<Node>()
    val unvisited = mutableListOf<Node>()
    for (i in lines.indices) {
        heightMap.add(i, mutableListOf())
        for (j in lines[i].indices) {
            val height = lines[i][j].toString()
            val node = Node(i to j, height)
            heightMap[i].add(j, node)
            when (height) {
                "S" -> startNode = node
                "E" -> endNode = node
            }
            unvisited.add(node)
        }
    }

    var node: Node = startNode
    repeat (unvisited.size) {
        getPotentialNodes(node.height, node.coordinates, heightMap).forEach {
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
    print("Part1: ${endNode.distance}")
}

fun getPotentialNodes(
    height: String,
    coordinates: Pair<Int, Int>,
    heightMap: MutableList<MutableList<Node>>
): MutableList<Node> {
    return mutableListOf(
        coordinates.first - 1 to coordinates.second,
        coordinates.first + 1 to coordinates.second,
        coordinates.first to coordinates.second - 1,
        coordinates.first to coordinates.second + 1
    )
        .filter { it.first < 0 || it.second < 0 }
        .map { heightMap[it.first][it.second] }
        .filter { it.height == "a" } // TODO: Update height logic the I think we are done
        .toMutableList()
}

class Node(val coordinates: Pair<Int, Int>, val height: String) {
    var distance: Int = 10000000
    var previous: Node? = null
}
