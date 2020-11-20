import DancingLinksSolver as DLS
from math import sqrt
import numpy


class SudokuSolver():

    def result(self, puzzle):
        self.puzzle = puzzle
        self.__validator()
        self.conditions = []
        self.solutions = []
        self.__solve(2)
        return self.solutions

    def __validator(self):
        self.size = len(self.puzzle[0])

    def __debugPrintMatrix(self):
        for x in self.xalgorytm_matrix.tolist():
            print(x)

    def __solve(self, limit):
        self.__create_xalgotythm_matrix()  # self.xalgorytm_matrix Матрица покрытия для судоку n*n
        print("Create matrix")
        self.solver = DLS.DancingLinksSolver(self.xalgorytm_matrix)
        print(type(numpy))
        print("Create dancing links")
        if self.solver.correct_start_condition_in_list(self.__create_list_of_conditions()) != 0:
            print("initial conditions are invalid")
            return
        iter = 0
        for x in self.solver.get_next_solve_generator():
            self.solutions.append(self.__convert_data(x))
            iter += 1
            if iter >= limit:
                break

    def __convert_all_data(self):
        newData = []
        for solution in self.solutions:
            newData.append(self.__convert_data(solution))
        self.solutions = newData

    def __convert_data(self, solution):
        result = numpy.zeros((self.size, self.size), dtype=int)
        for x in (solution + self.conditions):
            data = x
            num = data // self.size ** 2 + 1
            row = data % self.size ** 2 // self.size
            col = data % self.size ** 2 % self.size
            result[row][col] = num
        return result

    def __create_xalgotythm_matrix(self):
        # n - base value. col = (n*2+n*2+n*2+n*2)  str = (n**3)
        #                        1   2   3   4            5
        # 1 - каждая клетка должна быть заполнена
        # 2 - каждый столбик (n) имеет уникальное число от 1 до n**2
        # 3 - каждая строка (n) имеет уникальное число от 1 до n**2
        # 4 - каждый квадрат (n) имеет уникальное число от 1 до n**2
        # 5 - количество столбцов комбинация из всех клеток и цифр
        self.xalgorytm_matrix = numpy.zeros((self.size ** 3, 4 * self.size ** 2), dtype=int)
        for str_num in range(self.size ** 3):
            self.xalgorytm_matrix[str_num][0 * self.size ** 2 + str_num % self.size ** 2] = 1  # 1
            self.xalgorytm_matrix[str_num][
                1 * self.size ** 2 + str_num % self.size + (str_num // self.size ** 2) * self.size] = 1  # 2
            self.xalgorytm_matrix[str_num][2 * self.size ** 2 + str_num // self.size] = 1  # 3
            num = str_num // self.size ** 2  # номер от 0 до n
            quard = str_num % self.size ** 2  # количество комбинаций для одного числа
            col = quard % self.size  # Номер колонки
            str = quard // self.size  # номер строчки
            result = int((sqrt(self.size) * (str // sqrt(self.size)) + col // sqrt(self.size)) + num * self.size)
            # Порядковый номер квадранта в судоку, формула: 3(str//3) + col //3 для n**0/5=3
            self.xalgorytm_matrix[str_num][3 * self.size ** 2 + result] = 1  # 4

    def __create_list_of_conditions(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.puzzle[row][col] != 0:
                    self.conditions.append((self.puzzle[row][col] - 1) * self.size ** 2 + row * self.size + col)
        return self.conditions
