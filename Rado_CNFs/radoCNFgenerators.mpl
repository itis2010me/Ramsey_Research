
with(combinat);
with(ListTools);
pairs := proc(m, n) local i, j, L; L := []; for i to m do for j to n do L := [op(L), v[i, j]]; end do; end do; return L; end proc;
tuples := proc(n, k) local i, L, M, s; if k = 1 then return [seq(i, i = 1 .. n)]; end if; if 1 < k then L := []; M := tuples(n, k - 1); for s in M do for i to n do L := [op(L), [op(s), i]]; end do; end do; return L; end if; end proc;
posClauses := proc(n, k) local allClauses, i, clause, j; allClauses := []; for i to n do clause := []; for j to k do clause := [op(clause), v[i, j]]; end do; allClauses := [op(allClauses), clause]; end do; return allClauses; end proc;
negClauses := proc(n, k, A) local allClauses, numVars, tuple, sum, i, lastVar, color, clause; allClauses := []; numVars := numelems(A); for tuple in tuples(n, numVars - 1) do sum := 0; for i to numVars - 1 do sum := sum + A[i]*tuple[i]; end do; lastVar := -sum/A[-1]; if type(lastVar, integer) and 1 <= lastVar and lastVar <= n then for color to k do clause := []; for i in tuple do clause := [op(clause), v[i, color]]; end do; clause := [op(clause), v[lastVar, color]]; allClauses := [op(allClauses), clause]; end do; end if; end do; return allClauses; end proc;
optClauses := proc(n, k) local allClauses, i, c1, c2; allClauses := []; for i to n do for c1 to k - 1 do for c2 from c1 + 1 to k do allClauses := [op(allClauses), [v[i, c1], v[i, c2]]]; end do; end do; end do; return allClauses; end proc;






generateRado := proc(n, k, A) local index, t, e, filename, f, i, clause, j, numVars, numClauses, clauseString, lit, positiveClauses, negativeClauses, optionalClauses, vectorString, a; index := 1; t := table(); for e in pairs(n, k) do t[e] := index; index := index + 1; end do; positiveClauses := posClauses(n, k); negativeClauses := negClauses(n, k, A); optionalClauses := optClauses(n, k); numVars := k*n; numClauses := numelems(positiveClauses) + numelems(negativeClauses) + numelems(optionalClauses); vectorString := ""; for a in A do vectorString := cat(vectorString, "_", convert(a, string)); end do; filename := cat("rado", vectorString, "_k", convert(k, string), "_n", convert(n, string), ".cnf"); f := fopen(filename, 'WRITE', 'TEXT'); writeline(filename, cat("p ", "cnf ", convert(numVars, string), " ", convert(numClauses, string))); for clause in positiveClauses do clauseString := ""; for lit in clause do clauseString := cat(clauseString, convert(t[lit], string), " "); end do; clauseString := cat(clauseString, "0"); writeline(filename, clauseString); end do; for clause in [op(negativeClauses), op(optionalClauses)] do clauseString := ""; for lit in clause do clauseString := cat(clauseString, convert(-t[lit], string), " "); end do; clauseString := cat(clauseString, "0"); writeline(filename, clauseString); end do; fclose(filename); end proc;

