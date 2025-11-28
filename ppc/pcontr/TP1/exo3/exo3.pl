fusion([],L,L):-!.
fusion(L,[],L):-!.
fusion([X|L1],[Y|L2],[X|L3]):-X<Y,!,fusion(L1,[Y|L2],L3).
fusion(L1,[Y|L2],[Y|L3]):-fusion(L1,L2,L3).



















