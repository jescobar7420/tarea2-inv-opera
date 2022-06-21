"""
    Investigación de Operaciones - PUCV
    Tarea 2
    Autores: Javier Escobar - Diego Riveros
"""

# Librerias
import random
from math import e

# Constantes
FILE1 = "QAP_sko56_04_n.txt"
FILE2 = "QAP_sko100_04_n.txt"
T_END = 0.2
MAX_ITER = 8000


def read_file(file):
    list = []
    try:
        with open(file, "r") as a:
            list = a.read().split("\n")
    except FileExistsError:
        print("Archivo no encontrado.")
    return list
    

def get_n_stores(data):
    # En la posición 0 de la lista 'data' se encuentra el número de locales
    return int(data[0])


def get_size_stores(data):
    # En la posición 1 de la lista 'data' se encuentra el tamanio de los locales
    size_stores = []
    size_stores = data[1].split(",")
    size_stores = pass_an_int(size_stores)
    return size_stores


def pass_an_int(list):
    # Transforma la lista de string a integer
    return [int(x) for x in list]


def get_neighborhood(data):
    list_neighborhood = []
    # Crea una matriz/lista de listas con el vecindario
    for i in range(2, len(data)-1):
        row = data[i].split(",")
        row = pass_an_int(row)
        list_neighborhood.append(row)
    return list_neighborhood


def calculate_distance(i, j, size_stores):
    # Calcula la distancia que existe entre un local A al local B
    sum = 0
    for k in range(i+1, j):
        sum += size_stores[k]
    sum += (size_stores[i]/2) + (size_stores[j]/2)
    return sum


def calculate_efford(n, size_stores, list_neighborhood):
    # Calcula el esfuerzo del cliente en caminar de un puesto a otro
    sum = 0
    for i in range(n-1):
        for j in range(i+1, n):
            distance = calculate_distance(i, j, size_stores)
            sum += distance + list_neighborhood[i][j]
    return sum


def acceptance_requirements(best_score, new_score, temperature):
    ds = new_score - best_score
    # En caso de que el nuevo puntaje sea mejor que el actual, se acepta directamente
    if ds < 0:
        return True
    if temperature==0:
        return False

    # En caso contrario, se usa el criterio de metrópolis
    p = e**(-ds/temperature)
    random_prob = random.random()

    if random_prob < p:
        return True
    return False


def swap(list_neighborhood, size_stores, n_stores):
    a = 0
    b = 0
    # Intercambiar dos locales aleatoriamente
    while a == b:
        a = random.randint(0, n_stores-1)
        b = random.randint(0, n_stores-1)
    
    # Swap en los tamanios de los locales
    copy_tam = size_stores[a]
    size_stores[a] = size_stores[b]
    size_stores[b] = copy_tam
    
    # Swap en la lista de personas esperadas
    for i in range(n_stores):
        copy_pers = list_neighborhood[i][a]
        list_neighborhood[i][a] = list_neighborhood[i][b]
        list_neighborhood[i][b] = copy_pers


def ending_requirement(temperature):
    # Criterio de termino de las iteraciones
    if temperature < T_END:
        return False
    return True
            

def main():
    input_user = None
    data = None

    # Elegir instancia
    while input_user != 1 and input_user != 2:
        input_user = input('Elegir instancia. [1/2]: ')
        if input_user == '1':
            input_user = 1
            data = read_file(FILE1)
        elif input_user == '2':
            input_user = 2
            data = read_file(FILE2)

    # Parametros
    n_stores = get_n_stores(data) # Cantidad de locales
    size_stores = get_size_stores(data) # Tamanio de los locales
    list_neighborhood = get_neighborhood(data) # Cantidad de gente esperada por local
    alfa = 0.9
    temperature = 15000
    
    # Solucion inicial
    best_neighborhood = list_neighborhood
    best_size_stores = size_stores
    best_score = calculate_efford(n_stores, best_size_stores, best_neighborhood)

    # Hacer iteraciones hasta que se cumpla el criterio de termino o llegue al máximo de iteraciones
    i = 0
    while ending_requirement(temperature) and i < MAX_ITER:
        # Crear nueva solución con swap de la solución anterior
        new_neighborhood = best_neighborhood
        new_size_stores = best_size_stores
        swap(new_neighborhood, new_size_stores, n_stores)
        new_score = calculate_efford(n_stores, new_size_stores, new_neighborhood)
        
        # Comparar puntajes obtenidos
        if acceptance_requirements(best_score, new_score, temperature):
            best_score = new_score
            best_neighborhood = new_neighborhood
            best_size_stores = new_size_stores
        
        # Disminuir temperatura por cada iteración
        temperature *= alfa
        i += 1
        print("Temperatura actual: {}".format(temperature))
    print("Mejor puntaje: {}".format(best_score))
    print("Mejor vecindario:\n{}\n{}".format(best_size_stores, best_neighborhood))
    

if __name__ == '__main__':
    main()
