# SAT_Research
This project is the collabration between Professor Jesus De Loera(UC Davis), William Wesley and Yuan Chang. The repository contains miscellaneous information and content for the ISAAC 2022 candidate research paper, code for running the research experiments and their logged optimizations.

# Summary

The research focues on a subset of Ramsey Theory, Rado's theorems. Instead of looking at colored graphs, we are looking at large system(s) of linear homogenous equations and coloring the intergers to find solutions. 

There are many conjectures about the theoretical quantity of Rado's number and the degree of regurity. We wish to use the power of computer and boolean algebra to prove or dis-prove these conjectures. 

The use of Boolean algebra, particularly SAT, will be extensive. Each system of linear homogenous equation will be encoded into many clauses. Then, using SAT solvers, along with optimization techniques both before and during the execution of the solver, solve the SAT problem in a reasonable time. 


# Project Organization

- `README.md` - This file. 
- `./Shatter` - The directory containing the code to symmetrying breaking through Shatter and connected together thorough a script written in Perl. 
- `./Maple_files`- The directory containing the original Maple files to generate the Rado CNFs
- `./Presentations` - The directory containting all the presentation slides for William Wesley and Yuan Chang, typeset in `Latex`.
- `./code` - The directory containting all the source code for generating the Rado CNFs. The C version of the code and its `Makefile` are also included, but will not automatically be built when running the `process.sh` script. 
- `process.sh` - The script that runs all the code with specific input. 
- ` ./glucose_SAT_solver` - Copy of the glucose SAT solver.
- `./Example` - The directory containing example text files for the research paper. (CNF encoding and Loop unrolling example).
- `./paper_content` - The directory containing all files for extra information supporting the research paper for ISAAC 2022 conference.

Note that when running the code, a compiled and executatble SAT solver must be placed within the `./code` directory. At the moment, we coded our script to take in `satch` or `glucose` as SAT candidate solvers. 

# How to Run the code

Note: In order to try out the code, generate test files and compute, you need have both Python and Maple installed. If you wish to use the C++ version, you need to complie the executable yourself. 

1. Make sure to allow for execution of the bash and python scripts. 

   ```bash
   $ chmod a+x your_executable
   ```

2. Make sure to have `Maple` commandline version intalled. Modifiy the `Rado_Generate.sh` script line 11:

   ```bash
   your_maple_absolute_path -i isolve_maple.mpl -c "isolve_Maple($3);" -c "quit;"
   ```

3. The usage of `./process.sh` script:

   ```bash
   $./process.sh
   usage: ./process.sh k A lb up sym_f
   
   k          Number of colors
   A          Linear equation in 1 x n matrix form [a,b,c]
   lb         Lower bound for the Rado number
   up         Upper bound for the Rado number
   sym_f      Symmetry breaking flag, 0 -> turn off
   
   -sat=      Select a SAT solver to opearte. Default to satch
   -q|--quite Disable verbal response from SAT solver
   
   Input for k A and bounds are not checked for correctness.
   This process script will use binary search to search for the Rado number 
   of given settings.
   ```

4. Example: Find the 3-color Rado number for `x+y=z`

   ```bash
   $ ./process.sh 3 [1,1,-1] 5 15 0 -sat=satch -q
   ----------- [ Start ] -----------
   Running solver...
   Checking upper bound...
   Checking lower bound...
   Searching...
   10
   13
   14
   ----------- [ Results ] ----------
   Rado number for [1,1,-1] with 3-coloring is 14.
   ----------- [ Done ] -------------
   Time taken: 0 seconds
   ```


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

Next step, during the generation, generating all the possible solution for a linear equation with SCIP takes a significant amount of time. We are looking for linear algebra theorems to improve this part. 

Using Maple's `isolve` parametrization function, we can generate all possible solutions with python. 

- The speedup is around 4.25x compare to using SCIP alone. 

# Note

The script will use the following modules:

- Maple
  - Symbolic manipulation, generate SCIP input files.
- SCIP - for finding integer solutions much faster. (No longer in use)
  - Hermite Normal Form is the next step to optimize SCIP away.
- Perl
- Python 3
  - Sympy and Numpy python libraries.

The C++ Rado generator served as an improvement from Maple.

- Use SCIP to find all solutions to Ax=b (obsolete) 
- Linear read/write to files(areas of improvement)

The following SAT solvers I want to give credit to:

- satch: https://github.com/arminbiere/satch
- glucose(parallel) : https://www.labri.fr/perso/lsimon/glucose/
- minisat: http://minisat.se/

Script that I modified:

- Shatter's perl script
- Use in conjunction with symmetry breaking clause parser python script

# Version 

Project started June 26, 2021

Last updated on April 17, 2022
