
# sudoku_dictionary = {'SUDOKU 0':
#                          [
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
#                              [0, 0, 0, 0, 0, 0, 0, 0, 0]
#                          ]}

def parse_sudoku():
    count = -1
    dictionary = {}
    with open('Assignment 2 sudoku.txt', 'r') as f:
        for line in f:
            if line[0:6] == "SUDOKU":
                dictionary[line] = []
                name = line
                count = 0
            elif 9 > count > -1:
                row = []
                for i in range(9):
                    row.append(int(line[i]))
                dictionary[name].append(row)
                count += 1

    return dictionary




def main():
    sudoku_dictionary = parse_sudoku()

    for key in sudoku_dictionary:
        print("\n"+"---------------------------\n"+key+"---------------------------")
        for value in sudoku_dictionary[key]:
            print(value)


if __name__ == "__main__":
    main()
