#!/bin/bash

# Defaults
QUIET=0
QUIET_FLAG=""
SAT_FLAG=""
SAT=0
SAT_TEST=0
SOLVER="satch"
LOWER_BOUND=$3
UPPER_BOUND=$4
UPPER_CNF=""
MID=0
ANS=-1
k=$1 # colorings
A=$2 # system of equation
sym_f=$5
STARTTIME=$(date +%s)

clean_up () {
    rm -f *.cnf
    rm -f *.cnf.txt
}

usage () {
cat << EOF
usage: ./process.sh k A lb up sym_f

k          Number of colors
A          Linear equation in 1 x n matrix form
lb         Lower bound for the Rado number
up         Upper bound for the Rado number
sym_f      Symmetry breaking flag, 0 -> turn off

-sat=      Select a SAT solver to opearte. Default to satch
-q|--quite Disable verbal response from SAT solver

Input for k A and bounds are not checked for correctness.
This process script will use binary search to search for the Rado number 
of given settings.
EOF
  exit 0
}


if [ "$#" -lt 5 ]; then
    usage
fi

# Parse CLAs
for arg in "$@"
do
    case $arg in
    -q|--quiet)
    QUIET=1
    ;;
    -sat=*)
    SOLVER="${arg#*=}"
    ;;
    esac
done


echo "----------- [ Start ] -----------"

# setting the quiet flag
if [[ $QUIET -eq 1 ]]
then 
    if [[ $SOLVER == "satch" ]]
    then
        QUIET_FLAG="-q"
    elif [[ $SOLVER == "glucose" ]]
    then
        QUIET_FLAG="-verb=0"
    fi
fi

# set the glucose flag
if [[ $SOLVER == "glucose" ]]
then
    SOLVER="glucose-syrup"
    SAT_FLAG="-no-pre -asymm -nthreads=8"
fi

# RUN Shatter and/or SAT solver
cd ./Code
echo "" > log.txt

echo "Running solver..."


# checking bounds bound
echo "Checking upper bound..."
./Rado_Generate.sh $UPPER_BOUND $k $A $sym_f >> log.txt
FILE=$(find . -name "*n$UPPER_BOUND.cnf")
UPPER_CNF=${FILE:2}
./$SOLVER $QUIET_FLAG $SAT_FLAG $FILE > $FILE.txt
SAT_TEST=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

if [[ $SAT_TEST -eq 0 ]]
then # satisfiable
    echo "Upper bound too low."
    echo "Rado number for $A with $k-coloring is > $UPPER_BOUND."
    # clean up
    clean_up
    echo "----------- [ Done ] -------------"
    ENDTIME=$(date +%s)
    echo "Time taken: $(($ENDTIME - $STARTTIME)) seconds."
    exit 0
fi


echo "Checking lower bound..."

python3 ./Rado_sub_py.py $k $LOWER_BOUND $UPPER_CNF
FILE=$(find . -name "*n$LOWER_BOUND.cnf")

./$SOLVER $QUIET_FLAG $SAT_FLAG $FILE > $FILE.txt
SAT_TEST=$(grep -c 'UNSATISFIABLE' ./$FILE.txt)

if [[ $SAT_TEST -eq 1 ]]
then # unsatisfiable
    echo "Lower bound too High."
    echo "Rado number for $A with $k-coloring is <= $LOWER_BOUND."
    # clean up
    clean_up
    echo "----------- [ Done ] -------------"
    ENDTIME=$(date +%s)
    echo "Time taken: $(($ENDTIME - $STARTTIME)) seconds."
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

    ./$SOLVER $QUIET_FLAG $SAT_FLAG $FILE > $FILE.txt
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
ENDTIME=$(date +%s)
echo "Time taken: $(($ENDTIME - $STARTTIME)) seconds."
exit 0
