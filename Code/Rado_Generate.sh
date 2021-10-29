
STARTTIME=$(date +%s)
if [ "$#" -lt 4 ]; then
    echo "Usage: ./Rado_Generate.sh <number of integers> <number of colors> <vector determining equation> <symmetry_breaking_flag>"
    exit 0
fi

echo "" > isolve_maple.txt
echo "" > solutions.txt

/Library/Frameworks/Maple.framework/Versions/Current/bin/maple -i isolve_maple.mpl -c "isolve_Maple($3);" -c "quit;"

# python find_sol.py
python3 ./find_sol.py $1


echo "Solution generation done..."
ENDTIME=$(date +%s)
echo "Generation took $(($ENDTIME - $STARTTIME)) seconds."
num_sol=$(wc -l < "solutions.txt")
# ./RadoCG $2 $1 $3 $num_SCIP
python3 ./RadoCG_py.py $2 $1 $3 $num_sol $4

echo "Done"


