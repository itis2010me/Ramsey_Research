
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <stdlib.h>
#include <fstream>

std::string SCIP_file = "tempSCIPsols.txt";


// return n choose k, only for integer values
int choose(int n, int k){
    if (k == 0){
        return 1;
    }else {
        return (n * choose(n-1, k-1)) / k;
    }
}

std::string generate_file_name(std::string A, int k, int n, int num_SCIP_solutions){
    // assume equation in the form of [1,1,-1], k = 2, n = 4
    // we want "rado_1_1_-1_k2_n4.cnf"

    std::string equation = A.substr(1, A.length()-2);
    std::string file_name = "rado_";

    std::stringstream ss(equation);
    while(ss.good()){
        std::string value;
        std::getline(ss, value, ',');
        file_name = file_name + value + "_";
    }
    file_name = file_name + "k" + std::to_string(k) + "_n" + std::to_string(n)\
    + ".cnf"; 

    // insert the parameter line
    std::ofstream file(file_name, std::ofstream::trunc);
    int num_literal = n * k;
    int num_clauses = n + ((num_SCIP_solutions-1) * k) + (choose(k,2) * n);
    file << "p cnf " + std::to_string(num_literal) + " " + std::to_string(num_clauses)\
    + "\n";
    file.close();

    return file_name;
}

std::string generate_negative_clause(std::vector<int> solution, int k){

    // for solution 2 1 1 -> 2 = 1 + 1
    // for each color, there would be -z -x -y

    std::string clauses = "";
    std::string subclause = "";
    for(int c = (k-1); c >= 0; c--){
        std::string subclause;
        for(size_t index = 0; index < solution.size(); index++){
            subclause = subclause + "-" +\
            std::to_string((solution[index]*k)-c) + " ";
        }
        subclause = subclause + "0 \n";
        clauses = clauses + subclause;
    }

    return clauses;
}

// void prepare_parameter_line(int num_literal, int num_clauses, std::string file_name){
//     std::ofstream file(file_name, std::ofstream::trunc);
//     file << "p cnf " + std::to_string(num_literal) + " " + std::to_string(num_clauses)
//     + "\n";
//     file.close();
// }

void write_positive_clauses(std::string file_name, int k, int n){

    std::ofstream file(file_name, std::ofstream::app);
    int index = 1;
    int i,j;
    for(i = 1; i <= n; i++){
        for(j = 1; j <= k; j++){
            file << std::to_string(index++) + " ";
        }
        file << "0 \n";
    }
    file.close();
}

void write_negative_clauses(std::string file_name, int k){
    std::ifstream SCIP(SCIP_file);
    std::ofstream file(file_name, std::ofstream::app);
    if(!SCIP){
        std::cerr << "Cannot open SCIP file" << std::endl;
        exit(1);
    }
    std::string line;
    // skip first line
    std::getline(SCIP, line);
    while(std::getline(SCIP, line)){
        // remove end ", 0"
        line = line.substr(0,line.length()-3);
        std::vector<int> solution;
        std::stringstream ss(line);
        std::string value;
        std::getline(ss, value, ',');
        while(ss.good()){
            std::getline(ss, value, ',');
            solution.emplace_back(std::stoi(value));
        }
        file << generate_negative_clause(solution, k);
    }

    // close the files
    SCIP.close();
    file.close();
}

void write_optional_clauses(std::string file_name, int k, int n){

    std::ofstream file(file_name, std::ofstream::app);
    int i,j,q;
    for(i = 1; i <= n; i++){

        for(j = 1; j <= k-1; j++){

            for(q = j+1; q <= k; q++){
                file << "-"+std::to_string(i*k-(k-j)) + " "\
                + "-"+std::to_string(i*k-(k-q)) + " 0 \n";
            }
        }
    }
    file.close();
}


int main(int argc, char **argv){

    // k for number of colours, n for range [1,n]
    int k,n;
    std::string A; 
    std::string file_name;
    // int num_clauses = 0;
    int num_SCIP_solutions;


    if(argc == 1 || argc != 5){ 
        std::cout << "RadoCG: k n A num_SCIP_solutions" << std::endl;
        return 1;
    }else{
        k = std::atoi(argv[1]);
        n = std::atoi(argv[2]);
        A = std::string(argv[3]);
        num_SCIP_solutions = std::atoi(argv[4]);
    }

    file_name = generate_file_name(A,k,n,num_SCIP_solutions);
    write_positive_clauses(file_name, k, n);
    write_negative_clauses(file_name, k);
    write_optional_clauses(file_name, k, n);

    return 0;
}