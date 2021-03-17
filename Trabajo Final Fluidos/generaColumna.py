from visual import *
from particula import *


def generaColumna(posInicial, masa, nParticulasX, nParticulasY, nParticulasZ, densidad, separacion, vInicial, radio, color):

    listaParticulas= []

    #Calculamos la nueva posicion de la particula separada 
    for k in range(nParticulasZ):
        #print k
        newZ= k*separacion
        #print newZ
        for j in range(nParticulasY):
            newY= j*separacion
            for i in range(nParticulasX):
                newX= i*separacion                
                newPos= vector(newX, newY, newZ)
                
                posicion= posInicial + newPos
                #print posicion
                #Con los datos calculados genramos la nueva particula
                particula= Particula(posicion, masa, densidad, vInicial, radio, color)

                #Y la anadimos a nuetsra lista
                listaParticulas.append(particula)

                
    return listaParticulas


#Otros metodos de generacion de particulas


def generaLineaParticulas(listaParticulas, posInicial, masa, densidad, numParticulas, coordenada, separacion, vInicial, radio, color):

    if coordenada == 'x':
        vectorIterador = vector(separacion,0.0,0.0)
    elif coordenada == 'y':
        vectorIterador = vector(0.0,separacion,0.0)
    else:
        vectorIterador = vector(0.0,separacion,0.0)
        
    for i in range(numParticulas):
        posicion = posInicial + i*vectorIterador
        particula = Particula(posicion, masa, densidad, vInicial, radio, color)
        listaParticulas.append(particula)

    return listaParticulas
        
