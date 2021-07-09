#!/usr/bin/python3

# Note: Some times shatter will produce extra literals from the original file
#       This script will add any new literals and update the parameters


import sys
import re

if len(sys.argv) != 3 :
    print("Usage:$ python3 sbc_parser example.cnf.text, destination.cnf")
    exit()

symmetry_breaking_clauses = sys.argv[1]
output = sys.argv[2]
file = open(symmetry_breaking_clauses, "r")
max_num_literals = 0
num_added_clauses = 0

# skip the first line
file.readline()

lines = file.readlines()

new_content = []

for line in lines: 
    clause = re.findall(r'\(.*?\)', line)
    if len(clause) != 0:
        clause_to_add = clause[0]
        clause_to_add = clause_to_add.strip('()')
        data = clause_to_add.split(',')

        # Keep track of the literals
        if int(data[0]) > max_num_literals:
            max_num_literals = int(data[0])
        if int(data[1]) > max_num_literals:
            max_num_literals = int(data[1])

        new_content.append("-"+data[0]+" "+data[1]+" "+"0"+"\n")
        num_added_clauses += 1
        # print("-"+data[0]+" "+data[1]+" "+"0"+"\n", end="")

file.close()

file = open(output, "r+")


## Update the parameter line
parameters = file.readline().split()
# num literals
if int(parameters[2]) < max_num_literals:
    parameters[2] = str(max_num_literals)
# num clauses
parameters[3] = int(parameters[3]) + num_added_clauses

file.seek(0,0)
file.write(parameters[0]+" "+parameters[1]+" "+parameters[2]+" "+str(parameters[3])+"\n")

## Set to the end of the file
file.seek(0,2)
for line in new_content:
    file.write(line)
file.close()
