package adventofcode2022.util

import adventofcode2022.day01
import java.math.BigDecimal

fun runWithStopwatch(func: () -> Unit) {
    val startTime = System.nanoTime()
    func()
    val endTime = System.nanoTime()
    println("Elapsed time: ${(endTime - startTime).toBigDecimal().divide(BigDecimal.valueOf(1_000_000))} ms")
}