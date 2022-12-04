package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

private val input = File("./input/day03.txt").readLines()

private fun part1() {
    var priorityPoints = 0
    for (line in input) {
        val (firstComponent, secondComponent) = getCompartments(line)
        for (i in firstComponent.distinct()) {
            for (j in secondComponent.distinct()) {
                if (i == j) {
                    priorityPoints += j.toPriority()
                    break
                }
            }
        }
    }
    println("Total priority: $priorityPoints")
}

private fun part2() {
    var priorityPoints = 0
    for (index in 0 until(input.size / 3)) {
        val group = input.slice((index * 3) until (index + 1) * 3)
        for (i in group[0].toCharArray().distinct()) {
            for (j in group[1].toCharArray().distinct()) {
                if (i == j) {
                    for (k in group[2].toCharArray().distinct()) {
                        if (j == k) {
                            priorityPoints += k.toPriority()
                            break
                        }
                    }
                }
            }
        }
    }
    println("Total priority: $priorityPoints")
}

// NOTE: Extension function give good readability
private fun Char.toPriority(): Int {
    return this.lowercaseChar().code - 'a'.code + 1 + 26 * (if (this.isUpperCase()) 1 else 0)
}

// NOTE: Deconstruction give good readability
private fun getCompartments(line: String): Pair<CharArray, CharArray> {
    val length = line.length
    return Pair(
            line.substring(0, length / 2).toCharArray(),
            line.substring(length / 2, length).toCharArray()
    )
}


fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}