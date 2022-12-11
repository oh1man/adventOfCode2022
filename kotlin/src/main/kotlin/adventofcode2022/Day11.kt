package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import kotlin.math.floor

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

// TODO: This is solved, just a problem with the type. When long gets to big in kotlin it becomes negative!

private fun part1() {
    val monkeyInputs = File("./input/day11_test.txt").readLines().chunked(7)
    val monkeys = parseMonkeys(monkeyInputs)
    for (monkey in monkeys) {
        monkey.worryHandling = { floor((it / 3).toDouble()).toLong() }
    }
    repeat(20) {
        monkeys.forEach { it.executeMonkeyBusiness() }
    }
    val monkeyInteractions = monkeys.map { it.inspections }.sortedDescending()
    val monkeyBusiness = monkeyInteractions[0] * monkeyInteractions[1]
    println("Part1: $monkeyBusiness")

}

private fun part2() {
    val monkeyInputs = File("./input/day11_test.txt").readLines().chunked(7)
    val monkeys = parseMonkeys(monkeyInputs)

    var commonDivider = 1L
    for (monkey in monkeys) {
        commonDivider *= monkey.test
    }

    for (monkey in monkeys) {
        monkey.worryHandling = fun(item: Long): Long {
            return if (item % commonDivider == 0L) {
                item % commonDivider
            } else {
                item
            }
        }
    }
    repeat(10_000) {
        monkeys.forEach { it.executeMonkeyBusiness() }
    }
    val monkeyInteractions = monkeys.map { it.inspections }.sortedDescending()
    val monkeyBusiness = monkeyInteractions[0] * monkeyInteractions[1]
    println("Part2: $monkeyBusiness")
}

private fun List<Int>.product(): Int {
    var product = 0
    this.forEach {
        product *= it
    }
    return product
}


private fun parseMonkeys(monkeyInputs: List<List<String>>): MutableList<Monkey> {
    val monkeys = mutableListOf<Monkey>()
    for (monkeyInput in monkeyInputs) {
        val items = monkeyInput[1].split("Starting items: ")[1].split(", ").map { it.toLong() }.toMutableList()
        val operation = createOperation(monkeyInput[2].split(" = ")[1].split(" "))
        val test = monkeyInput[3].split(" by ")[1].toLong()
        val throwToIfTrue = monkeyInput[4].split(" monkey ")[1].toInt()
        val throwIfFalse = monkeyInput[5].split(" monkey ")[1].toInt()
        monkeys.add(Monkey(items, operation, test, throwToIfTrue, throwIfFalse, monkeys))
    }
    return monkeys
}

fun createOperation(split: List<String>): (Long) -> Long {
    return when (split[1]) {
        "*" -> { old: Long -> old * (split[2].toLongOrNull() ?: old) }
        "+" -> { old: Long  -> old + (split[2].toLongOrNull() ?: old) }
        else -> error("Strange input")
    }
}

class Monkey(
        private var items: MutableList<Long>,
        private val operation: (Long) -> Long,
        val test: Long,
        private val throwToIfTrue: Int,
        private val throwToIfFalse: Int,
        private val family: List<Monkey>
) {
    var inspections: Int = 0
    var worryHandling: (Long) -> Long = { it }

    fun executeMonkeyBusiness() {
        for (item in items) {
            var newItem = inspect(item)
            newItem = worryHandling(newItem)
            if (newItem % test == 0L) {
                family[throwToIfTrue].items.add(newItem)
            } else {
                family[throwToIfFalse].items.add(newItem)
            }
        }
        this.items = mutableListOf()
    }

    private fun inspect(item: Long): Long {
        inspections++
        return operation(item)
    }
}
