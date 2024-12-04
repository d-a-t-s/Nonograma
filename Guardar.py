import pickle
import os

#La idea es que dentro del archivo matrices.pkl se guarde una lista que dentro contendrá listas la cuales contienes las tres matrices correspondienes a un nonograma

def guardar_matriz(matriz_solution, matriz_states, matriz_paleta):
    cont = 0
    if os.path.exists('matrices.pkl'):
        lista = cargar_matriz('matrices.pkl')

        for elemento in lista:
            if elemento[0] == matriz_solution and elemento[1] == matriz_states and elemento[2] == matriz_paleta:
                break
            elif elemento[0] == matriz_solution and elemento[1] != matriz_states and elemento[2] == matriz_paleta: #Condicional en caso de que el usuario quiera guardar una partida que ya habia guardado antes
                elemento[0] = matriz_solution
                elemento[1] = matriz_states
                elemento[2] = matriz_paleta
                break

            else:
                cont+=1

        if cont == len(lista):
            lista.append([matriz_solution, matriz_states, matriz_paleta])

    else:
        lista = [[matriz_solution, matriz_states, matriz_paleta]]

    with open('matrices.pkl' , 'wb') as archivo:
        pickle.dump(lista, archivo)

def cargar_matriz(archivo):
    with open(archivo, 'rb') as a:
        matriz = pickle.load(a) 
    return matriz
