from visual import *
from struct import *
from particula import *
from sistemaParticulas import *




def exportar(Archivo, nFrame, sistemaParticulas, radioParticula):

        
	#numParticulas = len(sistemaParticulas)
	numParticulas = sistemaParticulas.getNumeroParticulas()
	name = Archivo + str(nFrame).zfill(5) +'.bin'
	archivo = open(name,'wb')
	crearCabecera(archivo, nFrame, numParticulas, radioParticula)

	
	for i in range(numParticulas):
                particula_i = sistemaParticulas.getParticula(i)
                posicion_i = particula_i.getPosicion()
                velocidad_i = particula_i.getVelocidad()
                
                x = posicion_i.x
                y = posicion_i.y
                z = posicion_i.z

                v_x = velocidad_i.x
                v_y = velocidad_i.y
                v_z = velocidad_i.z

                #[float]*3 ; particle position (XYZ-global)
                archivo.write(pack('fff', x, y, z))
                
                #[float]*3 ; particle velocity (XYZ)
                archivo.write(pack('fff', v_x, v_y, v_z))
                
                #[float]*3 ; particle force (XYZ)
                archivo.write(pack('fff', 0.0, 0.0, 0.0))

                #[float]*3 ; particle vorticity (XYZ) ;; version>=9
                archivo.write(pack('fff', 0.0, 0.0, 0.0))

                #[float]*3 ; normal vector (XYZ) ;; version>=3
                archivo.write(pack('fff', 0.0, 0.0, 1.0))
                
                #[int] ; number of neighbors ;; version>=4
                archivo.write(pack('i', 0))
                
                #[float]*3 ; Texture vector (UVW) ;; version>=5
                archivo.write(pack('fff', 0.0, 0.0, 0.0))
                
                #[short int] ; info bits ;; version>=5
                archivo.write(pack('h', 0))

                #[float] ; elapsed particle time (age)
                archivo.write(pack('f', 0.0))

                #[float] ; isolation time
                archivo.write(pack('f', 0.0))

                #[float] ; viscosity
                archivo.write(pack('f', 0.0))
                
                #[float] ; density
                archivo.write(pack('f', 1.0))

                #[float] ; pressure
                archivo.write(pack('f', 0.0))
                
                #[float] ; mass
                archivo.write(pack('f', 1.0))
                
                #[float] ; temperature
                archivo.write( pack('f', 0.0))
                
                #[int] ; particle ID ;; version<12 
                #archivo.write( 'i', 1 )
                
                #[uint64] ; particle ID ;; version>=12
                archivo.write(pack('i', 0))


        #necesario al final
	archivo.write(pack('i',0))
	archivo.write(pack('c',b'\x00'))
	archivo.write(pack('c',b'\x00'))
	archivo.close()
       
	        
        
    
        #archivo.write(pack('i', 0))
        
        

        

	
	

def crearCabecera(archivo, nFrame, numParticulas, radioParticula):

        nombreCabecera = 'ExportadorRF'
        
        archivo.write(pack('i',int('0xFABADA',0)))
        

        
        talla1 = len(nombreCabecera)
        talla2 = 250 - talla1
        archivo.write(nombreCabecera.encode())
        for i in range(1, talla2+1):
                archivo.write(pack('c',b'\x00'))

        #[short int] ; version (current = 13)
        archivo.write(pack('h', 9))

        #[float] ; scale scene
        archivo.write(pack('f', 1.0))

        #[int] ; fluid type
        archivo.write(pack('i', 9))

        #[float] ; elapsed simulation time
        archivo.write(pack('f', 0.0))

        #[int] ; frame number
        archivo.write(pack('i', nFrame))

        #[int] ; frames per second
        archivo.write(pack('i', 30))

        #[long int] ; number of particles
        archivo.write(pack('l', numParticulas))

        #[float] ; radius
        archivo.write(pack('f', radioParticula))

        #[float]*3 ; pressure (max, min, average)
        archivo.write(pack('fff', 0.0, 0.0, 0.0))

        #[float]*3 ; speed (max, min, average)
        archivo.write(pack('fff', 0.0, 0.0, 0.0))

        #[float]*3 ; temperature (max, min, average)
        archivo.write(pack('fff', 0.0, 0.0, 0.0))

        #[float]*3 ; emitter position ;; version>=7
        archivo.write(pack('fff', 0.0, 0.0, 0.0))

        #[float]*3 ; emitter rotation ;; version>=7
        archivo.write(pack('fff', 0.0, 0.0, 0.0))

        #[float]*3 ; emitter scale ;; version>=7
        archivo.write(pack('fff', 1.0, 1.0, 1.0))

        #archivo.close()
