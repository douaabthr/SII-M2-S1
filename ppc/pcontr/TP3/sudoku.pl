:-use_module(library('clp/bounds')).
sudoku(Vars):-  length(Vars,81),
                Vars in 1..9,
                cont_lignes(Vars),
                cont_colonnes(Vars),
                cont_carres(Vars),
                label(Vars).
# verfier tout les lignes de sufoku si les valeur de avr d'un ligne donnes sont all diff        
#ici nous avons parcoru la matrice logne par ligne comme elle est stocke   
cont_lignes([]).
cont_lignes(Vars):-length(Vars1,9),
                    append(Vars1,Vars2,Vars),
                    all_different(Vars1),
                    cont_lignes(Vars2).

# ici on parcours colonne par colonne 
cont_colonnes([],_,[]):-!.
cont_colonnes(_,10):-!.
cont_colonnes(Vars,I):-ext_colonnes(Vars,I,colonne),
                        all_different(colonne),
                        Iplus1 is I+1,
                        cont_colonnes(Vars,Iplus1).

ext_colonnes(Vars,I,[X|colonne]):-length(Vars1,9),
                append(Vars1,Vars2,Vars),
                length(Vars3,I-1),
                append(Vars3,[X|_],Vars1),
                ext_colonnes(Vars2,I,colonne).
