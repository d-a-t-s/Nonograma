def constraints(matriz):
    constraint_Y = list()
    constraint_X = list()
    constraints = list()
	
    counter = 0
	
	#Souciones horizontales
    for i in range(len(matriz)):
        tempList = []
        for j in matriz[i]:
            if j:
                counter += 1
            elif (counter):
                    tempList.append(counter)
                    counter = 0
        if (counter):
            tempList.append(counter)
            counter = 0
        constraint_X.append(tempList)
        
    #Soluciones verticales
    for i in range(len(matriz[0])):
        tempList = []
        for j in matriz:
            if j[i]:
                counter += 1
            elif (counter):
                tempList.append(counter)
                counter = 0
        if (counter):
            tempList.append(counter)
            counter = 0
        constraint_Y.append(tempList)
        
    #Solucion final
    constraints.append(constraint_Y)
    constraints.append(constraint_X)
    return constraints