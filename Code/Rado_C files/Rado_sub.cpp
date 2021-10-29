#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

using namespace std;
int max_limit = 0;

string create_file_name(int n, int k, string large_file_name){
    
    size_t index;
    for(index = 0; index < large_file_name.size(); index++){
        if(large_file_name[index] == 'n'){
            break;
        }
    }

    // new file name
    string file_name = large_file_name.substr(0, index);
    file_name = file_name + "n" + to_string(n) + ".cnf";

    return file_name;

}


bool below_limit(string line){

    int value;
    stringstream ss(line);
    while(ss >> value){

        if (value < 0){
            value = value * -1;
        }

        if(value > max_limit){
            return false;
        }
    }
    return true;
}

int extract_sub_formula(string file_name, string large_file_name){

    int count = 0;
    ifstream original(large_file_name);
    ofstream file(file_name, ofstream::trunc);
    
    string line;
    // skip first parameter line
    getline(original, line);
    while (getline(original, line)){
        if(below_limit(line)){
            file << line + "\n";
            count++;
        }
        
    }
    original.close();
    file.close();
    return count;
}

void create_file(string file_name, int num_literal, int num_clauses){
    ofstream file(file_name, ofstream::trunc);
    file << "p cnf " + to_string(num_literal) + " " + to_string(num_clauses) + "\n";
    file.close();
}



int main(int argc, char **argv){

    // Note: The program does not check for edge cases!
    int k,n,num_clauses; 
    string file_name;
    string new_file_name;

    if(argc == 1 || argc != 4){ 
        std::cout << "Rado_sub: k n file.cnf" << std::endl;
        return 1;
    }else{
        k = std::atoi(argv[1]);
        n = std::atoi(argv[2]);
        file_name = std::string(argv[3]);
    }

    max_limit = n*k;
    new_file_name = create_file_name(n,k,file_name);

    num_clauses = extract_sub_formula("temp.txt", file_name);
    create_file(new_file_name, (k*n), num_clauses);
    return 0;
}