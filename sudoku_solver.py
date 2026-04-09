import json
import time
from collections import deque

from text_parser import parse_sudoku


#Exports CSPs as json for debugging
def export_to_json(csp_instance, filename="/CSPs/sudoku_csp.json"):
    # We must convert tuple keys to strings because JSON keys must be strings
    data_to_export = {
        "domains": {f"{r},{c}": dom for (r, c), dom in csp_instance.domains.items()},
        "constraints": {f"{r},{c}": [f"{nr},{nc}" for (nr, nc) in neighbors]
                        for (r, c), neighbors in csp_instance.constraints.items()}
    }

    with open(filename, "w") as f:
        json.dump(data_to_export, f, indent=4)

    print(f"Successfully exported CSP structure to {filename}")


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

#Kollar arc-consistency, återvänder False om den hittar en inconsistency
def arc_consistency(csp):
    queue = deque()
    for var_i in csp.variables:
        for var_j in csp.get_neighbors(var_i):
            queue.append((var_i, var_j))

    while queue:
        (var_i, var_j) = queue.popleft()

        # Kollar om vi kan ta bort från domänen var_i tillhör
        if revise(csp, var_i, var_j):

            # Om domänen är tom kan puzzlet vara olösbart
            if len(csp.domains[var_i]) == 0:
                print("Olösbart?")
                return False

            # Ifall domänen ändras lägger vi grannarna till var_i i kön
            # (var_j exkluderad, då funktionen redan kollat den)
            for var_k in csp.get_neighbors(var_i):
                if var_k != var_j:
                    queue.append((var_k, var_i))

    return True

# Returnerar True om vi ändrar domänen av var_i för att matcha begränsningarna av var_j
def revise(csp, var_i, var_j):
    revised = False

    domain_i = csp.domains[var_i]
    domain_j = csp.domains[var_j]

    # We check each value in xi's domain
    for value_i in list(domain_i):
        # Constraint: xi != xj
        # If there is no value in xj's domain that is different from value_i,
        # then value_i is impossible.
        if not any(value_j != value_i for value_j in domain_j):
            domain_i.remove(value_i)
            revised = True

    return revised

def recursive_backtracking_search(csp):
    #Returnerar None om ingen lösning existerar
    return backtrack(csp)

def backtrack(csp):
    # Kolla om assigneringen är komplett (alla domäner har bara ett värde)
    if all(len(csp.domains[var]) == 1 for var in csp.variables):
        return csp.domains

    # Väljer
    var = minimum_remaining_value(csp)

    # Testar varje värde i domänen
    for value in list(csp.domains[var]):
        if is_consistent(csp, var, value):

            original_domains = {v: list(d) for v, d in csp.domains.items()}

            csp.domains[var] = [value]

            result = backtrack(csp)
            if result is not None:
                return result

            csp.domains = original_domains

    return None

## Gamla MRV-funktionen
# def minimum_remaining_value(csp):
#     unassigned = [v for v in csp.variables if len(csp.domains[v]) > 1]
#     return min(unassigned, key=lambda v: len(csp.domains[v]))

def minimum_remaining_value(csp):
    best_var = None
    smallest_size = 100

    for var in csp.variables:
        domain_size = len(csp.domains[var])
        if domain_size > 1:
            if domain_size < smallest_size:
                smallest_size = domain_size
                best_var = var

                if smallest_size == 2:
                    return best_var

    return best_var

def is_consistent(csp, var, value):
    # Kollar om assigneringen av ett värde bryter mot några constraints med dess grannar
    for neighbor in csp.get_neighbors(var):
        # Ifall grannen redan är assignerad och har samma värde så är det inkonsekvent
        if len(csp.domains[neighbor]) == 1 and csp.domains[neighbor][0] == value:
            return False
    return True

def fast():
    sudoku = parse_sudoku()
    start_time = time.time()
    results = []
    for i in sudoku:
        csp = SudokuCSP(sudoku[i])
        original = dict(csp.domains)
        success = arc_consistency(csp)

        solution = recursive_backtracking_search(csp)

        if solution:
            results.append(csp.domains)

    it_took = time.time() - start_time
    for solution in results:
        for row in range(9):
            print(" ", end=" ")
            for column in range(9):
                tuple = (row, column)
                print(solution[tuple][0], end="  ")
            print("")
        print("\n-----------------------------\n")
    print("\nIt took:\n" + str(it_took) + " seconds")


def visual():
    from sudoku_visualizer import sudoku_visualizer

    sudoku = parse_sudoku()
    start_time = time.time()
    results = []
    for i in sudoku:
        csp = SudokuCSP(sudoku[i])
        original = {k: list(v) for k, v in csp.domains.items()}
        export_to_json(csp, filename="CSPs/" + i[:-1] + ".json")
        # for var in csp.variables:
        #     print(csp.constraints[var])
        success = arc_consistency(csp)
        if success:
            export_to_json(csp, filename="AC-CSPs/" + i[:-1] + ".json")

        solution = recursive_backtracking_search(csp)

        if solution:
            print("Sudoku löst")
            results.append((original, csp.domains))
            for row in range(9):
                for column in range(9):
                    tuple = (row, column)
                    print(solution[tuple], end=" ")
                print("")
        else:
            print("Lösning saknas")
    it_took = time.time() - start_time
    print("\nIt took:\n" + str(it_took) + " seconds")

    gallery = sudoku_visualizer(results)
    gallery.run()

if __name__  == "__main__":
    # fast()
    visual()
