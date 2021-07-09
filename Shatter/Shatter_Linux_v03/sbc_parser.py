#!/usr/bin/python3

import sys
import re

if len(sys.argv) != 3 :
    print("Usage:$ python3 sbc_parser example.cnf.text, destination.cnf")
    exit()

symmetry_breaking_clauses = sys.argv[1]
output = sys.argv[2]
file = open(symmetry_breaking_clauses, "r")

file.readline()

lines = file.readlines()

new_content = []

for line in lines: 
    clause = re.findall(r'\(.*?\)', line)
    if len(clause) != 0:
        clause_to_add = clause[0]
        clause_to_add = clause_to_add.strip('()')
        data = clause_to_add.split(',')
        new_content.append("-"+data[0]+" "+data[1]+" "+"0"+"\n")
        print("-"+data[0]+" "+data[1]+" "+"0"+"\n", end="")
file.close()


