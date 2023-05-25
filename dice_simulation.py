"""
    JUEGO DE DADOS

    Se lanzan simultáneamente un par de dados y se suman los puntos de las caras superiores.
    
    ###### Reglas para el tirador: ######
    1. Gana si sale un 7 u 11
    2. Pierde si sale 2, 3 ó 12
    3. Si sale 4, 5, 6, 8, 9 ó 10, sigue tirando, con las siguientes reglas:
        3.1 Gana si repite el número que salió anteriormente (4, 5, 6, 8, 9 o 10)
        3.2 Pierde si sale el 7
        3.3 Mientras no ocurra lo anterior sigue tirando hasta que suceda cualquiera de los
            resultados anteriores en los que gana o pierde
    
    Calcular la probabilidad de ganar o perder, simulando 1.500 jugadas

"""

import random
import sys
from typing import Any

def obtener_comb_unicas_y_frec_sumas(numero_dados: int, numero_caras: int) -> tuple:

    """

        Devuelve una tupla con una lista de las combinaciones únicas de los dados y un diccionario
        con las frecuencias de las sumas de los dados.

        `numero_dados`: Número de dados a utilizar.
        `numero_caras`: Número de caras de cada dado.

    """

    # Se buscará saber cuántas combinaciones únicas se pueden obtener con los dados
    ocurrencias_suma = dict()

    suma_mas_baja = numero_dados
    suma_mas_alta = numero_dados * numero_caras

    for suma in range(suma_mas_baja, suma_mas_alta + 1):
        ocurrencias_suma[suma] = 0

    # La combinación inicial es la que tiene todos los números más bajos de cada dado
    combinacion = list(1 for _ in range(numero_dados))

    combinaciones_unicas = list()
    dado_en_curso = numero_dados

    # Se mezclan los dados desde el último hasta el límite
    while dado_en_curso > 0:

        # Se verifica si la combinación ya se había obtenido
        combinacion_ordernada = sorted(combinacion)

        if combinacion_ordernada not in combinaciones_unicas:

            # Se guarda la combinación
            combinaciones_unicas.append(combinacion_ordernada)
            # Se actualiza el número de ocurrencias de la suma
            ocurrencias_suma[sum(combinacion_ordernada)] += 1

        combinacion[dado_en_curso - 1] += 1

        # Se verifica si se ha llegado al límite de caras del dado en curso
        if combinacion[dado_en_curso - 1] > numero_caras:
            combinacion[dado_en_curso - 1] = 1 # Se reinicia el dado en curso
            dado_en_curso -= 1 # Se cambia al siguiente dado a la izquierda

        # De lo contrario, se cambia al último dado
        elif dado_en_curso < numero_dados:
            dado_en_curso = numero_dados

    return (combinaciones_unicas, ocurrencias_suma)

def obtener_prob_sumas(numero_dados: int, numero_caras: int, verbose: bool) -> list[tuple]:

    """

        Devuelve una lista de tuplas con la suma de los dados y la probabilidad de obtenerla (del 0 al 1).

        `numero_dados`: Número de dados a utilizar.
        `numero_caras`: Número de caras de cada dado.

    """

    combinaciones_unicas, ocurrencias_suma = obtener_comb_unicas_y_frec_sumas(numero_dados, numero_caras)

    if verbose:
        ver_comb_unicas_y_frec_sumas(combinaciones_unicas, ocurrencias_suma)

    probabilidades_suma = list()

    for suma in ocurrencias_suma:
        prob_continua = ocurrencias_suma[suma] / len(combinaciones_unicas) 
        probabilidades_suma.append( (suma, prob_continua) )

    return probabilidades_suma

def ver_comb_unicas_y_frec_sumas(combinaciones_unicas: list, ocurrencias_suma: dict):

    print("\nCombinaciones únicas:")
    msg_combinaciones = "\t"
    for combinacion in combinaciones_unicas:
        msg_combinaciones += f"{combinacion}, "
    print(msg_combinaciones)

    print("\nNo. de combinaciones únicas que suman cada número:")
    for suma in ocurrencias_suma:
        print(f"\t{suma}: {ocurrencias_suma[suma]} combinaciones")

def obtener_prob_acumuladas_sumas(numero_dados: int, numero_caras: int, verbose: bool) -> list[tuple]:

    """

        Devuelve un diccionario con las probabilidades acumuladas de obtener cada suma de los dados.

        `numero_dados`: Número de dados a utilizar.
        `numero_caras`: Número de caras de cada dado.

    """

    probabilidades_suma = obtener_prob_sumas(numero_dados, numero_caras, verbose)

    probabilidades_acumuladas = list(Any for _ in range(len(probabilidades_suma)))

    for i in range(len(probabilidades_suma)):

        # Se obtiene la acumulación de las probabilida de esta suma y las anteriores
        prob_acumulada = probabilidades_suma[i][1]

        if i > 0:
            prob_acumulada += probabilidades_acumuladas[i - 1][1]

        suma = probabilidades_suma[i][0]
        probabilidades_acumuladas[i] = (suma, prob_acumulada)

    return probabilidades_acumuladas

