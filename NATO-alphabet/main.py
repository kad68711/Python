import pandas

data=pandas.read_csv("nato_phonetic_alphabet.csv")


dict={}

dict={j.letter:j.code for i,j in data.iterrows()}
# for i,j in data.iterrows():
#     dict[j.letter]=j.code

asnwer=input("kotoba o haite kure").upper()

print(asnwer)

list=[dict[a] for a in asnwer ]

print(list)
    
    
  
