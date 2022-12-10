package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part1() {
    val commands = File("./input/day10.txt").readLines()
    val cycles = getCycles(commands)
    var signalStrength = mutableListOf<Int>()
    for (i in 20..220 step 40) {
        signalStrength.add(cycles[i - 1] * i)
    }
    println("Part1: ${signalStrength.sum()}")
}

private fun getCycles(commands: List<String>): MutableList<Int> {
    var x = 1
    val cycles = mutableListOf(x)
    for (command in commands) {
        val input = command.split(" ")
        when (input[0]) {
            "noop" -> cycles.add(x)
            "addx" -> {
                cycles.add(x)
                x += input[1].toInt()
                cycles.add(x)
            }

            else -> error("Strange input")
        }
    }
    return cycles
}

private fun part2() {
    val commands = File("./input/day10.txt").readLines()
    val cycles = getCycles(commands)
    var render = ""
    for (i in 0 until cycles.size - 1) {
        val midpoint = cycles[i]
        val sprite = listOf(midpoint - 1, midpoint, midpoint + 1)
        val index = i % 40
        render += if (sprite.contains(index)) {
            "█"
        } else {
            "░"
        }
    }
    val renderList = mutableListOf<String>()
    for (i in 0 until cycles.size - 1 step 40) {
        renderList.add(render.slice(i.. i + 39))
    }
    println("Part2:")
    for (line in renderList) {
        println(line)
    }
}