def formatear_probabilidades(prob_acumuladas: list, verbose: bool) -> dict:

    """

        Devuelve un diccionario que tiene por llaves una tupla con los límites inferior y superior
        de la probabilidad y por valor la suma de los dados que se encuentra en ese rango.

        `prob_acumuladas`: Diccionario con las probabilidades acumuladas de obtener cada suma de los dados.

    """

    lim_inferior = 0

    probabilidades_formateadas = dict()

    if verbose:
        print("\nProbabilidades acumuladas:")

    for i in range(len(prob_acumuladas)):

        lim_superior = prob_acumuladas[i][1]

        suma = prob_acumuladas[i][0]
        probabilidades_formateadas[(lim_inferior, lim_superior)] = suma

        msg_prob = f"\t{suma}: ({lim_inferior:.4f}"
        lim_inferior = lim_superior

        if verbose:
            print(msg_prob, f"- {lim_superior:.4f})")

    return probabilidades_formateadas

def tirar_dados(prob_formateadas: dict) -> int:

    """
        Simula el lanzamiento de dos dados, a través de la generación de un número aleatorio
        que se busca en un diccionario de probabilidades acumuladas, para determinar la suma
        de los dados.
    """
    
    # Se genera un número aleatorio entre 0 y 1
    num_aleatorio = random.random()

    # Se busca en el diccionario de probabilidades acumuladas
    for prob in prob_formateadas:

        if num_aleatorio >= prob[0] and num_aleatorio < prob[1]:
            return prob_formateadas[prob] # Se devuelve la suma de los dados

def jugar(prob_formateadas: dict):

    """
        Simula una jugada del juego de dados.
    """

    suma = tirar_dados(prob_formateadas)
    
    if suma in [7, 11]:
        return True
    elif suma in [2, 3, 12]:
        return False
    
    # Si no se ha ganado ni perdido, se sigue tirando
    primera_suma = suma

    while True:

        nueva_suma = tirar_dados(prob_formateadas)
        
        if nueva_suma == 7:
            return False
        elif nueva_suma == primera_suma:
            return True

def ver_prob_formateadas(prob_formateadas: dict):

    """
        Muestra las probabilidades formateadas.
    """

    print("\nSe muestran las probabilidades formateadas:")
    print("Suma : (Límite inferior - Límite superior)")

    for prob in prob_formateadas:
        print(f"\t{prob_formateadas[prob]} : ({prob[0]:.3f} - {prob[1]:.3f})")

def main():

    """
        Función principal del programa.
    """

    try:
        numero_jugadas = sys.argv[1]
    except IndexError:
        print("Debe ingresar el número de jugadas a simular.")
        return 1

    if not numero_jugadas.isdigit():
        print("El número de jugadas debe ser un número.")
        return 1

    numero_jugadas = int(numero_jugadas)

    if numero_jugadas < 0 or numero_jugadas % 1 != 0:
        print("El número de jugadas debe ser positivo y entero.")
        return 1

    verbose = False

    try:
        verbose = sys.argv[2]

        if verbose in ["-v", "--verbose"]:
            verbose = True
        else:
            print("El segundo argumento debe ser -v o --verbose, si se desea mostrar información adicional.")

    except IndexError:
        pass

    # Se obtienen las probabilidades acumuladas de obtener cada suma de los dados
    prob_acumuladas = obtener_prob_acumuladas_sumas(2, 6, verbose=verbose)

    # Se formatean las probabilidades acumuladas
    prob_formateadas = formatear_probabilidades(prob_acumuladas, verbose=verbose)

    ganadas = 0
    perdidas = 0

    # Se simulan las jugadas
    for _ in range(numero_jugadas):

        gano = jugar(prob_formateadas)

        if gano:
            ganadas += 1
        else:
            perdidas += 1

    probabilidad_ganar = ganadas / numero_jugadas
    probabilidad_perder = perdidas / numero_jugadas

    if verbose:
        print()
    print('Jugadas totales:', numero_jugadas)
    print(f"Probabilidad de ganar: {probabilidad_ganar*100:.2f} %")
    print(f"Probabilidad de perder: {probabilidad_perder*100:.2f} %")

    return 0

main()