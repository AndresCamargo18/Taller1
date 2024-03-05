# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 21:12:39 2024

@author: Andres Camargo
"""
import random 
import os
#Función que pide el valor de las resistencias
def PedirValor():    
    while True:
        r=input("Ingrese el valor de la resistencia: ")
        cadena="".join(r.split())        
        try:
            r=float(cadena)
            break
        except ValueError:
            try: 
                numero=float(cadena[0:len(cadena)-1:1])                
                sufijo=cadena[len(cadena)-1]
                if sufijo=='K': #Sufijo K debe ser en mayuscula
                    r=numero*1000
                    break
                elif sufijo=='M': #Sufijo M debe ser en mayuscula
                    r=numero*1000000
                    break
                else:
                  print("El valor de resistencia reportado no es valido, intentalo de nuevo")   
            except ValueError:
                print("El valor de resistencia reportado no es valido, intentalo de nuevo")         

    return r

#Función que pide el valor de la fuente
def PedirFuente():
    
    while True:
        try:
            V=float(input("Ingrese el valor de la fuente (V): "))
            break
        except ValueError:
            print('El voltaje de la fuente ingresado no es valido, intentalo de nuevo')
    print(f'(V{V})->')       
    return V    
        
#Función que imprime el circuito y calcula el valor de la resistencia
def ArregloResistencias(V):
    
    r_total=0
    numeracion_R=0
    circuito=f'(V{V})->'
    
    while True:
        
        if numeracion_R==0: #Inicialmente se debe ingresar una resistencia en serie porque no hay otra para hacer paralelo y no se puede cerrar el circuito sin resistencia.
            tipoderesistencia='a'
        else:    
            while True:
                print('Qué desea hacer a continuación')
                print('A. Añadir resistencia en serie')
                print('B. Añadir resistencia en paralelo')
                print('C. Cerrar circuito')
                tipoderesistencia=input("Ingrese la opción deseada: ")
                tipoderesistencia=tipoderesistencia.strip()
                tipoderesistencia=tipoderesistencia.lower()
                if tipoderesistencia=='a' or tipoderesistencia=='b' or tipoderesistencia=='c': #Validando las opcion seleccionada
                    break
                else:
                    print("Opción no valida. Intentelo de nuevo")
        
        if tipoderesistencia=='a': #Añadiendo resistencia en serie
            r_paralelo=0
            numeracion_R+=1
            print(f'R{numeracion_R} en serie:')
            r_nueva=PedirValor()
            r_total+=r_nueva
            circuito+=f'-|-RS{r_nueva}-|->'
            r_anterior=r_nueva
            #print(r_total)
            
        elif tipoderesistencia=='b':            #Añadiendo resistencia en paralelo
            numeracion_R+=1                                   
            print(f'R{numeracion_R} en paralelo:')
            r_nueva=PedirValor()
            
            if r_paralelo==0: # Dos resistencias en paralelo
                r_total-=r_anterior
                r_paralelo=r_nueva*r_anterior/(r_nueva+r_anterior)
                for i in range(len(circuito)): 
                    if circuito[len(circuito)-1-i]=='S' or circuito[len(circuito)-1-i]=='P':
                        if circuito[len(circuito)-1-i]=='S':
                            circuito=circuito[::-1]
                            circuito=circuito.replace('S', 'P',1)            
                            circuito=circuito[::-1]
                        break
            else: # Más de dos resistencias en paralelo
                r_total-=r_paralelo
                r_paralelo=r_nueva*r_paralelo/(r_nueva+r_paralelo)
            #print(r_paralelo)
            
            #Sumando la resistencia en paralelo    
            r_total+=r_paralelo
            circuito=circuito[:-4]
            circuito=circuito+f'/{r_nueva}-|->'
            r_anterior=r_nueva
            #print(r_total)  
            
        else: #Cierre del circuito
            break
        print('Circuito parcial')    
        print(circuito)
           
        
        
    circuito+='---(GND)' #Añadiendo la tierra
    
    #Impresión del circuito
    print('\nCircuito final\n')
    print(circuito)       
    return r_total
 
#Función que añade sufijos a los valores para su impresión
def sufijos(X):
    if X/1e-6<1000:
         X=round(X/1e-6,2)  
         X=f'{X} micro'
    elif X/1e-3>=1 and X/1e-3<1000:
         X=round(X/1e-3,2)   
         X=f'{X} mili' 
    elif X/1e3>=1 and X/1e3<1000:
         X=round(X/1e3,2)
         X=f'{X} Kilo'
    elif X/1e6>=1:
         X=round(X/1e6,2)
         X=f'{X} Mega'
    else:       # Si no lleva prefijo solo redondear
        X=round(X,2)
    return X   

print("El siguiente programa tiene como función permitirle al usuario construir un circuito electrico paso a paso , añadiendo resistencias en serie o paralelo y especificando el valor de la fuente de voltaje. Al final el programa dará una representación equematica del circuito y la resistencia total y la corriente resultante\n")

V=PedirFuente()
R=ArregloResistencias(V)
tol=random.uniform(-0.05, 0.05)
R=round((1+tol)*R, 2)
I=V/R

V=sufijos(V)
R=sufijos(R)
I=sufijos(I)

print(f'\nVoltaje de la fuente: {V} Voltios')
print(f'El sistema presenta una tolerancia de: {round(tol*100,2)}%')
print(f'La resistencia total del circuito es: {R} Ohmios')
print(f'La corriente total en el circuito es: {I} Amperios')
       


            
        