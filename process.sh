#!/bin/bash

# Defaults
QUIET=0
SHATTER=0
SAT=0
SAT_TEST=0
SOLVER="satch"
LOWER_BOUND=0
UPPER_BOUND=0
MID=0
ANS=-1
k=$1 # colorings
A=$2 # system of equation

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

n=$LOWER_BOUND

echo "----------- [ Start ] ----------"

# RUN Shatter and/or SAT solver
cd ./Rado_CNFs


echo "Running solver..."

# ./mapleSCIP.sh 500 3 [2,-2,-7]


# check upper bound
echo "Checking upper bound..."
./mapleSCIP.sh $UPPER_BOUND $k $A >> log.txt
FILE=$(find . -name "*.cnf")
./satch -q $FILE > $FILE.txt
SAT_TEST=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

if [[ $SAT_TEST -eq 0 ]]
then # satisfiable
    echo "Upper bound too low."
    echo "Rado number for $A with $k-coloring is > $UPPER_BOUND."
    exit 0
fi

# clean up
rm -f *.cnf
rm -f *.cnf.txt


# Searching
echo "Searching..."

while [ $UPPER_BOUND -ge $LOWER_BOUND ]
do
    MID=$((($LOWER_BOUND+$UPPER_BOUND)/2))
    echo $MID
    # Checking satisfiable or not
    ./mapleSCIP.sh $MID $k $A >> log.txt
    FILE=$(find . -name "*.cnf")
    ./satch -q $FILE > $FILE.txt
    SAT=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

    if [[ $SAT -eq 0 ]]
    then # satisfiable
        LOWER_BOUND=$(($MID+1))
    else # unsatisfibale
        ANS=$MID
        UPPER_BOUND=$(($MID-1))
    fi

    # clean up
    rm -f *.cnf
    rm -f *.cnf.txt
done

if [[ $ANS -eq -1 ]]
then # satisfiable
    echo "Cannot find Rado number."
    exit 0
fi

echo "" > log.txt
echo "----------- [ Results ] ----------"
echo "Rado number for $A with $k-coloring is = $ANS."
echo "----------- [ Done ] -------------"
exit 0


# for FILE in *.cnf
# do

#     if [[ $QUIET -eq 0 ]]
#     then
#         echo "---- [ $FILE ] -------------------"
#         ./SAT $FILE
#         ./SAT $FILE > ../$2/$FILE.txt
#         echo ""
#     else
#         ./SAT -q $FILE > ../$2/$FILE.txt
#     fi
# done

# for FILE in *.cnf
# do
#     SAT=$(grep -c 'UNSATISFIABLE' ../$2/$FILE.txt)
#     if [[ $SAT -eq 0 ]]
#     then
#         echo "$FILE is satisfiable"
#     else
#         echo "$FILE is unsatisfiable"
#     fi
# done
