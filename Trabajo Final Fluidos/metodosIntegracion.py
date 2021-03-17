from visual import *
from particula import *
import operacionesVectoriales


#Definicion de Euler mediante un metodo

def MetodoEuler(posicion, velocidad, aceleracion, pasoTiempo):
    pIni=posicion
    vIni=velocidad
    aIni=aceleracion
    salto=pasoTiempo
    
    #Calculos a mano
    """
    pFin=(pIni+(((salto*0.5)*salto)*aIni))+(vIni*salto)
    vFin=vIni+(salto*aIni)
    """

    #Calculos haciendo uso de operacionesVectoriales
    escaladoAuxiliar = operacionesVectoriales.escalarVector(salto,aIni)
    vFin = vIni + escaladoAuxiliar
    
    termAceleracion = operacionesVectoriales.escalarVector((0.5 * salto),escaladoAuxiliar)
    termVelocidad = operacionesVectoriales.escalarVector(salto, vIni)
    
    pFin = pIni + (termVelocidad + termAceleracion)
    
    #Control de decelaracion por si se pasa
    if (vFin.y > 4.5):
            vFin.y = 0.85 * vFin.y

    return [pFin,vFin]

