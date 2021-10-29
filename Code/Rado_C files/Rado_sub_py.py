#!/usr/bin/python3

# for grabbing CLAs
import sys


# function to create new file name
def creat_new_file_name(n,orignal_file):

    # find the index where 'n' is located
    index = orignal_file.find('n')

    # remove everything after index and insert new information
    return orignal_file[0:index+1] + str(n) + ".cnf"


def below_limit(line, limit):

    values = line.split()
    for value in values:
        if value[0] == '-':
            if int(value[1:]) > limit:
                return False
        else:
            if int(value) > limit:
                return False
    return True

def extract_sub_formula(file_name, original_file_name, limit):
    count = 0
    original = open(original_file_name, "r")
    file = open(file_name, "w")

    original.readline()
    while True:
        line = original.readline()

        if not line:
            break
        # print(line)

        if below_limit(line, limit):
            file.write(line)
            count += 1
    
    original.close()
    file.close()
    return count
        
def add_parameter_line(file_name, temp_file_name, num_literals, num_clauses):
    file = open(file_name, "a")
    file.write("p cnf " + str(num_literals) + " " + str(num_clauses) + "\n")
    temp_file = open(temp_file_name, "r")
    while True:
        line = temp_file.readline()
        if not line:
            break
        file.write(line)
    
    file.close()
    temp_file.close()


def main():
    if len(sys.argv) != 4 :
        print("Usage:$ python3 Rado_sub_py k n file.cnf")
        exit()
    
    k = int(sys.argv[1])
    n = int(sys.argv[2])
    origin_file = sys.argv[3]

    new_file = creat_new_file_name(n,origin_file)
    # print(str(below_limit("-49 50 -1 0", k*n)))
    num_clauses = extract_sub_formula("temp.txt", origin_file, k*n)
    add_parameter_line(new_file, "temp.txt", n*k, num_clauses)

main()