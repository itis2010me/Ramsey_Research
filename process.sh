#!/bin/bash

# Defaults
QUIET=0
SHATTER=0
SAT=0
SAT_TEST=0
SOLVER="satch"
LOWER_BOUND=0
UPPER_BOUND=0
UPPER_CNF=""
MID=0
ANS=-1
k=$1 # colorings
A=$2 # system of equation

clean_up () {
    rm -f *.cnf
    rm -f *.cnf.txt
    make clean >> log.txt
    echo "" > log.txt
}


if [ "$#" -lt 2 ]; then
    echo "Usage: ./process.sh k A -lb=x -up=y"
    echo "k      ->  number of colors"
    echo "A      ->  system of equations"
    echo "-lb/up ->  optional lower/upper bound"
    exit 0
fi

# Parse CLAs
for arg in "$@"
do
    case $arg in
    # -q|--quiet)
    # QUIET=1
    # ;;
    # -s|--shatter)
    # SHATTER=1
    # ;;
    -sat=*)
    SOLVER="${arg#*=}"
    ;;
    -lb=*)
    LOWER_BOUND=${arg#*=}
    ;;
    -up=*)
    UPPER_BOUND=${arg#*=}
    ;;
    esac
done


echo "----------- [ Start ] -----------"

# RUN Shatter and/or SAT solver
cd ./Rado_CNFs
# make clean >> log.txt
make >> log.txt

echo "Running solver..."


# checking bounds bound
echo "Checking upper bound..."
./mapleSCIP.sh $UPPER_BOUND $k $A >> log.txt
FILE=$(find . -name "*.cnf")
UPPER_CNF=${FILE:2}
./satch -q $FILE > $FILE.txt
SAT_TEST=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

if [[ $SAT_TEST -eq 0 ]]
then # satisfiable
    echo "Upper bound too low."
    echo "Rado number for $A with $k-coloring is > $UPPER_BOUND."
    # clean up
    clean_up
    exit 0
fi


echo "Checking lower bound..."

python3 ./Rado_sub_py.py $k $LOWER_BOUND $UPPER_CNF
FILE=$(find . -name "*n$LOWER_BOUND.cnf")

./satch -q $FILE > $FILE.txt
SAT_TEST=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

if [[ $SAT_TEST -eq 1 ]]
then # unsatisfiable
    echo "Lower bound too High."
    echo "Rado number for $A with $k-coloring is <= $LOWER_BOUND."
    # clean up
    clean_up
    exit 0
fi


# Searching
echo "Searching..."

while [ $UPPER_BOUND -ge $LOWER_BOUND ]
do
    MID=$((($LOWER_BOUND+$UPPER_BOUND)/2))
    echo $MID
    # Checking satisfiable or not


    python3 ./Rado_sub_py.py $k $MID $UPPER_CNF
    FILE=$(find . -name "*n$MID.cnf")

    ./satch -q $FILE > $FILE.txt
    SAT=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

    if [[ $SAT -eq 0 ]]
    then # satisfiable
        LOWER_BOUND=$(($MID+1))
    else # unsatisfibale
        ANS=$MID
        UPPER_BOUND=$(($MID-1))
        UPPER_CNF=${FILE:2}
    fi
done

clean_up

if [[ $ANS -eq -1 ]]
then # satisfiable
    echo "Cannot find Rado number."
    exit 0
fi

echo "----------- [ Results ] ----------"
echo "Rado number for $A with $k-coloring is $ANS."
echo "----------- [ Done ] -------------"
exit 0
