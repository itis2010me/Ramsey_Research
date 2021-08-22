#!/usr/bin/python3

import re
import sympy as sp
import math

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

# x > y -> return 1, otherwise return -1
# def get_loop_delta(x,y):
#     if x >= y:
#         return 1
#     else:
#         return -1

# complex_double_loop_sol(n, ("x",i), ("y", "-6*i/-13 + y/-13"))
def complex_double_loop_sol(n, outer_loop_pair, inner_loop_pair):

    count = 0

    # outer_loop_variable
    OLV = outer_loop_pair[1]

    # inner_loop_variable
    ILV = inner_loop_pair[0]
    inner_loop_equation = inner_loop_pair[1]
    if OLV == "i":
        for i in range(1,n+1):
            bound_A = math.floor(round(eval(inner_loop_equation.replace(ILV, "1")), 5))
            bound_B = math.ceil(round(eval(inner_loop_equation.replace(ILV, str(n))), 5))
            # print(bound_B, bound_A)
            # print(round(bound_B))
            for j in range(bound_B, bound_A+1):

                value = eval(evaluations["z"])
                if check_bounds(n,value):
                    print(eval(evaluations["z"]), end=", ")
                    print(eval(evaluations["y"]), end=", ")
                    print(eval(evaluations["x"]))
                    # print(i,j)
                    count += 1

        print("There are " + str(count) + " solutions.")

    elif OLV == "j":
        for j in range(1,n+1):
            pass
    else:
        print("Complex_loop: Error in parsing.")
        exit(0)

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
    n = 1000
    global evaluations

    # examples:
    # {x = a, y = 6*a - 13*b, z = a + 5*b}
    # {x = -i + j, y = i, z = j}
    # {x = i, y = 6*i - 13*j, z = i + 5*j}

    equation = "{x = i, y = 6*i - 13*j, z = i + 5*j}"
    # remove curly brackets
    equation = equation[1:-1]
    
    count = check_equations(equation)
    expressions = equation.split(",")
    expressions = clean_expressions(expressions)
    assign_evaluations(expressions)
    

    complex_double_loop_sol(n, ("x","i"), ("y", "-6*i/-13 + y/-13"))

    # print(evaluations["z"])
    
    # expressions = sorted(expressions, key=len)
    # if count == 2:
    #     print(expressions[len(expressions)-1])
    #     temp = (expressions[len(expressions)-1]).split("=")
    #     double_loop_sol(n, temp[0].strip())
    # elif count == 1:
    #     # output solutions
    #     simple = (expressions[len(expressions)-1]).split("=")
    #     outer_variable = simple[1].strip() # i or j
    #     pass
    # else:
    #     print("Error parsing the equation!")
    #     exit(0)
    

main()