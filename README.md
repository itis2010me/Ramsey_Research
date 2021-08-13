# SAT_Research
Repo for all the files during SS2021 research project on Ramsey Theory and SAT solvers.

# Summary

The research focues on a subset of Ramsey Theory, Rado's theorems. Instead of looking at colored graphs, we are looking at large system(s) of linear homogenous equations and coloring the intergers to find solutions. 

There are many conjectures about the theoretical quantity of Rado's number and the degree of regurity. We wish to use the power of computer and boolean algebra to prove or dis-prove these conjectures. 

The use of Boolean algebra, particularly SAT, will be extensive. Each system of linear homogenous equation will be encoded into many clauses. Then, using SAT solvers, along with heavy optimization techniques both before and during the execution of the solver, solve the SAT problem in a reasonable time. 

Details comming soon...



# Code Optimization

The computation can be broken down into two steps:

- Generating the encoded problem in CNF(Dimacs) format.
- Feed the result `.cnf` file into SAT solver.
  - There might be some symmetry breaking processes in the middle.

Orignal CNF generation was done in Maple. Another implementation later was done in C++ in order to achieve better speed.

- C++ implementation includes some optimzation techniques including: loop unrolling, multithreading.

Due to the sheer large number of write operations to a file(millions of lines), python was chosen in the end to generate CNF files.

Speed improvement for example of instance with `n=1500` is from 25mins(Maple) -> 5mins(C++) -> 1min(python).

Added symmetry breaking clauses according to M.Heule's encoding. 

- Symmetry breaking currently only works with linear equation with 3 variables only! 
- Performance increase is not apparent when coloring smaller instances of the integers. 

Next step, during the generation, generating all the possible solution for a linear equation with SCIP takes a significant amount of time. We are looking for linear algebra theorems to improve this part. Details coming soon...

# Note

The script will use the following modules:

- Maple
- SCIP - for finding integer solutions much faster.
- Perl
- Python 3

The C++ Rado generator served as an improvement from Maple.

- Use SCIP to find all solutions to Ax=b
- Linear read/write to files(areas of improvement)

The following SAT solvers I want to give credit to:

- satch: https://github.com/arminbiere/satch
- glucose(parallel) : https://www.labri.fr/perso/lsimon/glucose/
- minisat: http://minisat.se/

Script that I modified:

- Shatter's perl script
- Use in conjunction with symmetry breaking clause parser python script

# Version 

Project stated June 26, 2021

Last updated on Augest 13, 2021
