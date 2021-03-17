from visual import *
from particula import *
import operacionesVectoriales

class Colision:       #He creado el motor de colision como un metodo de la clase colision

    def __init__(self, caja):

        #Posicion de la caja
        posX=caja.pos.x
        posY=caja.pos.y
        posZ=caja.pos.z

        #Caculo de los limites de la caja(ampliamos estos limites para disminuir la probabilidad de particulas taravesando la pared), atributos de la clase
        self.limSupX = posX + (0.5*caja.length)
        self.limInfX = posX - (0.5*caja.length)
        
        self.limSupY = posY + (0.5*caja.height)
        self.limInfY = posY - (0.5*caja.height)
        
        self.limSupZ = posZ + (0.5*caja.width)
        self.limInfZ = posZ - (0.5*caja.width)
        #A diferencia del encunacido del problema del Tema 5, aqui no trabajamos con vectores




    #-------------------#
    #Metodo de colision:
    #-------------------#
        
    def motor(self, espesor, particula):
        
        #Variables auxiliares
        pos=particula.getPosicion()
        x=pos.x
        y=pos.y
        z=pos.z
        vel=particula.getVelocidad()
        acel= particula.getAceleracion()
        rad= particula.getRadio()
        #colisiona = False

        normal_x = vector(1.0,0.0,0.0)
        normal_y = vector(0.0,1.0,0.0)
        normal_z = vector(0.0,0.0,1.0)
        vectorNormal = vector(0.0,0.0,0.0)        

        
        #-----------------#
        #Logica del motor:
        #-----------------#
        

        #Control en X
        if(x<self.limInfX or x>self.limSupX):             #Si colisiona....
            particula.activaEstadoColision()
            vel.x=vel.x*(0.0)                             #La paramos en ese eje
            acel.x=acel.x*(0.0)
            if(x<self.limInfX):
                #colisiona=True
                #vecotorNormal=vectorNormal + normal_x
                particula.getPosicion().x=x+0.18*rad
            else:
                #colisiona = True
                #normal_x = -1.0 * normal_x
                #vectorNormal = vectorNormal + normal_x
                particula.getPosicion().x=x-0.18*rad
                

        #Control en Y
        if(y<self.limInfY or y>self.limSupY):
            particula.activaEstadoColision()
            vel.y=vel.y*(0.0)
            acel.y=acel.y*(0.0)
            if(y<self.limInfY):
                #colisiona = True
                #vectorNormal = vectorNormal + normal_y
                particula.getPosicion().y=y+0.18*rad
            else:
                #colisiona = True
                #normal_y = -1.0 * normal_y
                particula.getPosicion().y=y-0.18*rad
       

        #Control en Z
        if(z<self.limInfZ or z>self.limSupZ):
            particula.activaEstadoColision()
            vel.z=vel.z*(0.0)
            acel.z=acel.z*(0.0)
            if(z<self.limInfZ):
                #colisiona = True
                #vectorNormal = vectorNormal + normal_z
                particula.getPosicion().z=z+0.18*rad
            else:
                #colisiona = True
                #normal_z = -1.0 * normal_z
                #vectorNormal = vectorNormal + normal_z
                particula.getPosicion().z=z-0.18*rad


        """if colisiona ==True:
            particula.cambiaEstadoColision()
            self.respuestaColisionLimites(particula, vectorNormal, espesor)"""

        particula.setVelocidad(vel)
        particula.setAceleracion(acel)






    #--------------------#
    #Metodo de respuesta:
    #--------------------#
            
        
    def respuestaColisionLimites(self, particula, vectorNormal, espesor):
    
        #ESTA RESPUESTA ES VALIDA PARA LA COLISION POR LIMITES
        tasaRozamiento = 0.4
        tasaRebote = 0.4
        tasaPenetracion = 0.005 * espesor
        
        velocidadAuxiliar = particula.getVelocidad()
        modProyNormal = operacionesVectoriales.prodEscalar(velocidadAuxiliar,vectorNormal)
        velocidadNormal = operacionesVectoriales.escalarVector(modProyNormal, vectorNormal)
        velocidadTangencial = velocidadAuxiliar - velocidadNormal
                            
        respuestaNormal = operacionesVectoriales.escalarVector(tasaRebote,velocidadNormal)
        respuestaTangencial = operacionesVectoriales.escalarVector(tasaRozamiento, velocidadTangencial)
        velocidadRespuesta = respuestaNormal + respuestaTangencial
        particula.setVelocidad(velocidadRespuesta)
        toleranciaPosicion = operacionesVectoriales.escalarVector(tasaPenetracion, vectorNormal)
        nuevaPosicion = particula.getPosicion() + toleranciaPosicion
        particula.setPosicion(nuevaPosicion)
        
    

