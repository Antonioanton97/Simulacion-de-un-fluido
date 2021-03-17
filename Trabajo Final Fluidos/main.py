from visual import *
from struct import *
from particula import *
from metodosIntegracion import *
from gestorColisiones import *
from sistemaParticulas import *
from dinamica import *
import metodosIntegracion
import generaColumna
import exportadorBIN_RF
import vecinosHash
import operacionesVectoriales



#Implementacion de la ventana de simulacion

scene = display(title="SPH", width=500, height=500, x=0, y=0, center = (1./2.,1./2.,1./2.), forward = (129.620536, 3.904938, 123.748005) )
scene.autoscale = False

scene.forward # position
scene.center # look up

#Genero la caja
caja = box(pos=(0.15,0.0,0.9), length=4.5, height=3.0, width=2.0)
caja.opacity=0.1

#Genero los limites de la caja que serviran para mi motor de colisiones
colision = Colision(caja)

#Generamos la particula
masa=0.1
densidad=1000
radio=0.01
color=color.blue
separacion=0.015
nParticulasX=15
nParticulasY=15
nParticulasZ=15

posInicial=vector(-0.5,0.0,0.75)
vInicial=vector(0.0,-4.0,0.3)

#Generamos una lista de particulas en columna
print("Generando las particulas")
listParticulas=generaColumna.generaColumna(posInicial, masa, nParticulasX, nParticulasY, nParticulasZ, densidad, separacion, vInicial, radio, color)
print("Columna generada")

#Numero de particulas total
nParticulas=len(listParticulas)

#Genero mi sistema de particulas como un objeto de esa clase
sistemaP = SistemaParticulas()
sistemaP.setSistemaParticulas(listParticulas)

#Variables auxiliares
aceleracion = vector(0.0,-9.81, 0.0)
pasoTiempo = 0.01
cont = 0
tasaAmortiguamiento = 0.8
distanciaBS=0.6
k = 600
espesor=0.06

#Interaccion con el usuario
print("Seleccione el metodo de simulacion que desea implmentar")
print("Para ello introduzca un numero entero con una de estas dos opciones")
selector1 = input("Fuerza bruta (1) || SPH (0)   : ")
while(selector1!=0 and selector1!=1):
    print("Error, por favor eliga uno de estos dos metodos")
    selector1 = input("Fuerza bruta (1) || SPH (0)   : ")
    

if selector1==1:

    
    #-------------------#
    #Bucle de simulacion:
    #-------------------#

    
    #Interaccion con el usuario de Simulacion por fuerza bruta
    print("Seleccione el metodo de busqueda de vecinas que desea implmentar")
    print("Para ello introduzca un numero entero con una de estas dos opciones")
    selector = input("Fuerza bruta (1) || Hash (0)   : ")
    while(selector!=0 and selector!=1):
        print("Error, por favor eliga uno de estos dos metodos")
        selector = input("Fuerza bruta (1) || Hash (0)   : ")
    

        
    fuerzaInterna = Dinamica(sistemaP, distanciaBS)                   #Creo la clase dinamica
                
    while cont < 3000:
        rate(100)
        print ('Estoy en el paso: ' +repr(cont))
        
        if selector == 0:                                             #POR FUERZA BRUTA#
                vecinosHash.calculaVecinas(sistemaP, distanciaBS)        
            
        else:                                                         #POR HASH#
            #vecinosHash.calculaVecinas(sistemaP, distanciaBS)         
            lista = []
            for i in range(sistemaP.getNumeroParticulas()):
                lista.append(sistemaP.getParticula(i))

            vecinosHash.calculaVecinosHash(lista, distanciaBS)
                

        #Dinamica de mi bucle   
        fuerzaInterna.calculaFuerzasInternas(k)                        #Calculo las fuerzas internas
        
        for i in range(sistemaP.getNumeroParticulas()):
            particula_i = sistemaP.getParticula(i)
             
            colision.motor(espesor,particula_i)

            if(particula_i.getEstadoColision() == True):
                particula_i.mover()
                particula_i.cambiaEstadoColision()

            else:           
                
                aceleracionParticula = operacionesVectoriales.escalarVector((1.0/masa),particula_i.getFuerzaInterna())+ aceleracion
                velParticula = particula_i.getVelocidad()
                posParticula = particula_i.getPosicion()            
                nuevaCinematica = metodosIntegracion.MetodoEuler(posParticula, velParticula, aceleracionParticula, pasoTiempo)
                particula_i.setPosicion(nuevaCinematica[0])
                particula_i.setVelocidad(nuevaCinematica[1])
                particula_i.mover()


        cont+=1

    print ('FIN DE LA SIMULACION EN BRUTO')



else:

    
    #--------------#
    #Simulacion SPH:
    #--------------#


    dominoSoportado = separacion * 1.08

    dinamicaSPH = Dinamica(sistemaP,dominoSoportado)

    inclist = ['colors.inc', 'stones.inc', 'woods.inc', 'metals.inc']

    # El valor del dominio soportado no debe superar el 120% de la distania inicial de las particulas
    contador_simulacion = 0
    frame = 0

    while(contador_simulacion < 6000):
        rate(300)

        print ('Estoy en el paso: '+repr(contador_simulacion))
        
        dinamicaSPH.calculaDinamica()
        
        for i in range(sistemaP.getNumeroParticulas()):
            particula_i = sistemaP.getParticula(i)
            
            colision.motor(espesor, particula_i)        
            
            if(particula_i.getEstadoColision() == False):
                posParticula=particula_i.getPosicion()
                velParticula=particula_i.getVelocidad()
                aceleracionParticula = operacionesVectoriales.escalarVector((1.0/masa),particula_i.getFuerzaInterna())+ aceleracion
                nuevaCinematicaSPH = metodosIntegracion.MetodoEuler(posParticula, velParticula, aceleracionParticula, pasoTiempo)
                particula_i.setPosicion(nuevaCinematicaSPH[0])
                particula_i.setVelocidad(nuevaCinematicaSPH[1])
                particula_i.mover()
                
            else:
                
                particula_i.mover()
                particula_i.resetEstadoColision()



        #EXPORTADOR            
        if(contador_simulacion%15==0):
            frame = frame + 1
            #nombreArchivo = 'frame_'+ str(frame).zfill(5)
            exportadorBIN_RF.exportar("frame", contador_simulacion/15, sistemaP, radio)

            
        contador_simulacion = contador_simulacion + 1
        



    print ("FIN DE LA SIMULACION POR SPH") 
        
