import adventofcode2022.util.runWithStopwatch
import java.io.File
import java.lang.Exception
import java.lang.Math.abs
import kotlin.math.max
import kotlin.math.min

fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part1() {
    // Create scan of structures
    val structures = File("./input/day14.txt").readLines().map { Structure(it) }
    val coordinates = structures.flatMap { it.coordinates }
    val sortedX = coordinates.map { it.first }.distinct().sortedDescending()
    val sortedY = coordinates.map { it.second }.distinct().sorted()
    val norm = sortedX.last()
    val m = abs(sortedX.first() - sortedX.last()) + 1 // Decide these
    val n = sortedY.last() + 1
    val scan = MutableList(n) { MutableList(m) { '.' } }
    for (structure in structures) {
        for (p in structure.coordinates) {
            scan[p.second][p.first - norm] = '#'
        }
    }
    // Simulate
    val simulator = Simulator(scan, 0 to 500, norm)
    while (simulator.isRunning()) {
        simulator.drop()
    }
    scan.forEach { println(it.joinToString("")) }
    println("Part1: ${simulator.numberOfSand}")
}

class Structure(input: String) {
    val coordinates: List<Pair<Int, Int>>

    init {
        this.coordinates = parse(input)
    }

    private fun parse(input: String): List<Pair<Int, Int>> {
        val turns = input.split(" -> ").map {
            val split = it.split(",")
            split.first().toInt() to split.last().toInt()
        }.toList()
        var s = turns[0]
        val coordinates = mutableListOf(s)
        for (i in 1 until turns.size) {
            val t = turns[i]
            IntRange(min(s.first, t.first), max(s.first, t.first)).forEach {
                coordinates.add(it to s.second)
            }
            IntRange(min(s.second, t.second), max(s.second, t.second)).forEach {
                coordinates.add(s.first to it)
            }
            s = t.copy()
        }
        return coordinates.distinct()
    }
}

class Simulator {
    private var width: Int
    val scan: MutableList<MutableList<Char>>
    val start: Pair<Int, Int>
    var numberOfSand: Int = 0
    var run = true
    val norm: Int
    constructor(scan: MutableList<MutableList<Char>>, start: Pair<Int, Int>, norm: Int, width: Int = 0) {
        this.scan = scan
        this.start = start
        this.norm = norm
        this.width = width
    }

    fun drop() {
        var p = start
        if (scan[p.first][p.second - norm] == 'o') {
            run = false
            return
        }
        var atRest = false
        while (!atRest) {
            lateinit var newP: Pair<Int, Int>
            try {
                newP = step(p)
            } catch (e: Exception) {
                run = false
                break
            }
            if (newP == p) {
                scan[p.first][width + p.second - norm] = 'o'
                atRest = true
                numberOfSand++
            } else {
                p = newP
            }
        }
    }

    private fun step(p: Pair<Int, Int>): Pair<Int, Int> {
        return when {
            freeBelow(p) -> p.first + 1 to p.second
            freeLeft(p) -> p.first + 1 to p.second - 1
            freeRight(p) -> p.first + 1 to p.second + 1
            else -> p
        }
    }

    private fun freeBelow(p: Pair<Int, Int>): Boolean {
        return scan[p.first + 1][p.second - norm] == '.'
    }

    private fun freeLeft(p: Pair<Int, Int>): Boolean {
        return scan[p.first + 1][(p.second - 1) - norm] == '.'
    }

    private fun freeRight(p: Pair<Int, Int>): Boolean {
        return scan[p.first + 1][(p.second + 1) - norm] == '.'
    }


    fun isRunning(): Boolean {
        return run
    }
}

private fun part2() {
    // Create scan of structures
    val structures = File("./input/day14.txt").readLines().map { Structure(it) }
    val coordinates = structures.flatMap { it.coordinates }
    val sortedX = coordinates.map { it.first }.distinct().sortedDescending()
    val sortedY = coordinates.map { it.second }.distinct().sorted()
    val width = 200
    val norm_x = sortedX.last()
    val height = 2
    val m = abs(sortedX.first() - sortedX.last()) + 1 + 2*width // Decide these
    val n = sortedY.last() + 1 + height
    val scan = MutableList(n) { MutableList(m) { '.' } }
    for (structure in structures) {
        for (p in structure.coordinates) {
            scan[p.second][width + p.first - norm_x] = '#'
        }
    }

    // Add rock floor
    for (i in scan[0].indices) {
        scan[n - 1][i] = '#'
    }

    scan.forEach { println(it.joinToString("")) }

    // Simulate
    val simulator = Simulator(scan, 0 to 500 + width, norm_x)
    while (simulator.isRunning()) {
        simulator.drop()
    }
    scan.forEach { println(it.joinToString("")) }
    println("Part2: ${simulator.numberOfSand}")
}
