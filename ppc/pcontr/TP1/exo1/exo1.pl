appartient(X,[X|_]).
appartient(X,[_,Y|L]):-appartient(X,[Y|L]).

premier(X,[X|_]).

dernier(X,[X]).
dernier(X,[_,Y|L]):-dernier(X,[Y|L]).

avantdernier(X,[X,_]).
avantdernier(X,[_,Y,Z|L]):-avantdernier(X,[Y,Z|L]).

supprimerk(1,[_|L],L).
supprimerk(K,[X,Y|L1],[X|L2]):-K2 is K-1, supprimerk(K2,[Y|L1],L2).

substitute(_,_,[],[]).
substitute(X,Y,[X|L1],[Y|L2]):-!,
            substitute(X,Y,L1,L2).
substitute(X,Y,[Z|L1],[Z|L2]):-substitute(X,Y,L1,L2).

longueur([],0).
longueur([_|L],K):-longueur(L,K2), K is K2+1. 


% on suppose qu il ya au moin un element
somme([X],X).
somme([X,Y|L],S):-somme([Y|L],S2), S is S2+X.

affiche1([]).
affiche1([X|L]):-write(X),nl(),affiche1(L).



affiche2([]).
affiche2([X|L]):-affiche2(L),write(X),nl().


pair([]).
pair([_,_|L]):-pair(L).


deuxocc(X,[X|L]):-!,
                appartient(X,L).
deuxocc(X,[_,Y|L]):-deuxocc(X,[Y|L]).


concat([],L,L).
concat([X|L1],L2,[X|L3]):-concat(L1,L2,L3).

palindrome([]).
palindrome([_]).
palindrome([X,Y|L]):-dernier(X,[Y|L]),
            longueur([Y|L],K),
            supprimerk(K,[Y|L],L2),
            palindrome(L2).






% dernier(X,[1,9,4])
% x=4 ; --> false, cuz theres one solution


% cant have multiple ! ??



% supprimerk(2,[1,2,3],L).
% reponse:L = [1, 3] .

% supprimerk(K,[1,2,3],L).
% reponse:K=1
%L = [1, 3] .    avenc COUPURE S ARRETE

% else ; and it gives the rest



