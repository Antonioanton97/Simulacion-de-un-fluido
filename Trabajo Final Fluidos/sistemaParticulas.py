from visual import *
from particula import *

class SistemaParticulas:

    def __init__(self):
        self.masa = 0.0
        self.sistemaParticulas = []
        self.radioParticula = 0.0

    def setMasaParticula(self, masa):
        self.masa = masa

    def agregaParticula(self,particula):
        self.sistemaParticulas.append(particula)
        
    def agregaParticulaIndex(self, particula, indice):
        self.sistemaParticulas.insert(indice,particula)
        
    def eliminaParticula(self,particula):
        self.sistemaParticulas.remove(particula)
        
    def eliminaParticulaPorIndice(self,indice):
        self.sistemaParticulas.pop(indice)
        
    #---------------------#
    #Metodos Modificacores:
    #---------------------#

        
    def permutaParticula(self, indicePermutacion, particula):
        self.sistemaParticulas.pop(indicePermutacion)
        self.sistemaParticulas.insert(indicePermutacion,particula)
    
    def setSistemaParticulas(self, nuevoSistemaParticulas):
        self.sistemaParticulas = nuevoSistemaParticulas

    def agregaSistemaParticulas(self, nuevoSistemaParticulas):
        nuevoNumeroParticulas = len(nuevoSistemaParticulas)
        for i in range(nuevoNumeroParticulas):
            particula_i = nuevoSistemaParticulas[i]
            self.sistemaParticulas.append(particula_i)
            
        
    #-------------------#
    #Metodos Consultores:
    #-------------------#
            

    def getMasaParticula(self):
        return self.masa
    
    def getParticula(self,indice):
        return self.sistemaParticulas[indice]
    
    def getIndiceParticula(self, particula):
        return self.sistemaParticulas.index[particula]
      
    def getNumeroParticulas(self):
        return len(self.sistemaParticulas)

    def getSistemaParticulas(self):
        return self.sistemaParticulas


    
        

