:-use_module(library('clp/bounds')).
sudoku(Vars):-length(Vars,81),
                Vars in 1..9,
                cont_lignes(Vars),
                cont_colonnes(Vars,1),
                cont_carres(Vars,1),
                label(Vars).

cont_lignes([]).
cont_lignes(Vars):-length(Vars1,9),
                    append(Vars1,Vars2,Vars),
                    all_different(Vars1),
                    cont_lignes(Vars2).

cont_colonnes(_,10):-!.
cont_colonnes(Vars,I):-ext_colonnes(Vars,I,colonne),
                        all_different(colonne),
                        Iplus1 is I+1,
                        cont_colonnes(Vars,Iplus1).

ext_colonnes([],_,[]):-!.
ext_colonnes(Vars,I,[X|colonne]):-length(Vars1,9),
                append(Vars1,Vars2,Vars),
                Imoins1 is I-1,
                length(Vars3,Imoins1),
                append(Vars3,[X|_],Vars1),
                ext_colonnes(Vars2,I,colonne).


cont_carres(_,10):-!.
cont_carres(Vars,I):-ext_carre(Vars,I,Carre),
                        all_different(Carre),
                        Iplus1 is I+1,
                        cont_carres(Vars,Iplus1).
% 3 1er predit le 1 er ligne de care les 3 ligne suivant de code extrair 2 eme ligne de carre
ext_carre(Vars,I,[X1,X2,X3,X4,X5,X6,X7,X8,X9]):-
        debut0 is ((I-1) div 3)*27+((I-1) mod 3)*3,
        length(Vars1,debut0),
        append(Vars1,[X1,X2,X3|_],Vars),
        debut1 is debut0+9,
        length(Vars2,debut1),
        append(Vars2,[X4,X5,X6|_],Vars),
        debut2 is debut1+9,
        length(Vars3,debut2),
        append(Vars3,[X7,X8,X9|_],Vars).