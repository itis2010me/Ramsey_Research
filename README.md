# SAT_Research
Repo for all the files during SS2021 research project on Ramsey Theory and SAT solvers.

# Summary

The research focues on a subset of Ramsey Theory, Rado's theorems. Instead of looking at colored graphs, we are looking at large system(s) of linear homogenous equations and coloring the intergers to find solutions. 

There are many conjectures about the theoretical quantity of Rado's number and the degree of regurity. We wish to use the power of computer and boolean algebra to prove or dis-prove these conjectures. 

The use of Boolean algebra, particularly SAT, will be extensive. Each system of linear homogenous equation will be encoded into many clauses. Then, using SAT solvers, along with heavy optimization techniques both before and during the execution of the solver, solve the SAT problem in a reasonable time. 

Details comming soon...

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

