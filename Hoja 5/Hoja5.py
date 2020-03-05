#universidad del valle de Guatemala
#carlos Alberto Raxtum ramos
#carne 19721
#basado de los ejemplos del libro y los subido a canvas
import simpy
import random

#Definicion de variables
InstrucT = 3 
memoria_ram= 100
cant_procesos = int(input("Ingrese la cantidad de procesos"))
t_total=0 
tiempos=[] 


principal = simpy.Environment()  
cpu = simpy.Resource (principal, capacity=2) 
ram = simpy.Container(principal, init=memoria_ram, capacity=memoria_ram) 
espera = simpy.Resource (principal, capacity=2)

def proceso(principal, tiempo, nombre, ram, memoria, cant_ins, InstrucT):
   
    global t_total
    global tiempos
    
    yield principal.timeout(tiempo)
    print('tiempo: %f - %s (new) son %d de memoria ram' % (principal.now, nombre, memoria))
    tiempo_al_llegar = principal.now 

    yield ram.get(memoria)
    print('tiempo: %f - %s (admited) su solicitud a sido aceptada por %d de memoria ram' % (principal.now, nombre, memoria))

    #almacenara el numero de instrucciones completadas
    ins_complete = 0
    
    while ins_complete < cant_ins:

    
        #se pide conexion con compu (ready)
        with cpu.request() as req:
            yield req
            if (cant_ins-ins_complete)>=InstrucT:
                efectuar=InstrucT
            else:
                efectuar=(cant_ins-ins_complete)

            print('tiempo: %f - %s (ready) la compu ejecutara %d instrucciones' % (principal.now, nombre, efectuar))
            #tiempo de ejecucion con el numero(efectuar) de instrucciones a ejecutar
            yield principal.timeout(efectuar/InstrucT)

            #Se guarda el numero total de instrucciones completadas
            ins_complete += efectuar
            print('tiempo: %f - %s (runing) compu (%d/%d) completado' % (principal.now, nombre, ins_complete, cant_ins))

        atender = random.randint(1,2)

        if atender == 1 and ins_complete<cant_ins:
            #(waiting)
            with espera.request() as req2:
                yield req2
                yield principal.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (entrada/salida)' % (principal.now, nombre))
    
    #cantidad de ram que retorna
    yield ram.put(memoria)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (principal.now, nombre, memoria))
    t_total += (principal.now - tiempo_al_llegar) 
    tiempos.append(principal.now - tiempo_al_llegar) 


# Crear semilla para random 
random.seed(1997)
rango = 1 


# Se creean los procesos a simular
for i in range(cant_procesos):
    tiempo = random.expovariate(1.0 / rango)
    cant_ins = random.randint(1,1)
    memoria = random.randint(1,1) 
    principal.process(proceso(principal, tiempo, 'Proceso %d' % i, ram, memoria, cant_ins, InstrucT))

# llama a la funcion
principal.run()

#resultado del tiempo
print (" ")
prom=(t_total/cant_procesos)
print('El tiempo promeido es: %f' % (prom))

