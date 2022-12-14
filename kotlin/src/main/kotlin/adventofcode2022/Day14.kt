package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part1() {
    val structures = File("./input/day14_test.txt").readLines().map { Structure(it) }
    structures.sortedBy { it. }
    val list = mutableListOf<Char>()

    println("Part1: ")
}

private fun part2() {
    TODO("Not yet implemented")
}

class Structure {

    constructor(input: String) {

    }
}
