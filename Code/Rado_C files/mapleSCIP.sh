#bin/bash
STARTTIME=$(date +%s)
if [ "$#" -lt 4 ]; then
    echo "Usage: ./mapleSCIP.sh <number of integers> <number of colors> <vector determining equation> <symmetry_breaking_flag>"
    exit 0
fi

maple -i radoCNFgenerators.mpl -c "generateZIMPLfile($1,$3);" -c "quit;"
scip -q -c "set constraints countsols collect TRUE read tempSCIPproblem.zpl count write allsolutions tempSCIPsols.txt quit"
# maple -i radoCNFgenerators.mpl -c "generateRadoSCIP($1,$2,$3);" -c "quit;"

echo "SCIP done..."
ENDTIME=$(date +%s)
echo "SCIP took $(($ENDTIME - $STARTTIME)) seconds."
num_SCIP=$(wc -l < "tempSCIPsols.txt")
# ./RadoCG $2 $1 $3 $num_SCIP
python3 ./RadoCG_py.py $2 $1 $3 $num_SCIP $4

echo "Done"
