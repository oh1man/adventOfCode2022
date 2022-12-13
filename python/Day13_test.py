

def part1():
    i = 0  # line number
    pair = 1
    total = 0
    fileinput = open("../input/day13.txt", "r").readlines()

    # Return 1 if the lists are in the right oder,
    #       -1 if the lists are in the wrong order,
    #        0 if we cannot decide in ths current pass.
    def ordered(L, R):
        for i in range(0, len(L)):
            if i >= len(R):
                return -1
            if type(L[i]) is int and type(R[i]) is int:
                if L[i] < R[i]:
                    return 1
                elif L[i] > R[i]:
                    return -1
            elif type(L[i]) is list and type(R[i]) is list:
                j = ordered(L[i], R[i])
                if j != 0:
                    return j
            elif type(L[i]) is list:
                j = ordered(L[i], [R[i]])
                if j != 0:
                    return j
            elif type(R[i]) is list:
                j = ordered([L[i]], R[i])
                if j != 0:
                    return j

        # If we reach this spot, we ran out of items in the left list.
        if len(L) == len(R):
            return 0
        return 1


    for line in fileinput:
        i += 1
        if i % 3 == 1:
            left = eval(line.rstrip())
            continue
        elif i % 3 == 2:
            right = eval(line.rstrip())
        else:
            pair += 1
            continue

        if ordered(left, right) > 0:
            total += pair

    print(total)

if __name__ == '__main__':
    part1()