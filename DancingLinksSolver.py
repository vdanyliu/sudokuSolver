import numpy

class DancingLinksSolver():
    class Node():
        def __init__(self, data, up=None, down=None, left=None, right=None, upHeader=None, leftHeader=None):
            self.data = data
            self.up = up
            self.down = down
            self.left = left
            self.right = right
            self.upHeader = upHeader
            self.leftHeader = leftHeader

    def __init__(self, matrix):
        self.xListHeader = self.Node("Head")
        self.create_list_header(
            matrix.shape)  # Говнокод тот еще(хоть рабочий), но за то есть "оглавление" строк и столбцов
        print("create list headers")
        self.create_links_by_matrix(matrix)  # Конвертируем значения матрицы в связанный список (тоже говнокод)
        print("create links")
        self.solutionList = []
        # self.__debug_cheker()

    def correct_start_condition_in_list(self, conditionList):
        # Return 0 if initial conditions are valid
        count = len(conditionList)
        list = self.xListHeader.down
        while list != list.upHeader:
            if list.data in conditionList:
                self.crossDelInList(list)
                count -= 1
            list = list.down
        return count

    buff = []

    def solution(self):
        self.crossDelRestBuff = []
        # self.solve()
        for x in self.get_next_solve_generator():
            print(x)
        return self.solutionList

    def get_next_solve_generator(self):
        last_was_del = False
        buff = []
        while buff or not last_was_del:
            if not last_was_del:
                list = self.getListMin()
                if not list:
                    if not buff:
                        last_was_del = True
                    else:
                        last = buff.pop()
                        self.crossRestoreInList(last)
                        last = last.down
                        if last == last.upHeader:
                            last_was_del = True
                        else:
                            self.crossDelInList(last)
                            buff.append(last)
                            last_was_del = False
                else:
                    last = list.down
                    self.crossDelInList(last)
                    buff.append(last)
                    last_was_del = False
            else:
                last = buff.pop()
                self.crossRestoreInList(last)
                last = last.down
                if last == last.upHeader:
                    last_was_del = True
                else:
                    self.crossDelInList(last)
                    buff.append(last)
                    last_was_del = False
            if self.xListHeader == self.xListHeader.right:
                yield self.getDataFromBuff(buff)

    def solve(self):
        list = self.getListMin()  # Возвращает столбец с минимумом возможных решений, если вернет ничего, то в столбце нет возможных решений, что означает тупиковую ветку
        if list:
            list = list.down
            while list != list.upHeader:
                self.buff.append(list)
                self.crossDelInList(list)
                self.solve()
                if self.xListHeader.right == self.xListHeader:
                    print(len(self.buff))
                    self.solutionList.append(self.getDataFromBuff(self.buff))
                self.crossRestoreInList(self.buff.pop())
                list = list.down

    def getDataFromBuff(self, list):
        result = []
        for x in list:
            data = x.leftHeader.data
            result.append(data)
        return result

    def getListMin(self):
        list = self.xListHeader.right
        len = numpy.inf
        result = None
        while list != list.leftHeader:
            n = 0
            strList = list.down
            while strList != strList.upHeader:
                n += 1
                strList = strList.down
            if n == 0:
                return None
            if n < len:
                result = strList
                len = n
            list = list.right
        return result

    def __debug_cheker(self):
        start = self.xListHeader.right
        while start != self.xListHeader:
            down = start.down
            while down != down.upHeader:
                print(down.data)
                down = down.down
            start = start.right

    def create_list_header(self, shape):
        self.xListHeader.up = self.xListHeader.upHeader = self.xListHeader.leftHeader = self.xListHeader.down = self.xListHeader.left = self.xListHeader.right = self.xListHeader
        list = self.xListHeader
        for x in range(shape[1]):
            newNode = self.Node(x, None, None, list, list.right, None, self.xListHeader)
            list.right = newNode
            self.xListHeader.left = newNode
            list = list.right
            list.up = list.down = list.upHeader = list
        list = self.xListHeader
        for x in range(shape[0]):
            newNode = self.Node(x, list, list.down, None, None, self.xListHeader, None)
            list.down = newNode
            self.xListHeader.up = newNode
            list = list.down
            list.left = list.right = list.leftHeader = list

    def create_links_by_matrix(self, matrix):
        y = 0
        downStart = self.xListHeader.down
        for str in matrix:
            x = 0
            rightStart = self.xListHeader.right
            for col in str:
                if col:
                    newNode = self.Node((y, x), rightStart.up, rightStart, downStart.left, downStart,
                                        rightStart, downStart)
                    rightStart.up.down = newNode
                    rightStart.up = newNode
                    downStart.left.right = newNode
                    downStart.left = newNode
                rightStart = rightStart.right
                x += 1
            downStart = downStart.down
            y += 1

    def deleteStrFromList(self, node):
        list = node.leftHeader.right
        while list != list.leftHeader:
            list.up.down = list.down
            list.down.up = list.up
            list = list.right
        list.up.down = list.down
        list.down.up = list.up

    def deleteColFromList(self, node):
        strList = node.upHeader
        strList.left.right = strList.right
        strList.right.left = strList.left

    def restoreStrToList(self, node):
        list = node.leftHeader.right
        while list != list.leftHeader:
            list.up.down = list
            list.down.up = list
            list = list.right
        list.up.down = list
        list.down.up = list

    def restoreColToList(self, node):
        list = node.upHeader
        list.left.right = list
        list.right.left = list

    crossDelRestBuff = []

    def crossDelInList(self, node):
        buff2 = []
        list = node.leftHeader.right
        while list != list.leftHeader:
            buff = []
            colList = list.upHeader.down
            while colList != list.upHeader:
                buff.append(colList)
                self.deleteStrFromList(colList)
                colList = colList.down
            buff2.append(buff)
            self.deleteColFromList(list)
            list = list.right
        self.crossDelRestBuff.append(buff2)

    def crossRestoreInList(self, node):
        list = node.leftHeader.right
        while list != list.leftHeader:
            self.restoreColToList(list)
            list = list.right
        buff = self.crossDelRestBuff.pop()
        for x in buff:
            for y in x:
                self.restoreStrToList(y)