package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import java.lang.IndexOutOfBoundsException

fun main() {
    runWithStopwatch { part1() }
}

private fun part1() {
    val (map, movement) = parse(File("./input/day22.txt").readLines())
    val simulation = Simulation(map, map[0].indexOfFirst { it == '.' }, 0)
    for (move in movement) {
        simulation.executeMove(move)
    }
    println("Part1: ${simulation.getPassword()}")
}

private fun parse(input: List<String>): Pair<List<String>, MutableList<String>> {
    val index = input.indexOf("")
    val map = input.subList(0, index).map { "$it " }
    val movements = input.subList(index + 1, input.size)
    var movement = ""
    for (line in movements) {
        movement += line
    }
    val movementList = mutableListOf("")
    for (char in movement) {
        if (char.isLetter()) {
            movementList.add(char.toString())
            movementList.add("")
        } else {
            movementList[movementList.size - 1] = movementList.last().plus(char)
        }
    }
    return map to movementList
}

private class Simulation(map: List<String>, x: Int, y: Int) {
    val human: Human = Human(map, x = x, y = y)

    fun executeMove(movement: String) {
        if (movement.first().isLetter()) {
            when {
                movement.first() == 'L' -> human.turnLeft()
                movement.first() == 'R' -> human.turnRight()
            }
        } else {
            repeat(movement.toInt()) {
                human.step()
            }
        }
    }

    fun getPassword(): Int {
        val row = 1000 * (human.y + 1)
        val column = 4 * (human.x + 1)
        val facing = human.direction.ordinal
        return row + column + facing
    }

}

class Human(val map: List<String>, var direction: Direction = Direction.RIGHT, var x: Int, var y: Int) {
    fun turnLeft() {
        direction = when (direction) {
            Direction.RIGHT -> Direction.UP
            Direction.UP -> Direction.LEFT
            Direction.LEFT -> Direction.DOWN
            Direction.DOWN -> Direction.RIGHT
        }
    }

    fun turnRight() {
        direction = when (direction) {
            Direction.RIGHT -> Direction.DOWN
            Direction.DOWN -> Direction.LEFT
            Direction.LEFT -> Direction.UP
            Direction.UP -> Direction.RIGHT
        }
    }

    fun step() {
        val pos = nextStep(direction, y, x)
        executeStep(pos)
    }

    private fun executeStep(pos: Pair<Int, Int>) {
        when (canStep(pos)) {
            1 -> {
                y = pos.first
                x = pos.second
            }
            -1 -> executeStep(findOtherSide())
        }
    }

    private fun nextStep(steppingDirection: Direction, currentY: Int, currentX: Int) = when (steppingDirection) {
        Direction.DOWN -> currentY + 1 to currentX
        Direction.UP -> currentY - 1 to currentX
        Direction.LEFT -> currentY to currentX - 1
        Direction.RIGHT -> currentY to currentX + 1
    }

    private fun findOtherSide(): Pair<Int, Int> {
        val reversedDirection = direction.reversed()
        lateinit var oldPos: Pair<Int, Int>
        var newPos = y to x
        do {
            oldPos = newPos
            newPos = nextStep(reversedDirection, newPos.first, newPos.second)
        } while ((canStep(newPos) != -1))
        return oldPos
    }

    private fun canStep(pos: Pair<Int, Int>): Int {
        val char: Char
        try {
            char = map[pos.first][pos.second]
        } catch (e: IndexOutOfBoundsException) {
            return -1
        }
        return when (char) {
            '.' -> 1
            '#' -> 0
            ' ' -> -1
            else -> error("Strange input!")
        }
    }

    enum class Direction(i: Int) {
        RIGHT(0),
        LEFT(2),
        UP(3),
        DOWN(1);

        fun reversed(): Direction {
            return when (this) {
                RIGHT -> LEFT
                LEFT -> RIGHT
                UP -> DOWN
                DOWN -> UP
            }
        }
    }
}
