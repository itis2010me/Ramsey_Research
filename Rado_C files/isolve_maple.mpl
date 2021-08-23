
isolve_Maple := proc(A) local output, filename; output := convert(isolve(x*A[1] + y*A[2] + z*A[3] = 0, {i, j}), string); filename := "isolve_maple.txt"; fopen(filename, WRITE); writeline(filename, output); fclose(filename); end proc;


