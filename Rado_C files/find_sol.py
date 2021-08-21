#!/usr/bin/python3

import re
import sympy as sp

# List of regex that matches certain expressions:
# [xyz] = [ij] -> x = i or x = j or z = j ...
# 
# 
# 
# 
# 
# 

# stores x,y,z's evaluation expressions in a dict
evaluations = {}

# return 2 for basic double for loop, 1 for other loop
# return 0 for error
def check_equations(equation):
    count = 0
    expressions = equation.split(",")
    for expression in expressions:
        if re.search("[xyz] = [ij]", expression):
            count += 1
    return count

# check basic bounds of 1 <= x <= n
def check_bounds(n, value):
    if 1 <= value and value <= n:
        return True
    else:
        return False

def double_loop_sol(n, var):
    count = 0
    for i in range(1,n+1):
        for j in range(1,n+1):
            value = eval(evaluations[var])
            if check_bounds(n, value):
                count += 1
                print(i,j)
    print("There are " + str(count) + " solutions.")

# given an expression
# x = i, y = 6*i - 13*j, z = i + 5*j -> 
# def prepare_for_complex(expressions):



# def complex_double_loop_sol(n, ):


def clean_expressions(expressions):
    results = []
    for expression in expressions:
        results.append(expression.strip())
    return results

def assign_evaluations(expressions):
    global evaluations
    for expression in expressions:
        components = expression.split("=")
        evaluations[components[0].strip()] = components[1].strip()

    print(evaluations["x"])
    print(evaluations["y"])
    print(evaluations["z"])

def main():

    # upper bound
    n = 10
    global evaluations

    # examples:
    # {x = a, y = 6*a - 13*b, z = a + 5*b}
    # {x = -i + j, y = i, z = j}
    # {x = i, y = 6*i - 13*j, z = i + 5*j}

    equation = "{x = -i + j, y = i, z = j}"
    # remove curly brackets
    equation = equation[1:-1]
    
    count = check_equations(equation)
    expressions = equation.split(",")
    expressions = clean_expressions(expressions)
    assign_evaluations(expressions)
    
    # print(evaluations["z"])
    
    expressions = sorted(expressions, key=len)
    if count == 2:
        print(expressions[len(expressions)-1])
        temp = (expressions[len(expressions)-1]).split("=")
        double_loop_sol(n, temp[0].strip())
    elif count == 1:
        # output solutions
        simple = (expressions[len(expressions)-1]).split("=")
        outer_variable = simple[1].strip() # i or j
        pass
    else:
        print("Error parsing the equation!")
        exit(0)
    

main()