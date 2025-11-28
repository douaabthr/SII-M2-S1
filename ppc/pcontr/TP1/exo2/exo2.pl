
homme(ali).
homme(hacene).
homme(hakim).
homme(mohamed).
homme(said).
homme(samir).

femme(djamila).
femme(fatma).
femme(houria).
femme(lilia).
femme(linda).

pere(mohamed,samir).
pere(samir,lilia).
pere(samir,said).
pere(said,hacene).
pere(said,linda).
pere(hakim,ali).

mere(fatma,samir).
mere(houria,lilia).
mere(houria,said).
mere(lilia,ali).
mere(djamila,hacene).
mere(djamila,linda).

parent(X,Y):-pere(X,Y).
parent(X,Y):-mere(X,Y).

fils(X,Y):-homme(X),parent(Y,X).

fille(X,Y):-femme(X),parent(Y,X).

enfant(X,Y):-parent(Y,X).

grandpere(X,Y):-pere(X,Z),pere(Z,Y).

grandmere(X,Y):-mere(X,Z),mere(Z,Y).

frere(X,Y):- X\=Y,homme(X),parent(Z,X),parent(Z,Y).

soeur(X,Y):- X\=Y,femme(X),parent(Z,X),parent(Z,Y).

frere_ou_sere

tante






%dif(x,y) or \x = y or x \= y  (= est un predicat)
% vriables a guche et a droite --> quantifiees universellement
% a droite : existentiellemnt
% OR: 2 predicats

%  les femmes : femme(X)
% homme et pere