import random


class SudokuPuzzle:

    def __init__(self, mode) -> None:
        self.__puz = [[0] * 9 for i in range(9)]
        self.__puzSolution = [[0] * 9 for i in range(9)]

        self.__row = [{j: False for j in range(1, 10)} for i in range(9)]
        self.__col = [{j: False for j in range(1, 10)} for i in range(9)]
        self.__block = [{j: False for j in range(1, 10)} for i in range(9)]

        self.genSolution(0, 0)
        self.reset()
        self.genPuzzle(mode)

    def getPuzzle(self):
        tmp = [[0] * 9 for i in range(9)]
        self.copy(tmp, self.__puz)
        return tmp

    def getSolution(self):
        tmp = [[0] * 9 for i in range(9)]
        self.copy(tmp, self.__puzSolution)
        return tmp

    def reset(self):
        """Reset the row, col and block dict to empty dict"""
        self.__row = [{j: False for j in range(1, 10)} for i in range(9)]
        self.__col = [{j: False for j in range(1, 10)} for i in range(9)]
        self.__block = [{j: False for j in range(1, 10)} for i in range(9)]

    def copy(self, list1, list2):
        for y in range(9):
            for x in range(9):
                list1[y][x] = list2[y][x]

    def getBlockIndex(self, x, y):
        """Find the index of 3x3 block corresponding to (x, y)"""
        if 0 <= x < 3:
            if 0 <= y < 3:
                return 0
            elif 3 <= y < 6:
                return 3
            else:
                return 6
        if 3 <= x < 6:
            if 0 <= y < 3:
                return 1
            elif 3 <= y < 6:
                return 4
            else:
                return 7
        if 6 <= x < 9:
            if 0 <= y < 3:
                return 2
            elif 3 <= y < 6:
                return 5
            else:
                return 8

    def getIntersection(self, row, col, block):
        """Find the intersection between row, column and block lists"""
        return {
            item: True for item in row.keys() if not (row[item] or col[item] or block[item])
        }

    def genSolution(self, x, y):
        """Generate a sodoku solution"""
        if y == 9:
            return True
        elif x == 9:
            return self.genSolution(0, y + 1)

        choices = self.getIntersection(
            self.__row[y], self.__col[x], self.__block[self.getBlockIndex(x, y)])

        while len(choices) > 0:
            self.__puzSolution[y][x] = random.choice(list(choices.keys()))
            self.__row[y][self.__puzSolution[y][x]] = self.__col[x][self.__puzSolution[y][x]
                                                                    ] = self.__block[self.getBlockIndex(x, y)][self.__puzSolution[y][x]] = True
            if self.genSolution(x + 1, y):
                return True

            choices.pop(self.__puzSolution[y][x], None)

            self.__row[y][self.__puzSolution[y][x]
                          ] = self.__col[x][self.__puzSolution[y][x]] = False
            self.__block[self.getBlockIndex(
                x, y)][self.__puzSolution[y][x]] = False
            self.__puzSolution[y][x] = 0
        return False

    def genPuzzle(self, mode: str):
        """Generate the puzzle"""

        self.copy(self.__puz, self.__puzSolution)

        if mode == "h":
            k = 60
        elif mode == "m":
            k = 52
        else:
            k = 44

        possible_coor = {}

        for y in range(9):
            for x in range(9):
                possible_coor[(x, y)] = True

        while k > 0:
            k -= 1

            x, y = random.choice(list(possible_coor.keys()))
            self.__puz[y][x] = 0
            possible_coor.pop((x, y), None)
