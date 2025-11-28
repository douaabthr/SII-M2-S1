suppRep([],[]).
suppRep([X|L1],[X|L2]):-suppToutes(X,L1,L3),suppRep(L3,L2).

suppToutes(_,[],[]).
suppToutes(X,[X|L1],L2):-!,suppToutes(X,L1,L2).
suppToutes(X,[Y|L1],[Y|L2]):-suppToutes(X,L1,L2).
%il faut que suppRep de L3 nous donne L2

% coupure donc 3 eme clause x!=y