#!/usr/bin/python3

# for grabbing CLAs
import sys

symmetry_flag = True

def choose(n,k):
    if k == 0:
        return 1
    else:
        return (n * choose(n-1,k-1)) / k

# currently only works for 3 coloring and equations with 3 variables!
def generate_symmetry_breaking_clauses(k):
    file = open("solutions.txt", "r")
    symmetry_breaking_clauses = []
    flag = True

    print("Adding symmetry...")

    while flag:
        solution = file.readline()
        solution = solution.strip("\n")
        # end of file
        if len(solution) == 0:
            return symmetry_breaking_clauses
        # solution = solution[0:-4]
        solution = solution.split(',')
        # solution.pop(0)
    
        if len(set(solution)) == 2:
            flag = False
    
    file.close()
    solution = list(set(solution))
    symmetry_breaking_clauses.append(str(int(solution[0])*k) + " 0\n")
    symmetry_breaking_clauses.append(str(int(solution[1])*k-1) + " 0\n")

    return symmetry_breaking_clauses


def generate_file_name(A,k,n,num_solutions):
    file_name = "rado_"
    # remove '[' ']' around the equation, then get each value into a list
    equation = (A[1:-1]).split(',')

    for value in equation:
        file_name = file_name + value + "_"
    file_name = file_name + "k" + str(k) + "_n" + str(n) + ".cnf"

    if symmetry_flag:
        SBC = generate_symmetry_breaking_clauses(k)
    else:
        SBC = []


    num_literals = n * k
    num_clauses = n + ((num_solutions) * k) + (choose(k,2) * n) + len(SBC)

    # write the parameter line
    file = open(file_name, "w")
    file.write("p cnf " + str(num_literals) + " " + str(int(num_clauses)) + "\n")
    for clause in SBC:
        file.write(clause)
    file.close()

    return file_name


def write_positive_clauses(file_name, k, n):
    file = open(file_name, "a")
    index = 1
    for _ in range(n):
        for _ in range(k):
            file.write(str(index) + " ")
            index += 1
        file.write("0 \n")

    file.close()

# def write_positive_clauses(file_name, k, n):
#     file = open(file_name, "a")
#     index = 1
#     for _ in range(n):
#         file.write(str(index) + " ")
#         file.write(str(index+1) + " ")
#         file.write(str(index+2) + " ")
#         index += 3
#         file.write("0 \n")

#     file.close()

def write_optional_clauses(file_name, k, n):
    file = open(file_name, "a")
    for i in range(1,n+1):
        for j in range (1,k):
            for q in range(j+1,k+1):
                file.write("-" + str(i*k-(k-j)) + " " + "-" + str(i*k-(k-q)) + " 0 \n")

    file.close()

def generate_negative_clause(solution,k):
    clauses = ""
    for c in range(k-1,-1,-1):
        subclause = ""
        for value in solution:
            subclause = subclause + "-" + str((int(value)*k)-c) + " "
        subclause = subclause + "0 \n"
        clauses = clauses + subclause
    return clauses

def write_negative_clauses(file_name,k):
    Solutions = open("solutions.txt", "r")
    file = open(file_name, "a")

    for line in Solutions:
        # line = line[0:-4]
        solution = line.split(',')
        # solution.pop(0)
        file.write(generate_negative_clause(solution,k))

    Solutions.close()
    file.close()




def main():
    if len(sys.argv) != 6 :
        print("Usage:$ python3 RadoCG_py k n A num_solutions f")
        print("Got" + str(len(sys.argv)))
        exit(0)
    
    k = int(sys.argv[1])
    n = int(sys.argv[2])
    A = sys.argv[3]

    global symmetry_flag

    if sys.argv[5] == "1":
        symmetry_flag = True
    else:
        symmetry_flag = False


    # this will assume that SCIP contains an extra line, actual number is 1 less
    num_solutions = int(sys.argv[4])

    file_name = generate_file_name(A,k,n,num_solutions)
    write_positive_clauses(file_name,k,n)
    write_negative_clauses(file_name,k)
    write_optional_clauses(file_name,k,n)

main()