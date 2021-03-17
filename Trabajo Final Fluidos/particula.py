from visual import *

class Particula:

        def __init__(self, posInicial, masa, densidad, velocidad, radio, color):
                self.posicion=posInicial
                self.radio=radio
                self.color=color
                self.esfera=sphere(pos=self.posicion, radius=self.radio, color=self.color)
                self.velocidad=velocidad
                self.densidad=densidad
                self.masa=masa
                
                self.aceleracion=vector() #Este atributo lo calculamos mediante un metodo de la misma clase
                
                self.presion=0.0          #
                self.viscosidad=0.0       #Parametros encapsulados en la clase por convenencia

                self.listaVecina = []     #Atributo de lista de vecinas de cada particula(Modulo hash)

                self.estadoColision = False
                self.fuerzaInterna = vector(0.0,0.0,0.0)
                
        #--------------#
        #Modificadores:
        #--------------#

        def setPosicion(self, newPos):
                self.posicion=newPos

        def setRadio(self, newRad):
                self.radio=newRad

        def setColor(self, newCol):
                self.color=newCol

        def setVelocidad(self, newVel):
                self.velocidad=newVel

        def setDensidad(self,newDen):
                self.densidad=newDen

        def setAceleracion(self, newAcel):
                self.aceleracion=newAcel

        def setPresion(self,newP):
                self.presion=newP

        def setViscosidad(self,newVis):
                self.viscosidad=newVis

        def setListaVecinas(self, listaVecinas):
                self.listaVecina = listaVecinas

        def cambiaEstadoColision(self):
                if(self.estadoColision == True):
                    self.estadoColision = False
                else:
                    self.estadoColision = True
        def setFuerzaInterna(self,nuevafuerzaInterna):
                self.fuerzaInterna = nuevafuerzaInterna



        #------------#
        #Consultores:
        #------------#

        def getPosicion(self):
                return self.posicion
        
        def getRadio(self):
                return self.radio
        
        def getColor(self):
                return self.color
        
        def getVelocidad(self):
                return self.velocidad

        def getDensidad(self):
                return self.densidad

        def getAceleracion(self):
                return self.aceleracion

        def getListaVecinas(self):
                return self.listaVecina

        def getMasa(self):
                return self.masa
        
        def getPresion(self):
                return self.presion
    
        def getEstadoColision(self):
                return self.estadoColision
        def getFuerzaInterna(self):
                return self.fuerzaInterna


    

        #--------------------#
        #Metodos de la clase:
        #--------------------#

        def mover(self):
                self.esfera.pos = self.posicion

        def calculaAceleracion(self):
                densidad=self.getDensidad()
                if(densidad==0):
                        fGravedad= vector(0.0,-9.81,0.0)
                        fPresion= vector(0.0,0.0,0.0)
                        fViscosidad= vector(0.0,0.0,0.0)
                else:
                        fGravedad= densidad * vector(0.0,-9.81,0.0)
                        fPresion= self.getPresion()
                        fViscosidad= self.getViscosidad()

                aceleracion= fGravedad + fPresion + fViscosidad
                return aceleracion


        #Por si con el cambiaEstado no quedaba claro
        def activaEstadoColision(self):
                self.estadoColision = True

        def resetEstadoColision(self):
                self.colisiona = False

        def resetVecina(self):
                self.listaVecinas = []
