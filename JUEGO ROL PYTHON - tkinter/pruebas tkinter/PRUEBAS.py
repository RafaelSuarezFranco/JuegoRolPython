import random

r1 = []
for i in range(0,3):
    r1.append(random.randint(1, 20))

    
r2 = [] #dos tiradas para el enemigo, las guardamos ordenadas.
for i in range(0,2):    
    r2.append(random.randint(1, 25))
    #la dificultad aumenta o disminuye las probabilidades de ganar del monstruo.
 
print(r1)
r1 = sorted(r1, key=int, reverse=True)
print(r1)
"""
    
if (pjmax1 == enemax1 and pjmax2 == enemax2) or (pjmax1 > enemax1 and pjmax2 < enemax2) or (pjmax1 < enemax1 and pjmax2 > enemax2):
    resultado = "empate"
elif (pjmax1 > enemax1 and pjmax2 > enemax2) or (pjmax1 > enemax1 and pjmax2 == enemax2) or (pjmax1 == enemax1 and pjmax2 > enemax2):
    resultado = "ganar"
else:
    resultado = "perder"
    
"""