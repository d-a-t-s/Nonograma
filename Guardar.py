import pickle
import os

#La idea es que dentro del archivo matrices.pkl se guarde una lista que dentro contendrá listas la cuales contienes las tres matrices correspondienes a un nonograma

def guardar_matriz(matriz_solution, matriz_states, matriz_paleta):
    cont = 0
    if os.path.exists('matrices.pkl'):
        lista = cargar_matriz('matrices.pkl')

        for elemento in lista:
            if elemento[0] == matriz_solution and elemento[1] == matriz_states and elemento[2] == matriz_paleta:
                print("TODAS LAS MATRICES SON IGUALES")
                break
            elif elemento[0] == matriz_solution and elemento[1] != matriz_states and elemento[2] == matriz_paleta: #Condicional en caso de que el usuario quiera guardar una partida que ya habia guardado antes
                elemento[0] = matriz_solution
                elemento[1] = matriz_states
                elemento[2] = matriz_paleta
                break

            elif elemento[0] != matriz_solution and elemento[1] != matriz_states and elemento[2] != matriz_paleta:
                print("TODAS SON DISTINTAS")
                cont+=1
        if cont == len(lista):
            lista.append([matriz_solution, matriz_states, matriz_paleta])

        print("El archivo SI existe")
    else:
        print("El archivo NO existe")
        lista = [[matriz_solution, matriz_states, matriz_paleta]]

    with open('matrices.pkl' , 'wb') as archivo:
        pickle.dump(lista, archivo)

def cargar_matriz(archivo):
    with open(archivo, 'rb') as a:
        matriz = pickle.load(a) 
    return matriz

matriz1 = [[1,2],[3,4]]
matriz2 = [[5,6],[7,8]]
matriz3 = [[9,10],[11,12]]
matriz4 = [['a','b'],['c','d']]
matriz5 = [['e','f'],['g','h']]
matriz6 = [['i','j'],['k','l']]
matriz7 = [['p','p'],['p','p']]
matriz8 = [['p','p'],['p','p']]
matriz9 = [['p','p'],['p','p']]

#guardar_matriz(matriz1, matriz2, matriz3)
guardar_matriz(matriz4, matriz5, matriz6)
#guardar_matriz(matriz7,matriz8,matriz9)

#lista = cargar_matriz('matrices.pkl')

#print(lista)


#listita = [matriz1, matriz2, matriz3]
#print(listita[1])

#guardar_matriz(matriz1, matriz2, matriz3)
m1 = cargar_matriz('matrices.pkl')
print(m1)

#test = [[[[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]], [[19, 20, 21], [22, 23, 24], [25, 26, 27]]]]
#print("TEST: ")
#print(test[0][1])

