package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

private val input = File("./input/day05.txt").readLines()


private fun part1() {
    val (stacks, commands) = parseInput(input)
    executeCommands(stacks, commands, crateMover9000)
    println(getTopCrates(stacks))
}

private fun part2() {
    val (stacks, commands) = parseInput(input)
    executeCommands(stacks, commands, crateMover9001)
    println(getTopCrates(stacks))
}

fun getTopCrates(stacks: List<ArrayList<Char>>): String {
    var topCrates = ""
    for (i in stacks.indices) {
        topCrates += stacks[i][stacks[i].lastIndex]
    }
    return topCrates
}

fun parseInput(input: List<String>): Pair<List<ArrayList<Char>>, List<String>> {
    val cutoffIndex = input.indexOf("")
    return parseStacks(input.subList(0, cutoffIndex - 1)) to input.subList(cutoffIndex + 1, input.size)
}

fun parseStacks(subList: List<String>): List<ArrayList<Char>> {
    val stacks = List(9) { ArrayList<Char>() }
    for (line in subList.reversed()) {
        for ((stackIndex, elementIndex) in (1 until line.length step 4).withIndex()) {
            val element = line[elementIndex]
            if (element != ' ') {
                stacks[stackIndex].add(element)
            }
        }
    }
    return stacks
}

fun executeCommands(stacks: List<ArrayList<Char>>, commands: List<String>, mover: (stacks: List<ArrayList<Char>>, move: Int, from: Int, to: Int) -> Unit) {
    for (command in commands) {
        var startIndex = command.indexOf("move ") + "move ".length
        var endIndex = command.indexOf(" from ")
        val move = command.substring(startIndex, endIndex).toInt()
        startIndex = endIndex + " from ".length
        endIndex = command.indexOf(" to ")
        val from = command.substring(startIndex, endIndex).toInt()
        startIndex = endIndex + " to ".length
        val to = command.substring(startIndex).toInt()
        mover(stacks, move, from, to)
    }
}

val crateMover9000 = fun (stacks: List<ArrayList<Char>>, move: Int, from: Int, to: Int) {
    val fromIndex = from - 1
    val toIndex = to - 1
    for (i in 0 until move) {
        val crate = stacks[fromIndex][stacks[fromIndex].lastIndex]
        stacks[toIndex].add(crate)
        stacks[fromIndex].removeAt(stacks[fromIndex].lastIndex)
    }
}

val crateMover9001 = fun (stacks: List<ArrayList<Char>>, move: Int, from: Int, to: Int) {
    val fromIndex = from - 1
    val toIndex = to - 1
    val movingCrates = arrayListOf<Char>()
    for (i in 0 until move) {
        movingCrates.add(stacks[fromIndex][stacks[fromIndex].lastIndex])
        stacks[fromIndex].removeAt(stacks[fromIndex].lastIndex)
    }
    for (crate in movingCrates.reversed()) {
        stacks[toIndex].add(crate)
    }
}

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}