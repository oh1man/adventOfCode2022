package adventofcode2022.util

import adventofcode2022.day01

fun runWithStopwatch(func: () -> Unit) {
    val startTime = System.nanoTime()
    func()
    val endTime = System.nanoTime()
    println("Elapsed time: ${(endTime - startTime).toDouble() / 1000000000} sec")
}