package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File


fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    val coordinates = File("./input/day18.txt")
            .readLines()
            .map { line -> line.split(",").map { el -> el.toInt() } }

    val lavaDroplets = coordinates.map { LavaDroplet(it) }
    val maxNumberOfSides = lavaDroplets.size * 6
    val coveredSurfaceArea = calculateSurfaceArea(lavaDroplets)
    val unCoveredSurfaceArea = maxNumberOfSides - coveredSurfaceArea

    // Determine inverse surface.
    val edges = getEdges(coordinates)
    val outerDroplets = createOuterDroplets(coordinates)
    val airDroplets = createInverseDroplets(outerDroplets, lavaDroplets)
    val (airDropletsNonEdges, airDropletsEdges) = filterEdges(airDroplets, edges)

    var uncoveredContainedAir = 0
    for (drop in lavaDroplets) {
        for (air in airDropletsNonEdges) {
            val value = drop.subtract(air).abs().sum()
            if (value == 1) {
                uncoveredContainedAir += 1
            }
        }
    }

    val externalUncoveredArea = unCoveredSurfaceArea - uncoveredContainedAir
    println("Part2: $externalUncoveredArea")
}

fun filterEdges(airDroplets: MutableList<LavaDroplet>, edges: Edges): Pair<MutableList<LavaDroplet>, MutableList<LavaDroplet>> {
    val nonEdges = airDroplets
            .filter { it.coordinates[0] != edges.minX && it.coordinates[0] != edges.maxX }
            .filter { it.coordinates[1] != edges.minY && it.coordinates[1] != edges.maxY }
            .filter { it.coordinates[2] != edges.minZ && it.coordinates[2] != edges.maxZ }
            .toMutableList()

    val edges = createInverseDroplets(airDroplets, nonEdges)
    do {
        val tempEdges = edges.toMutableList()
        val tempNonEdges = nonEdges.toMutableList()
        var containedCounter = 0
        for (droplet in tempNonEdges) {
            for (j in tempEdges) {
                val value = droplet.subtract(j).abs().sum()
                if (value == 1) {
                    containedCounter++
                    nonEdges.remove(droplet)
                    edges.add(droplet)
                }
            }
        }

    } while (containedCounter != 0)
    return nonEdges to edges
}

fun createInverseDroplets(fullSet: List<LavaDroplet>, subSet: List<LavaDroplet>): MutableList<LavaDroplet> {
    val inverseSubSet = emptyList<LavaDroplet>().toMutableList()
    fullSet.forEach { if (it !in subSet) inverseSubSet.add(it) }
    return inverseSubSet
}

private fun calculateSurfaceArea(lavaDroplets: List<LavaDroplet>): Int {
    var coveredSurfaceArea = 0
    for (i in lavaDroplets.indices) {
        val l = lavaDroplets[i]
        var subSurfaceArea = 0
        for (j in i + 1 until lavaDroplets.size) {
            val r = lavaDroplets[j]
            val subtract = l.subtract(r)
            val absSubtract = subtract.abs()
            val value = absSubtract.sum()
            if (value == 1) {
                subSurfaceArea += 2
            }
        }
        coveredSurfaceArea += subSurfaceArea
    }
    return coveredSurfaceArea
}

fun createOuterDroplets(coordinates: List<List<Int>>): List<LavaDroplet> {
    val (minX, maxX, minY, maxY, minZ, maxZ) = getEdges(coordinates)
    val lavaDroplet = emptyList<LavaDroplet>().toMutableList()
    for (x in minX..maxX) {
        for (y in minY..maxY) {
            for (z in minZ..maxZ) {
                lavaDroplet.add(LavaDroplet(listOf(x, y, z)))
            }
        }
    }
    return lavaDroplet
}

fun getEdges(coordinates: List<List<Int>>): Edges {
    val xs = coordinates.sortedBy { it[0] }
    val minX = xs[0][0]
    val maxX = xs.last()[0]
    val ys = coordinates.sortedBy { it[1] }
    val minY = ys[0][1]
    val maxY = ys.last()[1]
    val zs = coordinates.sortedBy { it[2] }
    val minZ = zs[0][2]
    val maxZ = zs.last()[2]
    return Edges(minX, maxX, minY, maxY, minZ, maxZ)
}

data class Edges(val minX: Int, val maxX: Int, val minY: Int, val maxY: Int, val minZ: Int, val maxZ: Int)

private fun part1() {
    val lavaDroplets = File("./input/day18.txt")
            .readLines()
            .map { line -> line.split(",").map { el -> el.toInt() } }
            .map { LavaDroplet(it) }

    val maxNumberOfSides = lavaDroplets.size * 6
    val coveredSurfaceArea = calculateSurfaceArea(lavaDroplets)
    val unCoveredSurfaceArea = maxNumberOfSides - coveredSurfaceArea

    println("Part1: $unCoveredSurfaceArea")
}

class LavaDroplet(val coordinates: List<Int>) {
    fun subtract(lavaDroplet: LavaDroplet): LavaDroplet {
        val subtract = emptyList<Int>().toMutableList()
        for (i in coordinates.indices) {
            subtract.add(coordinates[i] - lavaDroplet.coordinates[i])
        }
        return LavaDroplet(subtract)
    }

    fun sum(): Int {
        return coordinates.sum()
    }

    fun abs(): LavaDroplet {
        val absC =  emptyList<Int>().toMutableList()
        for (i in coordinates) {
            absC.add(kotlin.math.abs(i))
        }
        return LavaDroplet(absC)
    }

    override fun hashCode(): Int {
        return coordinates.hashCode()
    }

    override fun equals(other: Any?): Boolean {
        return hashCode() == other.hashCode()
    }
}
