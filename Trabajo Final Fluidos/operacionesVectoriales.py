from visual import *
#se importa visual para tener acceso a las librerias numpy.

def escalarVector(escalar,vectorEntrada):
    x = vectorEntrada.x * escalar
    y = vectorEntrada.y * escalar
    z = vectorEntrada.z * escalar
    
    salida = vector(x, y, z)
    return salida

def prodEscalar(vector1,vector2):
    escalar = (vector1.x * vector2.x)+(vector1.y * vector2.y)+(vector1.z * vector2.z)
    return escalar
'''
def Verlet(aceleracion, velocidad, posicionPrevia, posicion, pasoTiempo):

    velocidad = velocidad +(aceleracion * pasoTiempo)
    nPosicion = (2.0 * posicion) - posicionPrevia
    posicion = nPosicion + ( aceleracion * (pasoTiempo * pasoTiempo))

    vectorEstado = [posicion,velocidad]

    return vectorEstado
'''   
    
