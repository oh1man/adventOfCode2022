package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    TODO("Not yet implemented")
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

    var visibleTrees: Int = 0
    for (i in trees.indices) {
        for (j in trees[i].indices) {
            val tree = trees[i][j]
            val leftTreeLine = trees[i].slice(0 until i)
            val rightTreeLine = trees[i].slice(i + 1 until trees[i].size)
            val verticalLine = trees.map { it[j] }
            val bottomTreeLine = verticalLine.slice(j + 1 until verticalLine.size)
            val topTreeLine = verticalLine.slice(0 until j)
            val visibleFromLeft = isVisible(leftTreeLine, tree)
            val visibleFromRight = isVisible(rightTreeLine, tree)
            val visibleFromTop = isVisible(topTreeLine, tree)
            val visibleFromBottom = isVisible(bottomTreeLine, tree)
            if (visibleFromTop || visibleFromBottom || visibleFromLeft || visibleFromRight) {
                visibleTrees++
            }
        }
    }
    println("number of trees visible is: $visibleTrees")
}

private fun isVisible(treeLine: List<Int>, tree: Int) = treeLine.all { it < tree }
