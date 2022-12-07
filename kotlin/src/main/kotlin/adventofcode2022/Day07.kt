package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    val commands = File("./input/day07.txt").readLines()
    val directories = buildDirectoryStructure(commands)
    val rootMemory = directories.values.toList()[0]
    val totalMemory = 70000000
    val spaceNeeded = 30000000
    val deleteSize = spaceNeeded - (totalMemory - rootMemory)
    val directoryToDelete = directories
            .map { it.value }
            .filter { it >= deleteSize }
            .minOf { it }
    println("Director to delete has memory: $directoryToDelete")
}

private fun part1() {
    val commands = File("./input/day07.txt").readLines()
    val directories = buildDirectoryStructure(commands)
    val sortedDescending = directories.map { it.value }.toList().sortedDescending()
    val totalValue = sortedDescending.filter { it <= 100000 }.sum()
    println("Total value: $totalValue")

}

private fun buildDirectoryStructure(commands: List<String>): MutableMap<String, Long> {
    val directories = mutableMapOf<String, Long>()
    var path = ""
    for (command in commands) {
        if ("$ cd " in command) {
            val input = command.split("$ cd ")
            when (input[1]) {
                ".." -> {
                    path = path.substring(0, path.length - path.split("-").last().length - 1)
                }

                else -> {
                    path += "-" + input[1]
                    directories[path] = 0
                }
            }
            continue
        }
        val input = command.split(" ")
        val memory = input[0].toLongOrNull()
        if (memory != null) {
            for (element in directories) {
                if (element.key in path) {
                    directories[element.key] = directories[element.key]!! + memory
                }
            }
        }
    }
    return directories
}
