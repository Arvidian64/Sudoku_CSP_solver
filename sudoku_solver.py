from text_parser import parse_sudoku
import time

class SudokuCSP:
    def __init__(self, puzzle):
        #81 tuples, representerar rad o kolumn
        self.variables = []
        for row in range(9):
            for column in range(9):
                self.variables.append((row, column))

        self.domains = {}
        for row in range(9):
            for column in range(9):
                if puzzle[row][column] == 0: # Tom cell
                    self.domains[(row, column)] = list(range(1, 10))
                else: # Fylld cell
                    self.domains[(row, column)] = [puzzle[row][column]]

        self.constraints = {}
        for var in self.variables:
            self.constraints[var] = self.get_neighbors(var)

    def get_neighbors(self, var):
        # Hittar constraints till en given plats baserat på kringliggande tal
        row, column = var
        neighbors = set() #Genom att använda set kan de inte innehålla duplicerade värden

        # De tre constraintsen är samma rad, kolumn o 3x3 låda

        for neighboring_row in range(9):
            if neighboring_row != row:
                neighbors.add((neighboring_row, column))

        for neighboring_column in range(9):
            if neighboring_column != column:
                neighbors.add((row, neighboring_column))

        box_row, box_column = 3 * (row // 3), 3 * (column // 3)
        for neighboring_row in range(box_row, box_row + 3):
            for neighboring_column in range(box_column, box_column + 3):

                if (neighboring_row, neighboring_column) != (row, column):
                    neighbors.add((neighboring_row, neighboring_column))

        return neighbors

if __name__  == "__main__":
    sudoku = parse_sudoku()
    for i in sudoku:
        print(sudoku[i])
        csp = SudokuCSP(sudoku[i])
        for var in csp.variables:
            print(csp.constraints[var])
