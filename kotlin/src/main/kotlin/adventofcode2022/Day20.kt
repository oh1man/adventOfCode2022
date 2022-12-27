package adventofcode2022

import adventofcode2022.util.runWithStopwatch
import java.io.File
import java.util.*
import kotlin.math.abs


fun main() {
    runWithStopwatch { part1() }
    runWithStopwatch { part2() }
}

private fun part2() {
    TODO("Not yet implemented")
}

private fun part1() {
    val input = File("./input/day20.txt").readLines().map { it.toInt() }
    val map = parse(input)
    var mixKeys = map.keys.toMutableList()
    for ((key, value) in map) {
        val index = mixKeys.indexOf(key)
        // TODO: Think about how to do this generally
        // Create a method that does this. Move an element from index = x to index y
        val leftList = mixKeys.subList(0, newIndex)
        val rightList = mixKeys.subList(newIndex + 1, mixKeys.size)
        leftList.remove(key)
        rightList.remove(key)
        leftList.add(key)
        leftList.addAll(rightList)
        mixKeys = leftList
    }
    // TODO: Create the correct list
    val mix = mixKeys.stream().map { map[it] }.toList()

    // TODO: Find the needed indexes:
    val indexOfZero = mix.indexOf(0)
    var sum = 0
    for (th in listOf(1000, 2000, 3000)) {
        val index = ((indexOfZero + th % size) + size) % size
        val value = mix.get(index)
        sum += value
    }
    println("Part1: ")
/*
    val size = input.size
    val map = createMapOfLinkedList(start, size)
    var end = map[map.keys.last()]
    for ((i, key) in map.keys.withIndex()) {
        val element = map[key]!!
        val steps = element.value % size
        when {
            steps < 0 && steps != abs(size) - 1 -> {
                val target = goBackward(steps, element, end!!)
                collapse(element.before, element.after)
                moveElementBackward(target?.before, element, target, end)
            }
            steps > 0 && steps != abs(size) - 1 -> {
                val target = goForward(steps, element, start)
                collapse(element.before, element.after)
                moveElementForward(target, element, target?.after, start)
            }
        }
        val p = updateStartAndEnd(map)
        start = p.first
        //val mix = createMapOfLinkedList(start, size)
        end = p.second

    }
    val mix = createMapOfLinkedList(start, size)
    val indexOfZero = mix.keys.indexOf(0)
    var sum = 0
    for (th in listOf(1000, 2000, 3000)) {
        val index = ((indexOfZero + th % size) + size) % size
        val value = mix.values.toList().get(index)!!.value
        sum += value
    }*/
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


fun updateStartAndEnd(map: MutableMap<Int, Element?>): Pair<Element, Element> {
    lateinit var start: Element
    lateinit var end: Element
    for (element in map.values) {
        if (element?.before == null) {
            start = element!!
        }
        if (element.after == null) {
            end = element
        }
    }
    return start to end
}

fun moveElementBackward(before: Element?, element: Element, after: Element?, end: Element) {
    var tempBefore = before
    var tempAfter = after
    if (before == null) {
        tempBefore = end
        tempAfter = null
    }
    tempBefore?.after = element
    tempAfter?.before = element
    element.before = tempBefore
    element.after = tempAfter
}

fun moveElementForward(before: Element?, element: Element, after: Element?, start: Element) {
    var tempBefore = before
    var tempAfter = after
    if (after == null) {
        tempBefore = null
        tempAfter = start
    }
    tempBefore?.after = element
    tempAfter?.before = element
    element.before = tempBefore
    element.after = tempAfter
}

fun collapse(before: Element?, after: Element?) {
    before?.after = after
    after?.before = before
}

fun goForward(steps: Int, element: Element, start: Element): Element? {
    var current: Element? = element
    repeat(abs(steps)) {
        current = current?.after
        if (current == null) {
            current = start
        }
    }
    return current
}

fun goBackward(steps: Int, element: Element, end: Element): Element? {
    var current: Element? = element
    repeat(abs(steps)) {
        current = current?.before
        if (current == null) {
            current = end
        }
    }
    return current
}

private fun parse2(input: List<Int>): Element {
    var after: Element? = null
    for (value in input.reversed()) {
        val element = Element(value, after)
        after = element
    }
    val start = after!!
    var current = start.after
    current?.before = start
    do {
        val old = current
        current = current?.after
        current?.before = old
    } while (current?.after != null)
    return start!!
}

fun createMapOfLinkedList(element: Element, size: Int): MutableMap<Int, Element?> {
    var temp: Element = element
    val map = mutableMapOf<Int, Element?>()
    map.put(temp.value, temp)
    do {
        temp = temp.after!!
        var tempValue = temp.value
        while (tempValue in map.keys) {
            tempValue += size
        }
        map.put(tempValue, temp)
    } while (temp.after != null)
    return map
}

class Element(val value: Int, var after: Element?) {
    var before: Element? = null
}

class TempElement(val value: Int, val id: Int)
