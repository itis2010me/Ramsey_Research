#!/usr/bin/python3

# for grabbing CLAs
import sys


def choose(n,k):
    if k == 0:
        return 1
    else:
        return (n * choose(n-1,k-1)) / k


def generate_file_name(A,k,n,num_SCIP_solutions):
    file_name = "rado_"
    # remove '[' ']' around the equation, then get each value into a list
    equation = (A[1:-1]).split(',')

    for value in equation:
        file_name = file_name + value + "_"
    file_name = file_name + "k" + str(k) + "_n" + str(n) + ".cnf"

    num_literals = n * k
    num_clauses = n + ((num_SCIP_solutions-1) * k) + (choose(k,2) * n)

    # write the parameter line
    file = open(file_name, "w")
    file.write("p cnf " + str(num_literals) + " " + str(int(num_clauses)) + "\n")
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
    SCIP = open("tempSCIPsols.txt", "r")
    file = open(file_name, "a")

    SCIP.readline()
    for line in SCIP:
        line = line[0:-4]
        solution = line.split(',')
        solution.pop(0)
        file.write(generate_negative_clause(solution,k))

    SCIP.close()
    file.close()

def main():
    if len(sys.argv) != 5 :
        print("Usage:$ python3 RadoCG_py k n A num_SCIP_solutions")
        exit()
    
    k = int(sys.argv[1])
    n = int(sys.argv[2])
    A = sys.argv[3]

    # this will assume that SCIP contains an extra line, actual number is 1 less
    num_SCIP_solutions = int(sys.argv[4])

    file_name = generate_file_name(A,k,n,num_SCIP_solutions)
    write_positive_clauses(file_name,k,n)
    write_negative_clauses(file_name,k)
    write_optional_clauses(file_name,k,n)

main()