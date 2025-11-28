import nltk
import os

with open("TP1/exo1/text extraction/D_21.txt", "r", encoding="utf-8") as f:
    text = f.read()


# A SENETCE ENDS WITH A FULL STOP, A COMMA MARKS THE END OF A CLAUSE
ExpReg = nltk.RegexpTokenizer( 
    r'[^.\n]+'                    
                      
) 

senetences= ExpReg.tokenize(text)


save_dir = "TP1/exo1/text preprocessing"
filename = os.path.join(save_dir, f"S.txt")
with open(filename, "w", encoding="utf-8") as f:
    for s in senetences:
        f.write(f"{s}\n\n")
print(f"Saved vocab {filename}")
    