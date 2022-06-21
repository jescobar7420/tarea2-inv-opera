import random
from math import e

ARCHIVO1 = "QAP_sko56_04_n.txt"
ARCHIVO2 = "QAP_sko100_04_n.txt"
T_TERMINO = 0.2


def leer_archivo(archivo):
    list = []
    try:
        with open(archivo, "r") as a:
            list = a.read().split("\n")
    except FileExistsError:
        print("Archivo no encontrado.")
    return list


def dividir_tam_locales(datos):
    tam_locales = []
    tam_locales = datos[1].split(",")
    tam_locales = pasar_a_entero(tam_locales)
    return tam_locales


def dividir_cant_locales(datos):
    return int(datos[0])


def pasar_a_entero(lista):
    return [int(x) for x in lista]


def dividir_personas_esperadas(datos):
    list_cant_personas = []
    i = 2 # Donde comienza los datos de cantidad de gente esperada en los locales

    for i in range(2, len(datos)-1):
        row = datos[i].split(",")
        row = pasar_a_entero(row)
        list_cant_personas.append(row)

    return list_cant_personas


def calcular_distancia(i, j, tam_locales):
    suma = 0
    for k in range(i+1, j):
        suma += tam_locales[k]
    suma += (tam_locales[i]/2) + (tam_locales[j]/2)
    return suma


def calcular_esfuerzo(n, tam_locales, lista_cant_personas):
    suma = 0
    for i in range(n-1):
        for j in range(i+1, n):
            distancia = calcular_distancia(i, j, tam_locales)
            suma += distancia + lista_cant_personas[i][j]
    return suma


def criterio_aceptacion(mejor_puntaje, nuevo_puntaje, T):
    ds = nuevo_puntaje - mejor_puntaje

    if ds < 0:
        return True
    if T==0:
        return False

    p = e**(-ds/T)
    random_prob = random.random()

    if random_prob < p:
        return True

    return False


def swap(lista_cant_personas, tam_locales, n):
    a = None
    b = None
    while True:
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)
        if a != b:
            break
    
    # Swap en los tamanios de los locales
    copy_tam = tam_locales[a]
    tam_locales[a] = tam_locales[b]
    tam_locales[b] = copy_tam
    
    # Swap en la lista de personas esperadas
    for i in range(n):
        copy_pers = lista_cant_personas[i][a]
        lista_cant_personas[i][a] = lista_cant_personas[i][b]
        lista_cant_personas[i][b] = copy_pers


def criterio_termino(T, T_TERMINO):
    if T < T_TERMINO:
        return False
    return True
            

def main():
    # Parametros
    alfa = 0.9
    T = 15000

    input_usuario = None
    datos = None

    # Elegir instancia
    while input_usuario != 1 and input_usuario != 2:
        input_usuario = input('Elegir instancia. [1/2]: ')
        if input_usuario == '1':
            input_usuario = 1
            datos = leer_archivo(ARCHIVO1)
        elif input_usuario == '2':
            input_usuario = 2
            datos = leer_archivo(ARCHIVO2)

    # Parametros
    n = dividir_cant_locales(datos) # Cantidad de locales
    tam_locales = dividir_tam_locales(datos) # Tamanio de los locales
    lista_cant_personas = dividir_personas_esperadas(datos) # Cantidad de gente esperada por local
    
    # Solucion inicial
    mejor_vecindario = lista_cant_personas
    mejor_tam_locales = tam_locales
    mejor_puntaje = calcular_esfuerzo(n, mejor_tam_locales, mejor_vecindario)

    while criterio_termino(T, T_TERMINO):
        nuevo_vecindario = mejor_vecindario
        nuevo_tam_locales = mejor_tam_locales
        swap(nuevo_vecindario, nuevo_tam_locales, n)
        nuevo_puntaje = calcular_esfuerzo(n, nuevo_tam_locales, nuevo_vecindario)
        
        if criterio_aceptacion(mejor_puntaje, nuevo_puntaje, T):
            mejor_puntaje = nuevo_puntaje
            mejor_vecindario = nuevo_vecindario
            mejor_tam_locales = nuevo_tam_locales
        
        T *= alfa
        print("Temperatura actual: {}".format(T))
    
    print("Mejor puntaje: {}".format(mejor_puntaje))
    print("Mejor vecindario:\n{}\n{}".format(mejor_tam_locales, mejor_vecindario))
    

if __name__ == '__main__':
    main()
