import csv
 
lista = [["nombre", "apellidos", "grado"],
          ['Alex', 'Brian', 'A'],
          ['Tom', 'Smith', 'B']]
 
fichero = open('libro2.csv', 'w')
with fichero:
    csvescrito = csv.writer(fichero,delimiter = ';')
    csvescrito.writerows(lista)
     
print("ESCRITURA COMPLETA")