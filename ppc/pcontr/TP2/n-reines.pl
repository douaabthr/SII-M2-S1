:-use_module(library('clp/bounds')).
nReines(Vars,N):-length(Vars,N),
                Vars in 1..N, #defenire les domaine de chaque variable dans N
                all_different(Vars),
                cont_diag(Vars,1),
                label(Vars).

cont_diag([_],_):-!.
cont_diag([XI|Vars],I):-Iplus1 is I+1,
            distribuer(XI,Vars,I,Iplus1),
            cont_diag(Vars,Iplus1).

distribuer(_,[],_,_).
distribuer(XI,[XJ|Vars],I,J):-XI-XJ#\=I-J,
    XI-XJ#\=J-I,
    Jplus1 is J+1,
    distribuer(XI,Vars,I,Jplus1).

                                                       