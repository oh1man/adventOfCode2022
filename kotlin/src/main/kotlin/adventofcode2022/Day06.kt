package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File

private var input = File("./input/day06.txt")

private fun part1() {
    val index = getNumberOfIndexesPassedBeforeUniqueSequence(4)
    println("Number of character before the first marker: " + (index + 1))
}

private fun part2() {
    val numberOfCharacters = getNumberOfIndexesPassedBeforeUniqueSequence(14)
    println("Number of character before the first word: " + (numberOfCharacters + 1))
}

private fun getNumberOfIndexesPassedBeforeUniqueSequence(numberOfChar: Int): Int {
    val inputStream = input.bufferedReader()
    val queue = Queue()
    var index = 0
    while (inputStream.ready()) {
        val char = inputStream.read()
        queue.enqueue(char.toChar())
        if (queue.size() > numberOfChar) {
            queue.dequeue()
            if (queue.isUnique()) {
                break
            }
        }
        index++
    }
    return index
}

private class Queue {
    val queue: ArrayList<Char> = arrayListOf()

    fun enqueue(char: Char) {
        queue.add(char)
    }

    fun dequeue() {
        queue.removeFirst()
    }

    fun size(): Int {
        return queue.size
    }

    fun isUnique(): Boolean {
        return queue == queue.distinct()
    }
}

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}