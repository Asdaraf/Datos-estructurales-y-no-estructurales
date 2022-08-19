from datetime import date, datetime
from collections import defaultdict, deque

ARCHIVO = "ETHUSD.csv"

DICT_MESES = {
    "1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun",
    "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}


def cargar_archivo(archivo):

    with open(archivo, "r", encoding="utf-8") as file:
        diccionario_eth = dict()
        # enumarte es una función built-in de python que retorna una tupla de la seguinte forma (indice, valor) tal que el valor seria lo que ya estariamos iterando
        # mientras que el indice seria como si huberamos hecho antes del for i= 0 y a cada iteración sumar 1+ a ese valor.
        for i, line in enumerate(file):
            if i == 0:
                continue
            else:
                # Con eso ingnoramos la primea linea, ya que esa solo nos sirve para los datos del archivo
                date, open_, high, low, close, adj_close, volume = line.strip().split(",")
            # Aca estamos separando la linea por cada coma(,) del archivo, además de removendo el salto de linea
                diccionario_eth[date] = {
                    'open': open_, 'high': high,
                    'low': low, 'close': close,
                    'adj_close': adj_close, 'volume': volume
                }
        return diccionario_eth


if __name__ == '__main__':
    diccionario_eth = cargar_archivo(ARCHIVO)

# Consulta 1


def organizar_por_mes(diccionario_eth):

    organizador_mes = dict()
# transforma la fecha en formato date, obteniendo el valor del mes en 3 letras
    for x, y in diccionario_eth.items():
        fecha = x.strip().split("-")
        nuevaFecha = date(int(fecha[0]), int(fecha[1]), int(fecha[2]))
        nuevaFecha2 = date.strftime(nuevaFecha, '%b')
# crea un diccionario con todos los meses del año dejando una lista vacia
        for mes2 in DICT_MESES:
            if nuevaFecha2 == DICT_MESES[mes2]:
                organizador_mes[nuevaFecha2] = list()
# pasamos la fecha a una tupla
    for x, y in diccionario_eth.items():
        dia = dict()
        fecha = x.strip().split("-")
        tupla1 = int(fecha[0])
        tupla2 = int(fecha[1])
        tupla3 = int(fecha[2])
        fecha_tupla = (tupla1, tupla2, tupla3)
# volveemos a tener el mes en su abreviacion para ver si existe en diccionario final
        nuevaFecha = date(int(fecha[0]), int(fecha[1]), int(fecha[2]))
        nuevaFecha2 = date.strftime(nuevaFecha, '%b')
# obtenemos el diccionario con la tupla de fecha y los valores correspondiente a esa fecha y agregamos ese diccionario a la lista del mes correspondiente
        dia[fecha_tupla] = y
        if nuevaFecha2 in organizador_mes.keys():
            organizador_mes[nuevaFecha2].append(dia)

    print(organizador_mes)

# organizar_por_mes(diccionario_eth)

#################################################################################################################################################

# Consulta 2

# Funcion entrega el valor maximo y los ordena por la fecha mas reciente a la mas antigua. 

def valores_maximos_por_dia(diccionario_eth):
    valorMaximo = deque()

    for x, y in diccionario_eth.items():
        linea = {}
        dicc_deque = {}
        fecha = x
        linea = y
        for key, valor in linea.items():
            if key == 'high':
                valorAlto = valor
                dicc_deque[fecha] = valor
                valorMaximo.appendleft(dicc_deque) #Como el archivo CSV no cambia se usa este metodo para ordenarlo.

    print(valorMaximo)

# valores_maximos_por_dia(diccionario_eth)

#################################################################################################################################################

# #CONSULTA 3

def mejor_mes(diccionario_eth, year=None):
    promedio_meses = dict()
    # crea diccionario con los meses y años con una lista vacia
    for x in diccionario_eth.keys():
        fecha = x.split("-")
        añoMes = fecha[0]+"-"+fecha[1]
        promedio_meses[añoMes] = list()
    # agrega los valores maximos a las listas vacias de los meses correspondiente
    for x, y in diccionario_eth.items():
        fecha = x.split("-")
        añoMes = fecha[0]+"-"+fecha[1]
        if añoMes in promedio_meses:
            high_dia = y["high"]
            promedio_meses[añoMes].append(high_dia)
    # saca el promedio del mes y lo agrega al mes correspondiente
    for x, y in promedio_meses.items():
        suma = 0
        lista_suma = list()
        for i in y:
            if i == "null":
                continue
            else:
                suma += float(i)
                lista_suma.append(i)
                promedio = suma/len(lista_suma)
        promedio_meses[x] = promedio
    # evalua dependiendo del año entregado
    if year == None:
        valor_max = max(promedio_meses.values())
        key_max = max(promedio_meses.keys())

        print(
            f"El valor maximo de los años es {valor_max} de la fecha {key_max}")
    else:
        dicc = dict()
        for fecha, valor in promedio_meses.items():
            if str(year) in str(fecha):
                dicc[fecha] = valor
        valor_max = max(dicc.values())
        key_max = max(dicc, key=dicc.get) # https://es.stackoverflow.com/questions/407011/como-conseguir-el-key-con-el-valor-mas-alto-en-un-diccionario-en-python
        fecha = key_max.split("-")
        print(
            f"El valor maximo del año {year} es {valor_max} del mes {fecha[1]}")

# mejor_mes(diccionario_eth)
# mejor_mes(diccionario_eth, 2015)
# mejor_mes(diccionario_eth, 2016)
# mejor_mes(diccionario_eth, 2017)
# mejor_mes(diccionario_eth, 2018)
# mejor_mes(diccionario_eth, 2019)
# mejor_mes(diccionario_eth, 2020)
# mejor_mes(diccionario_eth, 2021)

diccionario_eth = cargar_archivo(ARCHIVO)
opcion = 0
while opcion != 4:
    print("\n1. Organizar por mes.\n2. Valores Maximos por dia. \n3. Mejor Mes. \n4. Salir del programa.")
    opcion = int(input("\nIngrese alguna de las siguientes opciones: "))
    if opcion == 1:
        organizar_por_mes(diccionario_eth)
    elif opcion == 2:
        valores_maximos_por_dia(diccionario_eth)
    elif opcion ==3:
        año = input("Si desea puede ingresar un año, si no solo acepte:")
        if año == '':
            mejor_mes(diccionario_eth, year=None)
        else:
            año = int(año)
            mejor_mes(diccionario_eth, year=año)
    else:
        print("Saliendo del programa")

## Tarea realizada entre Francisco Jeraldo y Fernando Mardones