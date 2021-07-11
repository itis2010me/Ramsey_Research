#!/bin/bash

# Defaults
QUIET=0
SHATTER=0
SAT=0
SOLVER="satch"


if [ "$#" -lt 2 ]; then
    echo "Usage: ./process.sh <Directory of CNFS> <Results Directory> -flags"
    echo "flags:"
    echo "-q|--quiet    Quite mode for the SAT solvers. Glucose does not have quite mode!"
    echo "-s|--shatter  User Shatter to optimize input files."
    echo "-sat=<solver> Specifiy the SAT solver you want to use"
    echo "Also make sure that SAT solver is in the first directory and named SAT"
    echo "Does not support more specialized flags of each SAT solver, yet!"
    exit 0
fi

# Parse CLAs
for arg in "$@"
do
    case $arg in
    -q|--quiet)
    QUIET=1
    # shift
    ;;
    -s|--shatter)
    SHATTER=1
    ;;
    -sat=*)
    SOLVER="${arg#*=}"
    ;;
    esac
done


# Create result directory
if [ -d "$2" ]
then
    echo "$2 directory already exist."
else
    echo "Creating results directory..."
    mkdir $2
fi

# Check input CNF directory
if [ ! -d "./$1" ]
then
    echo "$1 DOES NOT EXIST!"
    exit 1
fi

# RUN Shatter and/or SAT solver
cd ./$1

if [ $SHATTER -eq 1 ]
then 
    echo "Running Shatter..."
fi

for FILE in *.cnf
do
    if [ $SHATTER -eq 1 ]
    then 
        perl shatter.pl $FILE
        rm -f *.cnf.g
        rm -f *.cnf.txt
    fi
done

echo "Running solver..."
for FILE in *.cnf
do 
    
    if [[ $QUIET -eq 0 ]] 
    then
        echo "---- [ $FILE ] -------------------"
        ./$SOLVER $FILE
        ./$SOLVER $FILE >> ../$2/$FILE.txt
        echo ""
    else
        ./$SOLVER -q $FILE > ../$2/$FILE.txt
        SAT=$(grep -c 'UNSATISFIABLE' ../$2/$FILE.txt)
        if [[ $SAT -eq 0 ]]
        then 
            echo "$FILE is satisfiable"
        else    
            echo "$FILE is unsatisfiable"
        fi
    fi
done

exit 0