from visual import *
from particula import *
from vecinosHash import *
import operacionesVectoriales

class Dinamica:


    def __init__(self, sistemaParticulas, h):
        self.sistemaParticulas = sistemaParticulas
        self.numeroParticulas = sistemaParticulas.getNumeroParticulas()
        self.distancia = h

        #Variables auxiliares (Atributos de mi clase para implementar en mis metodos)
        self.cteGases = 1000.0 * sistemaParticulas.getParticula(0).getMasa() 
        self.Densidad = 1000
        self.viscosidad=0.36

        
    def calculaDinamica(self):
        lista=self.sistemaParticulas.getSistemaParticulas()
        calculaVecinosHash(lista, self.distancia)
        self.calculaFuerzasPSPH(self.distancia,self.viscosidad)
        #self.calculaFuerzasInternas(self.distancia)
        #self.calculaAceleracion()

        
    #----------------------#
    #Metodos FuerzaDinamica:
    #----------------------#

        
        
    def calculaFuerzaSPH(self):
        
        #Calcula la fuerza mediante el metodo SPH
        
        for i in range(self.numeroParticulas):                              #Para cada particula del sistema de particulas (particula_i)
            particula_i = self.sistemaParticulas.getParticula(i)
            posicion_i = particula.getPosicion()                            #Obtener la posicion de la particula_i 
            desnsidadpart_i = calculaDensidad(particula_i)                  #Calcular la densidad (metodo calculaDensidad)
            fuerzaPre = calculaFuerzaPresion(particula_i)                   #Calcular la fuerza de presion (metodo calculaFuerzaPresion)
            fuerzaVisc = calculaFuerzaViscosidad(particula_i)               #Calcular la fuerza de viscosidad (metodo calculaFuerzaViscosidad)
            fuerzaInt = fuerzaPre + fuerzaVisc
            particula_i.setFuerzaInterna(fuerzaInt)                         #Sumar ambas fuerzas internas y actualizar la fuerza interna de la particula_i.

        #NOTA: Metodo Void 


    def calculaFuerzasInternas(self,k):

        #PARTICULA = i      PARTICULASVECINAS = j

        for i in range(self.numeroParticulas):
            particula_i = self.sistemaParticulas.getParticula(i)             #Para cada particula del sistema de particulas (particula_i)
            particulaVecinas_i = particula_i.getListaVecinas()               #Obtener lista de particulas vecinas y conocer su numero
            numVecinas_i=len(particulaVecinas_i)
            posicion_i = particula_i.getPosicion()                           #Obtener la posicion de la particula_i
            fuerzaInternaTotal = vector(0.0,0.0,0.0)                         #Inicializamos la Finterna

            for j in range (numVecinas_i):
                particula_j = particulaVecinas_i[j]                          #Para cada una de las particulas vecinas (particula_j)
                posicion_j = particula_j.getPosicion()                       #Obtener la posicion de la particula_j

                vectorRes = posicion_j - posicion_i                          #Calcular la distancia entre ambas posiciciones y el vector director.
                modVectorRes = mag(vectorRes)
                vectorUnitario = vectorRes/modVectorRes
                modVectorUnitario = mag(vectorUnitario)

                aux = modVectorRes - self.distancia
                fuerzaInterna = operacionesVectoriales.escalarVector(aux, vectorUnitario)   #Efectuar el sumatorio de la fuerza interna de la particula_i
                fuerzaInternaTotal = fuerzaInternaTotal + fuerzaInterna

            particula_i.setFuerzaInterna ((-k*fuerzaInternaTotal))         #cuando se hayan hecho los calculos para todas las particulas vecinas, actualizar la fuerza interna de la particula_i.  #Seteamos la fuerza en la particula

        #NOTA: Metodo VOID
            


    def calculaFuerzasPSPH(self,K,viscosidad):
        
        for i in range(self.numeroParticulas):                                  #Para cada particula del sistema de particulas (particula_i)
            fuerzaTotal = vector(0.0,0.0,0.0)
            particula_i = self.sistemaParticulas.getParticula(i)
            vecinas = particula_i.getListaVecinas()                             #Obtener lista de particulas vecinas y conocer su numero
            nVecinas = len(vecinas)
            
            posicion_i = particula_i.getPosicion()                              #Obtener la posicion de la particula_i
            fuerzaPresion = vector(0.0,0.0,0.0)
            fuerzaViscosidad = vector(0.0,0.0,0.0)                              #Incializamos las fuerzas aux
            fuerzaGravedad = particula_i.getMasa() * vector(0.0,-9.81,0.0)
            for j in range(nVecinas):
                particula_j = vecinas[j]                                        #Para cada particula del sistema de veinas (particula_j)
                posicion_j = particula_j.getPosicion()                          #Obtener la posicion de la particula_j
                direccion = posicion_j - posicion_i                             #Calcular la distancia entre ambas posiciciones y el vector director.
                distancia = mag(direccion)
                direccion = operacionesVectoriales.escalarVector((1.0/distancia),direccion)
                

                #Controlamos en caso de que la distancia sea menor que la dada
                if distancia < self.distancia:
                    incremento = distancia - self.distancia
                    modulo = K * incremento * self.gradKernel(distancia)
                    fPresion = vector(0.0,0.0,0.0)
                    fPresion.x = (modulo*0.6) * direccion.x
                    fPresion.y = (modulo*0.75) * direccion.y
                    fPresion.z = (modulo*0.6) * direccion.z
                    fuerzaPresion = fuerzaPresion + fPresion
                else:
                    incremento = distancia - self.distancia
                    modulo = K * incremento * self.gradKernel(distancia)
                    fPresion = vector(0.0,0.0,0.0)
                    fPresion.x = (modulo*0.08) * direccion.x
                    fPresion.y = (modulo*0.15) * direccion.y
                    fPresion.z = (modulo*0.08) * direccion.z
                    fuerzaPresion = fuerzaPresion + fPresion

                                
                #Ahora la viscosidad
                velRel = particula_i.getVelocidad() - particula_j.getVelocidad()          #Calculo de la fuerza relativa
                modProyectado = velRel.dot(direccion)
                velRel = operacionesVectoriales.escalarVector(modProyectado,direccion)
                
                fViscosidad = viscosidad * velRel                                         #Calculo de Fuerza de viscosidad
                #fViscosidad = operacionesVectoriales.escalarVector(viscosidad,velRel)
                fuerzaViscosidad = fuerzaViscosidad + fViscosidad
            

            fuerzaTotal = fuerzaPresion + fuerzaViscosidad + fuerzaGravedad      #Fuerza Total
            particula_i.setFuerzaInterna(fuerzaTotal)                            #Seteamos la fuerzaTotal  

           
        #NOTA: Metodo VOID




    #-----------------#
    #Metodos Atributos:
    #-----------------#

            

    def calculaDensidad(self,particula_i):
        
        #PARTICULA = i      PARTICULASVECINAS = j
        
        for i in range(self.numeroParticulas):
            particula_i = self.arrayParticulas[i]
            posicion1 = particula_i.getPosicion()
            vecinas = particula_i.getListaVecinas()
            numVecinas = len(vecinas)
            
            rho_i = 0.0   #inicializar rho_i(rho_i es un escalar)
            
            for j in range(numVecinas):
                particula_j = vecinas[j]
                posicion2 = particula_j.getPosicion()
                masa_j = particula_j.getMasa()                  #Obtener la masa de la particula_j
                Wij = self.KernelMuller(posicion1, posicion2)   #Formular la funcion kernel recomendada
                rhoAux = masa_j * Wij                           #Calcular, para cada vecina, el producto de la masa y la funcion kernel
                rho_i = rho_i + rhoAux
            particula_i.setDensidad(rho_i)                      #Cuando se haya terminado el sumatorio actualizar la densidad de la particula_i

        #NOTA: la densidad rho_i sera una atributo que hay que anadir a la clase particula.
            

    def calculaPresion(self, rho_i):
        
        diferencia = rho_i-self.Densidad
        Presion_i = self.cteGases * diferencia
        
        return Presion_i

    #La viscosidad esta por defecto a 0.36 pero metemos un modificador para hacer el problema mas generico
    def setViscosidad(self, nuevaViscosidad):

        self.viscosidad = nuevaViscosidad

    #------------------#
    #Metodos FuerzasAux:
    #------------------#    
    
    """
    CALCULO DE FUERZAPRESION PASANDOLE LA VECINA
    def calculaFuerzaPresion(self, particula_i, particula_j):

        rho_i = particula_i.getDensidad()                               #Saco sus densidades
        rho_j = particula_j.getDensidad()
        
        if(rho_i == 0.0 or rho_j == 0.0):                               #En el caso de (0,0)c la Fpresion vale 0
            FuerzaPresion_i = (0.0,0.0,0.0)
            
            return FuerzaPresion_i
        
        else:
            posicion_i = particula_i.getPosicion()
            posicion_j = particula_j.getPosicion()

            gradWij = self.gradKernelMuller(posicion_i, posicion_j)     #Formular la funcion kernel recomendada
            #Variables auxiliares para operar
            presion_i = self.calculaPresion(rho_i)                      #Calculo sus presiones a traves de un modulo porpio
            presion_j = self.calculaPresion(rho_j)
            rho_i2 = rho_i * rho_i
            rho_j2 = rho_j * rho_j
            aux = (presion_i/rho_i2) + (presion_j/rho_j2)
            aux = aux * particula_j.getMasa()       
            
            FuerzaPresion_i = termino * gradWij                         #Calcular la fuerza Fpresion.
            
            return FuerzaPresion_i                                      #Cuando se hayan hecho los calculos para todas las particulas vecinas, devolver el valor de dicha fuerza
        
        
        
        #Si esa distancia es inferior a self.distanca entonces 
        
        #NOTA: return FuerzaPresion_i
    """
    #CALCULO DE FUERPRESION SIN PASARLE LA VECINA
    def calculaFuerzaPresion(self,particula_i):
        
        vecinas = particula_i.getListaVecinas()                      #Sacamos las vecinas
        numVecinas = len(vecinas)

        FuerzaPresion_i = (0.0,0.0,0.0)                              #Inicializamos Fpresion

        for j in range(numVecinas):
            particula_j = vecinas[j]
            k = 2650                                                 #Cte de la formula Fpresion
            
            rho_i = particula_i.getDensidad()                        #Sacamos las densidades
            rho_j = particula_j.getDensidad()

            if(rho_i == 0.0 or rho_j ==0.0):
                FuerzaPresion_i = (0.0,0.0,0.0)
                
                return FuerzaPresion_i                               #Si es (0,0) la Fpresion es 0
            
            else:
                masa_j = particula_j.getMasa()
                suma_densiadades = rho_i + rho_j
                
                if( rho_i > rho_j):
                    posicion_i = particula_i.getPosicion()
                    posicion_j = particula_j.getPosicion()
                    wij = self.gradKernelMuller(posicion_i,posicion_j)
                    #Operaciones
                    f = (masa_j*(suma_densidades/(2*rho_i)))
                    s = operacionesVectoriales.escalarVector(f,wij)
                    FuerzaPresion_i = FuerzaPresion_i + s
                    
                else:
                    posicion_i = particula_i.getPosicion()
                    posicion_j = particula_j.getPosicion()
                    wij = gradKernelMuller(posicion_i,posicion_j)
                    #Operaciones
                    f = (masa_j*(suma_densidades/(2*rho_j)))
                    s = operacionesVectoriales.escalarVector(f,wij)
                    FuerzaPresion_i = FuerzaPresion_i + s

        #FuerzaPresion_i = -k * FuerzaPresion_i
        FuerzaPresion_i = operacionesVectoriales.escalarVector(-k,FuerzaPresion_i)
        
        return FuerzaPresion_i

    """
    CALCULO DE FUERZAVISC PASANDOLE LA VECINA
    def calculaFuerzaViscosidad(self, particula_i, particula_j):
        
        rho_i = particula_i.getDensidad()                              #Saco sus densidades
        rho_j = particula_j.getDensidad() 
        
        if(rho_i == 0.0 or rho_j == 0.0):
            FuerzaViscosidad_i = (0.0,0.0,0.0)                         #Si es (0,0) la Fvisc es 0

            return FuerzaViscosidad_i
        else:
            posicion_i = particula_i.getPosicion()
            posicion_j = particula_j.getPosicion() 
            laplWij = self.laplKernelMuller(posicion_i, posicion_j)    #Formular la funcion kernel recomendada
            velocidad_i = particula_i.getVelocidad()
            velocidad_j = particula_j.getVelocidad()
            rho_i2 = rho_i * rho_i
            rho_j2 = rho_j * rho_j
            #Calculos (a mano)
            aux = ( (self.Viscosidad/rho_i2) * velocidad_i + (self.Viscosidad/rho_j2) * velocidad_j )
            aux = aux * particula_j.getMasa()
            
            FuerzaViscosidad_i = aux * laplWij                          #Calcular la fuerza Fvisc
            
            return FuerzaViscosidad_i 
        

        #NOTA: return FuerzaViscosidad_i
"""
    
    #CALCULO DE FUERZAVISC SIN PASARLE LA VECINA
    def calculaFuerzaViscosidad(self,particula_i,viscosidad):
        
        vecinas = particula_i.getListaVecinas()                  #Calculo de vecinas
        posicion_i = particula_getPosicion()
        numVecinas = len(vecinas)
        velocidad_i = particula_i.getVelocidad()

        FuerzaViscosidad_i=(0.0,0.0,0.0)                         #Inicializamos Fvisc
        for j in range (numVecinas):
            particula_j = vecinas[j]
            masa_j = particula_j.getMasa()
            velocidad_j  = particula_j.getVelocidad()
            #Calculos
            r = velocidad_i - velocidad_j
            s = masa_j/2
            Wij = self.laplKernelMuller(posicion_i, posicion_j)
            aux = operacionesVectoriales.escalarVector(s,r)
            aux2 = operacionesVectoriales.escalaVector(Wij,aux)
            FuerzaViscosidad_i = FuerzaViscosidad_i + aux2
            
        #FuerzaViscosidad_i = viscosidad * FuerzaViscosidad_i     #La Fvisc es el producto de la viscosidad por el vector fuerza calculado
        FuerzaViscosidad_i = operacionesVectoriales.escalarVector(viscosidad,FuerzaViscosidad_i) 
        return FuerzaViscosidad_i


    
    #--------------#
    #Metodos Kernel:
    #--------------#

    def KernelMuller(self, posicion_i, posicion_j):
        mod_r = mag(posicion_j-posicion_i)
        alpha = 1.08 * math.pow(self.h,2)
        h_septima = math.pow(self.h,7)
        h_cuadrado = math.pow(self.h,2)
        r_cuadrado = math.pow(mod_r,2)
        resta = h_cuadrado - r_cuadrado
        resta_cubo = math.pow(resta,3)
        wij = ((alpha*315)/(64*math.pi*h_septima))*resta_cubo
       
        return Wij
    
    def gradKernelMuller(self, posicion_i, posicion_j):
        mod_r = mag(posicion_j - posicion_i)
        vect_r = (posicion_j-posicion_i)/mod_r
        beta = 1.768 * self.h
        h_quinta = math.pow(self.h,5)
        h_cuadrado = math.pow(self.h,2)
        r_cuadrado = math.pow(mod_r,2)
        resta = h_cuadrado - r_cuadrado
        resta_cuadrado = math.pow(resta, 2)
        
        gradKernel = ((beta*15)/(math.pi*h_quinta))*resta_cuadrado *vect_r  
    
        return gradKernel
    
    def laplKernelMuller(self, posicion_i, posicion_j):

        mod_r = mag (posicion_j - posicion_i)
        y = 31.16
        h_cuadrado = math.pow(self.h,2)
        r_cuadrado = math.pow(mod_r,2)
        resta = h_cuadrado - r_cuadrado
        wij = ((y*318)/(7*math.pi*h_cuadrado))*resta

        return Wij

    def gradKernel(self, distancia):
        alpha = 3.18
        beta  = 2.12
        gamma = 0.85
        cota = self.distancia * 0.96

        inicial = (gamma + alpha)
        inicial = 2.0*(inicial - 2.0*beta)
        inicial = inicial / cota

        segundo = 2.0*((beta-alpha)/cota)
        segundo = segundo - ((0.5 * inicial)*cota)
        
        cuadratico = inicial * (distancia * distancia)
        lineal = segundo * distancia
        Wij = cuadratico + lineal
        Wij = Wij + alpha
        
        return Wij
