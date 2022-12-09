package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import kotlin.math.abs

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part1() {
    val commands = File("./input/day09.txt").readLines()
    val rope = Rope(1)
    val tailLocationHistory = execute(commands, rope)
    println("Part1: ${tailLocationHistory.size}")
}

private fun part2() {
    val commands = File("./input/day09.txt").readLines()
    val rope = Rope(9)
    val tailLocationHistory = execute(commands, rope)
    println("Part2: ${tailLocationHistory.size}")
}

private fun execute(commands: List<String>, rope: Rope, ): MutableSet<Pair<Int, Int>> {
    val tailLocationHistory = mutableSetOf<Pair<Int, Int>>()
    for (commandText in commands) {
        val command = commandText.split(" ")
        for (ignore in 0 until command[1].toInt()) {
            when (command[0]) {
                "U" -> rope.moveUp()
                "D" -> rope.moveDown()
                "L" -> rope.moveLeft()
                "R" -> rope.moveRight()
                else -> error("Strange input!")
            }
            tailLocationHistory.add(rope.last())
        }
    }
    return tailLocationHistory
}

class Rope(size: Int) {
    private var head: Pair<Int, Int> = 0 to 0
    private var tail: Array<Pair<Int, Int>>

    init {
        tail = Array(size) { 0 to 0 }
    }

    fun moveRight() {
        val x = head.first + 1
        val y = head.second
        head = x to y
        updateTail()
    }

    fun moveLeft() {
        val x = head.first - 1
        val y = head.second
        head = x to y
        updateTail()
    }

    fun moveUp() {
        val x = head.first
        val y = head.second + 1
        head = x to y
        updateTail()
    }

    fun moveDown() {
        val x = head.first
        val y = head.second - 1
        head = x to y
        updateTail()
    }

    fun last(): Pair<Int, Int> {
        return tail.last()
    }

    private fun updateTail() {
        var tempHead = head
        for (i in tail.indices) {
            val (dx, dy) = getDiff(tempHead, tail[i])
            if (!isAdjacent(dx, dy)) {
                tail[i] = tail[i].first + sign(dx) to tail[i].second + sign(dy)
            }
            tempHead = tail[i]
        }
    }

    private fun getDiff(first: Pair<Int, Int>, second: Pair<Int, Int>): Pair<Int, Int> {
        val dx = first.first - second.first
        val dy = first.second - second.second
        return dx to dy
    }

    private fun sign(value: Int): Int {
        return if (value > 0) {
            1
        } else if (value < 0) {
            -1
        } else {
            0
        }
    }

    private fun isAdjacent(dx: Int, dy: Int): Boolean {
        return abs(dx) <= 1 && abs(dy) <= 1
    }
}

