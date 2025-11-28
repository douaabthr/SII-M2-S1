triSel([X],[X]).
trisel([X,Y|L1],[Z|L2]):-min(Z,[X,Y|L1]),suppOcc1(Z,[X,Y|L1],L3),triSel(L3,L2)
%triSel(L3,L2) l2 is the same in Z|L2
% suppocc1 supprimer la premiere occ de Z

min(Z,[Z]).
min(Z,[Y,T|L1]):-min(Z,[T|L1]),Z<Y,!.
min(Z,[Z,_|_]).


suppocc1(X,[X,L],L):-!.
suppocc1(X,[Y|L1],[Y|L2]):-suppocc1(X,L1,L2).