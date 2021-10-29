#!/usr/bin/python3

# from ast import parse
import re
import sympy as sp
import math
import sys

# from sympy.core.symbol import var

# List of regex that matches certain expressions:
# [xyz] = [ij]\Z -> x = i or x = j or z = j ...
# Note: \Z for end of the string
# 
# 
# 
# 
# 

# stores x,y,z's evaluation expressions in a dict
evaluations = {}
input_file = "isolve_maple.txt"
output_file = "solutions.txt"

# return 2 for basic double for loop, 1 for other loop
# return 0 for error
def check_equations(equation):
    count = 0
    expressions = equation.split(",")
    for expression in expressions:
        if re.search("[xyz] = [ij]\Z", expression.strip()):
            count += 1
    return count

# check basic bounds of 1 <= x <= n
def check_bounds(n, value):
    if 1 <= value and value <= n:
        return True
    else:
        return False


def double_loop_sol(n, var):
    file = open(output_file, "w")
    for i in range(1,n+1):
        for j in range(1,n+1):
            value = eval(evaluations[var])
            if check_bounds(n, value):
                # print(eval(evaluations["z"]), end=", ")
                # print(eval(evaluations["y"]), end=", ")
                # print(eval(evaluations["x"]))
                solution = str(eval(evaluations["z"])) + ", " + str(eval(evaluations["y"])) + \
                    ", " + str(eval(evaluations["x"])) + "\n"
                # # count += 1
                file.write(solution)
    file.close()



# given an expression
# [x = i, y = 6*i - 13*j, z = i + 5*j] -> [("x", "i"), ("y", "6*i/13 - y/13")]
def prepare_for_complex(expressions):

    # sympy preparation
    x,y,z,i,j = sp.symbols('x y z i j')

    results = []
    loop_variables = "ij"
    expressions_sorted = sorted(expressions, key=len)

    # prepare for ("x", "i") outer loop
    expression_A = (expressions_sorted[0]).split("=")
    expression_A_tuple = (expression_A[0].strip(), expression_A[1].strip())

    # set inner var, if outer is 'i', inner is 'j' instead, vice versa
    loop_variables = loop_variables.replace(expression_A_tuple[1], "")
    
    # prepare for ("y", "6*i/13 - y/13") inner loop
    expression_B = (expressions_sorted[2]).split("=")
    inner_var = expression_B[0].strip()
    equation = sp.Eq(sp.parse_expr(inner_var), sp.parse_expr(expression_B[1].strip()))

    expression_B_tuple = (inner_var, str(sp.solve(equation, loop_variables)[0]))
    
    results.append(expression_A_tuple)
    results.append(expression_B_tuple)

    return results


# complex_double_loop_sol(n, [("x",i), ("y", "-6*i/-13 + y/-13")])
def complex_double_loop_sol(n, loop_pairs):
    print(loop_pairs)
    # count = 0
    outer_loop_pair = loop_pairs[0]
    inner_loop_pair = loop_pairs[1]
    variables = "xyz"
    file = open(output_file, "w")

    # outer_loop_variable
    OLV = outer_loop_pair[1]

    # inner_loop_variable
    ILV = inner_loop_pair[0]

    variables = variables.replace(outer_loop_pair[0], "")
    variables = variables.replace(inner_loop_pair[0], "")
    inner_loop_equation = inner_loop_pair[1]
    if OLV == "i":
        for i in range(1,n+1):
            bound_A = math.floor(round(eval(inner_loop_equation.replace(ILV, "1")), 5))
            bound_B = math.ceil(round(eval(inner_loop_equation.replace(ILV, str(n))), 5))

            # ILB - Inner Loop bounds
            # need to determine which bound to start from
            ILB = [bound_A, bound_B]
            ILB.sort()

            for j in range(ILB[0], ILB[1]+1):
                
                value = eval(evaluations[variables])
                value_out = eval(evaluations[outer_loop_pair[0]])
                value_in = eval(evaluations[inner_loop_pair[0]])
                if check_bounds(n,value) and check_bounds(n,value_out) and check_bounds(n,value_in):
                    solution = str(eval(evaluations["z"])) + ", " + str(eval(evaluations["y"])) + \
                        ", " + str(eval(evaluations["x"])) + "\n"
                    # count += 1
                    file.write(solution)
        file.close()
    elif OLV == "j":
        for j in range(1,n+1):
            bound_A = math.floor(round(eval(inner_loop_equation.replace(ILV, "1")), 5))
            bound_B = math.ceil(round(eval(inner_loop_equation.replace(ILV, str(n))), 5))

            # ILB - Inner Loop bounds
            ILB = [bound_A, bound_B]
            ILB.sort()

            for i in range(ILB[0], ILB[1]+1):

                value = eval(evaluations[variables])
                value_out = eval(evaluations[outer_loop_pair[0]])
                value_in = eval(evaluations[inner_loop_pair[0]])
                if check_bounds(n,value) and check_bounds(n,value_out) and check_bounds(n,value_in):
                    solution = str(eval(evaluations["z"])) + ", " + str(eval(evaluations["y"])) + \
                        ", " + str(eval(evaluations["x"])) + "\n"
                    # count += 1
                    file.write(solution)
        file.close()
    else:
        file.close()
        print("Complex_loop: Error in parsing.")
        exit(0)

# remove white spaces around individual expressions
def clean_expressions(expressions):
    results = []
    for expression in expressions:
        results.append(expression.strip())
    return results

# assign the expressions to the variables
def assign_evaluations(expressions):
    global evaluations
    for expression in expressions:
        components = expression.split("=")
        evaluations[components[0].strip()] = components[1].strip()


def main():

    # upper bound
    n = int(sys.argv[1])
    global evaluations

    file = open(input_file, "r")
    equation = file.readline()
    if not equation :
        print("Error reading isolve input file.")
        exit(0)
    file.close()

    # examples:
    # {x = -i + j, y = i, z = j} PASS
    # {x = i, y = 6*i - 13*j, z = i + 5*j} PASS

    # {x = i, y = 5*i - j, z = j}
    # {x = i, y = 2*j, z = 2*i - 3*j}
    # {x = -i+j, y = i, z = j}

    # remove curly brackets and \n
    equation = equation.strip("{}\n")
    
    count = check_equations(equation)
    expressions = equation.split(",")
    expressions = clean_expressions(expressions)
    assign_evaluations(expressions)
    
    expressions = sorted(expressions, key=len)
    if count == 2:
        # print("Simple Loop")
        temp = (expressions[len(expressions)-1]).split("=")
        double_loop_sol(n, temp[0].strip())
    elif count == 1:
        # print("Complex Loop")
        parsed = prepare_for_complex(expressions)
        complex_double_loop_sol(n, parsed)
    else:
        print("Error parsing the equations!")
        exit(0)
    

main()