scanSCIPnegClauseOutput := proc(filename, numVars, numColors, varLimit) local f, formatString, i, line, allClauses, clauseVars, color, clause, var; f := fopen(filename, READ); formatString := "%*s"; for i to numVars do formatString := cat(formatString, "%d,"); end do; formatString := cat(formatString, "%*d"); line := readline(f); allClauses := []; while line <> 0 do line := readline(f); if line <> 0 then clauseVars := sscanf(line, formatString); if belowLimit(clauseVars, varLimit) then for color to numColors do clause := []; for var in clauseVars do clause := [op(clause), v[var, color]]; end do; allClauses := [op(allClauses), clause]; end do; end if; end if; end do; fclose(filename); return allClauses; end proc;
belowLimit := proc(L, limit) local isBelow, i; isBelow := true; for i in L do if limit < abs(i) then isBelow := false; end if; end do; return isBelow; end proc;
generateRadoSCIP := proc(n, k, A) local index, t, e, filename, f, i, clause, j, numVars, numClauses, clauseString, lit, positiveClauses, negativeClauses, optionalClauses, vectorString, a; index := 1; t := table(); for e in pairs(n, k) do t[e] := index; index := index + 1; end do; numVars := k*n; positiveClauses := posClauses(n, k); negativeClauses := scanSCIPnegClauseOutput("tempSCIPsols.txt", numelems(A), k, n); optionalClauses := optClauses(n, k); numClauses := numelems(positiveClauses) + numelems(negativeClauses) + numelems(optionalClauses); vectorString := ""; for a in A do vectorString := cat(vectorString, "_", convert(a, string)); end do; filename := cat("rado", vectorString, "_k", convert(k, string), "_n", convert(n, string), ".cnf"); f := fopen(filename, 'WRITE', 'TEXT'); writeline(filename, cat("p ", "cnf ", convert(numVars, string), " ", convert(numClauses, string))); for clause in positiveClauses do clauseString := ""; for lit in clause do clauseString := cat(clauseString, convert(t[lit], string), " "); end do; clauseString := cat(clauseString, "0"); writeline(filename, clauseString); end do; for clause in [op(negativeClauses), op(optionalClauses)] do clauseString := ""; for lit in clause do clauseString := cat(clauseString, convert(-t[lit], string), " "); end do; clauseString := cat(clauseString, "0"); writeline(filename, clauseString); end do; fclose(filename); end proc;


extractRadoSubformula := proc(cnf, n, k, numEqVars) local fileInfo, newFileName, i, g, newNumVars, line, oldNumClauses, newNumClauses, formatString, clauseVars; fclose(cnf); fopen(cnf, READ); fileInfo := sscanf(cnf, "%[rado_01234567890k-]%[n_]%d%[_0123456789.cnf]"); fileInfo[-2] := n; newFileName := ""; for i to numelems(fileInfo) do newFileName := cat(newFileName, convert(fileInfo[i], string)); end do; fclose(newFileName); g := fopen(newFileName, WRITE); newNumVars := n*k; line := readline(cnf); writeline(newFileName, line); oldNumClauses := op(sscanf(line, "%*s%*s%*d%*d")); newNumClauses := 0; formatString := ""; for i to max(k, numEqVars) do formatString := cat(formatString, "%d"); end do; line := readline(cnf); while line <> 0 do clauseVars := sscanf(line, formatString); if belowLimit(clauseVars, newNumVars) then newNumClauses := newNumClauses + 1; writeline(newFileName, line); end if; line := readline(cnf); end do; fclose(cnf); filepos(newFileName, 0); writeline(newFileName, cat("p cnf ", convert(newNumVars, string), " ", convert(newNumClauses, string))); fclose(newFileName); end proc;
convertListToString := proc(A) local vectorString, a; vectorString := ""; for a in A do vectorString := cat(vectorString, "_", convert(a, string)); end do; return vectorString; end proc;
generateZIMPLfile := proc(n, A) local numVars, filename, eqString, i; numVars := numelems(A); filename := "tempSCIPproblem.zpl"; fopen(filename, WRITE); writeline(filename, cat("var x[<i> in {1..", convert(numVars, string), "}] integer >=1 <=", convert(n, string), ";")); eqString := cat(convert(A[1], string), "*x[1]"); for i from 2 to numVars do eqString := cat(eqString, "+", convert(A[i], string), "*x[", convert(i, string), "]"); end do; eqString := cat(eqString, " == 0;"); writeline(filename, cat("subto avoidEq: ", eqString)); fclose(filename); end proc;
generateZIMPLfile(9, [1, 1, -1]);

