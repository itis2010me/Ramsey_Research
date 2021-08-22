#!/usr/bin/python3


import sys


def main():

    SCIP_file = sys.argv[1]
    output_file = sys.argv[2]

    SCIP = open(SCIP_file, "r")
    file = open(output_file, "r")

    output_sols = file.readlines()
    # print(output_sols[0])

    SCIP.readline()

    for line in SCIP:
        line = line[0:-4]
        line = line[line.find(",")+2:] + "\n"
        if line in output_sols:
            continue
        else:
            print(line)


    SCIP.close()
    file.close()

main()
