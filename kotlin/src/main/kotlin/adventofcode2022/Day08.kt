package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    val input = File("./input/day08.txt")
    val trees = input.readLines()
        .stream()
        .map { line ->
            line.split("")
                .filter { it.toIntOrNull() != null }
                .map { it.toInt() }
        }
        .toList()

    var scenicScrores = mutableListOf<Long>()
    for (i in trees.indices) {
        for (j in trees[i].indices) {
            val tree = trees[i][j]
            val scenicScoreLeft = getDirectionalScenicScore(trees[i].slice(0 until j), tree)
            val scenicScoreRight = getDirectionalScenicScore(trees[i].slice(j + 1 until trees[i].size), tree, false)
            val verticalLine = trees.map { it[j] }
            val scenicScoreTop = getDirectionalScenicScore(verticalLine.slice(0 until i), tree)
            val scenicScoreBottom = getDirectionalScenicScore(verticalLine.slice(i + 1 until verticalLine.size), tree, false)
            val scenicScore = scenicScoreLeft * scenicScoreRight * scenicScoreTop * scenicScoreBottom
            scenicScrores.add(scenicScore)
        }
    }
    scenicScrores.sortDescending()
    println("The highest scenic score possible is: ${scenicScrores[0]}")
}

private fun getDirectionalScenicScore(treeLine: List<Int>, tree: Int, right: Boolean = true): Long {
    var tempTreeLine = treeLine
    if (right) {
        tempTreeLine = treeLine.reversed()
    }
    var directionalScenicScore = 0L
    for (adjTree in treeLine) {
        directionalScenicScore++
        if (adjTree >= tree) {
            break
        }
    }
    return directionalScenicScore
}

private fun part1() {
    val input = File("./input/day08.txt")
    val trees = input.readLines()
            .stream()
            .map { line ->
                line.split("")
                        .filter { it.toIntOrNull() != null }
                        .map { it.toInt() }
            }
            .toList()

    var visibleTrees = 0
    for (i in trees.indices) {
        for (j in trees[i].indices) {
            val tree = trees[i][j]
            val visibleFromLeft = isVisible(trees[i].slice(0 until j), tree)
            val visibleFromRight = isVisible(trees[i].slice(j + 1 until trees[i].size), tree)
            val verticalLine = trees.map { it[j] }
            val visibleFromTop = isVisible(verticalLine.slice(0 until i), tree)
            val visibleFromBottom = isVisible(verticalLine.slice(i + 1 until verticalLine.size), tree)
            if (visibleFromTop || visibleFromBottom || visibleFromLeft || visibleFromRight) {
                visibleTrees++
            }
        }
    }
    println("Number of trees visible is: $visibleTrees")
}

private fun isVisible(treeLine: List<Int>, tree: Int) = treeLine.all { it < tree }
