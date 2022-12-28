package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import kotlin.math.abs


fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    val decryptionKey = 811589153
    val input = File("./input/day20.txt").readLines().map { it.toLong() * decryptionKey }
    var size = input.size - 1
    val map = parseLong(input)
    var mixKeys = map.keys.toMutableList()
    repeat(10) {
        for ((key, value) in map) {
            val index = mixKeys.indexOf(key)
            val newIndex = ((index + value % size) + size) % size

            if (index == newIndex.toInt()) {
                continue
            }
            mixKeys = when {
                value > 0 -> moveElementRight(mixKeys, key, newIndex.toInt())
                value < 0 -> moveElementLeft(mixKeys, key, newIndex.toInt())
                else -> error("Strange input!")
            }
        }
    }
    val mix = mixKeys.stream().map { map[it] }.toList()

    val indexOfZero = mix.indexOf(0)
    size = mix.size
    var sum: Long = 0
    for (th in listOf(1000, 2000, 3000)) {
        val index = ((indexOfZero + th) % size)
        val value = mix.get(index)!!
        sum += value
    }
    println("Part2: $sum")
}

private fun part1() {
    val input = File("./input/day20.txt").readLines().map { it.toInt() }
    var size = input.size - 1
    val map = parse(input)
    var mixKeys = map.keys.toMutableList()
    for ((key, value) in map) {
        val index = mixKeys.indexOf(key)
        val newIndex = ((index + value % size) + size) % size

        if (index == newIndex) {
            continue
        }
        mixKeys = when {
            value > 0 -> moveElementRight(mixKeys, key, newIndex.toInt())
            value < 0 -> moveElementLeft(mixKeys, key, newIndex)
            else -> error("Strange input!")
        }
    }
    val mix = mixKeys.stream().map { map[it] }.toList()

    val indexOfZero = mix.indexOf(0)
    size = mix.size
    var sum = 0
    for (th in listOf(1000, 2000, 3000)) {
        val index = ((indexOfZero + th) % size)
        val value = mix.get(index)!!
        sum += value
    }
    println("Part1: $sum")
}

private fun <T> moveElementRight(
        mixKeys: MutableList<T>,
        key: T,
        newIndex: Int
): MutableList<T> {
    val temp = mixKeys.toMutableList()
    temp.remove(key)
    val leftList = temp.subList(0, newIndex).toMutableList()
    val rightList = temp.subList(newIndex, temp.size).toMutableList()
    leftList.add(key)
    return (leftList + rightList).toMutableList()
}

private fun <T> moveElementLeft(
        mixKeys: MutableList<T>,
        key: T,
        newIndex: Int
): MutableList<T> {
    val temp = mixKeys.toMutableList()
    temp.remove(key)
    val leftIndex = newIndex
    val leftList = temp.subList(0, leftIndex).toMutableList()
    val rightList = temp.subList(leftIndex, temp.size).toMutableList()
    leftList.add(key)
    return (leftList + rightList).toMutableList()
}

private fun parse(input: List<Int>): Map<Int, Int> {
    val size = input.size
    val map = mutableMapOf<Int, Int>()
    input.forEach {
        var temp = it
        while (temp in map.keys) {
            temp += size
        }
        map[temp] = it
    }
    return map.toMap()
}

private fun parseLong(input: List<Long>): Map<Long, Long> {
    val size = input.size
    val map = mutableMapOf<Long, Long>()
    input.forEach {
        var temp = it
        while (temp in map.keys) {
            temp += size
        }
        map[temp] = it
    }
    return map.toMap()
}