package adventofcode2022

import adventofcode2022.Hand.Companion.getWinningHand
import java.io.File

fun day02() {
    val file = File("./input/day02.txt")
    val wrongHands = file.readLines().stream()
            .map {
                val split = it.split(" ")
                Pair(Hand.from(split[0]), Hand.from(split[1]))
            }.toList()
    var wrongPoints = 0
    for (hand in wrongHands) {
        wrongPoints += play(hand)
    }
    println("Total points from wrong strategy: $wrongPoints")

    val correctHands = file.readLines().stream().map {
        val split = it.split(" ")
        Pair(Hand.from(split[0]), convertToCorrectHand(split))
    }.toList()
    var correctPoints = 0
    for (hand in correctHands) {
        correctPoints += play(hand)
    }
    println("Total points from correct strategy: $correctPoints")
}

fun convertToCorrectHand(strategy: List<String>): Hand {
    val goForStrategy = strategy[1]
    val opponentHand = Hand.from(strategy[0])
    if (goForStrategy == "Z") {
        return getWinningHand(opponentHand)
    }
    if (goForStrategy == "Y") {
        return opponentHand
    }
    return getWinningHand(getWinningHand(opponentHand))
}

enum class Hand {
    ROCK, PAPER, SCISSOR, NONE;
    companion object {
        fun from(code: String): Hand {
            return when(code) {
                "X", "A" -> ROCK
                "Y", "B" -> PAPER
                "Z", "C" -> SCISSOR
                else -> NONE
            }
        }

        fun getWinningHand(hand: Hand): Hand {
            return when (hand) {
                ROCK -> PAPER
                PAPER -> SCISSOR
                SCISSOR -> ROCK
                else -> NONE
            }
        }
    }
}

fun play(hands: Pair<Hand, Hand>): Int {
    if (isWinningHand(hands)) {
        return getPointsForResult(left = false, right = true) + getPointForHand(hands.second)
    }
    if (isDrawingHand(hands)) {
        return getPointsForResult(left = true, right = true) + getPointForHand(hands.second)
    }
    return 0 + getPointForHand(hands.second)
}

private fun isWinningHand(hands: Pair<Hand, Hand>) = listOf(
        Pair(Hand.SCISSOR, Hand.ROCK),
        Pair(Hand.ROCK, Hand.PAPER),
        Pair(Hand.PAPER, Hand.SCISSOR)
).contains(hands)

fun isDrawingHand(hands: Pair<Hand, Hand>) = listOf(
        Pair(Hand.ROCK, Hand.ROCK),
        Pair(Hand.PAPER, Hand.PAPER),
        Pair(Hand.SCISSOR, Hand.SCISSOR)
).contains(hands)

fun getPointsForResult(left: Boolean, right: Boolean): Int {
    if (right && !left) {
        return 6
    }
    if (right == left) {
        return 3
    }
    return 0
}

fun getPointForHand(hand: Hand): Int {
    return when(hand) {
        Hand.ROCK -> 1
        Hand.PAPER -> 2
        Hand.SCISSOR -> 3
        else -> 0
    }
}

fun main() {
    val startTime = System.nanoTime()
    day02()
    val endTime = System.nanoTime()
    println("Elapsed time: ${(endTime - startTime).toDouble() / 1000000000} sec")
}