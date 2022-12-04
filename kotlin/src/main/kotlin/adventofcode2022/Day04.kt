package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import kotlin.math.sign

private val input = File("./input/day04.txt").readLines()

private fun part1() {
    val numberOfOverlapping = input.stream().filter { pair ->
        val sections = pair.split(",", "-")
        val firstSectionPair = sections[0].toDouble() - sections[2].toDouble()
        val secondSectionPair = sections[1].toDouble() - sections[3].toDouble()
        firstSectionPair.sign + secondSectionPair.sign == 0.0 ||
                (firstSectionPair.sign == 0.0 || secondSectionPair.sign == 0.0)
    }.toList().size
    println("Total number of overlapping: $numberOfOverlapping" )
}

private fun part2() {
    val numberOfAllOverlapping = input.stream().filter {
        val sections = it.split(",", "-")
        val firstSectionRange = (sections[0].toInt()..sections[1].toInt()).toList()
        val secondSectionRange = (sections[2].toInt()..sections[3].toInt()).toList()
        firstSectionRange.intersect(secondSectionRange).isNotEmpty()
    }.toList().size
    println("Total number of all overlapping: $numberOfAllOverlapping" )
}

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}