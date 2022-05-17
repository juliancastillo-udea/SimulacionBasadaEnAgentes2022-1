# -*- coding: utf-8 -*-
"""
Created on Mon May 16 19:22:23 2022
Conway's Game of Life en Python 3.9 con PyGame
@author: JulianCastillo

    Created By
    -------
    Julian Andres Castillo
        DESCRIPTION. Ingeniero de Sistemas M.Sc. En Ingeniería, creado para el 
        curso de Simulación Basada en agentes de posgrados UdeA.
        Basado en el concepto de https://www.neuralnine.com/
"""

import time
import pygame
import numpy as np
#Colores del juego en RGB
color_fondo = (10, 10, 10) #Color del fondo BackGround
color_malla = (40, 40, 40) #Color de la malla
color_celda_muerta = (170, 170, 170) #Color de celda muerta
color_celda_viva = (255,255,255) #Color de celda viva

def MatrizProbabilidad(row,col,probabilidad):
    return np.random.choice([0, 1], size=(row,col), p=[probabilidad, 1-probabilidad])
def ReglasGameOfLife(screen, cells, size, estado_ejecucion=False): 
    '''
    Parameters
    ----------
    screen : PyGame Screen 
        DESCRIPTION. Tamaño de la pantalla, lo definimos en el momento de crear el juego
        se define de 800x600 (800-->pixeles horizontales, 600-->pixeles verticales)
    cells : Celdas
        DESCRIPTION. Celdas sobre las cuales se realizará el juego. También es el tamaño
        de la malla.
    size : Numérico, mxn
        DESCRIPTION. Tamaño de las celdas cuadradas del juego.
    estado_ejecucion : Booleano, optional
        DESCRIPTION. El valor por defecto es falso, cuando verdadero, actualiza
        la pantalla para ver los cambios realizados en el modelo.
    porcentaje_aleatorio_malla : Flotante, optional
        DESCRIPTION. El valor por defecto es 0.5 y detalla la probabilidad de
        una celda de tener un valor en cero o en uno, sirve para crear una
        malla aleatoria, si el valor es cero, se debe crear con el mouse
 
    Returns
    -------
    celdas_actualizadas
        DESCRIPTION. Retorna las celdas con el valor actualizado del juego

    '''
    celdas_actualizadas = np.zeros((cells.shape[0], cells.shape[1]))
      
    for row, col in np.ndindex(cells.shape): #https://numpy.org/doc/stable/reference/generated/numpy.ndindex.html
        cont_cvivas = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        #Row y Col mas dos, los limites del slicing son [inicio:final)
        #color = color_fondo if cells[row,col] == 0 else color_celda_viva
        cell_color = cells[row, col]
        
        if cell_color == 0:
            color = color_fondo
        else:
            color = color_celda_viva
        
        if cells[row, col] == 1: #Si la celda esta viva debemos preguntar las reglas
            if cont_cvivas < 2 or cont_cvivas > 3:
                celdas_actualizadas[row,col] = 0
                if estado_ejecucion:
                    color = color_celda_muerta
            elif 2 <= cont_cvivas <= 3:
                celdas_actualizadas[row,col] = 1
                if estado_ejecucion:
                    color = color_celda_viva
        else:
            if cont_cvivas == 3:
                celdas_actualizadas[row,col] = 1
                if estado_ejecucion:
                    color = color_celda_viva
        pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))
    return celdas_actualizadas

def EstadoJuego(tamanio_malla, tamanio_celda, velocidad):
    print('Estado inicial del juego:')
    print('\tTamaño de la ventana=', (tamanio_malla[1], tamanio_malla[0]), ' Valores en Pixeles')
    print('\tTamaño de la malla=', tamanio_celda)
    print('\tVelocidad de refrescado=', velocidad)
    
def main():
    pygame.init()
    tamanio_celdas = (50,50)
        #Debemos validar la probabilidad 
        #Valores a detallar
        #   0 --> Iniciamos con matriz en cero y debemos pintar el mapa
        #   1 --> Debemos cargar el documento GameOfLife.txt
        #   p --> Creamos una matriz con un valor de probabilida p de unos y ceros
    p = 0.5 #Cambiar el presente valor para detallar el procedimiento y mejorarlo o empeorarlo
    if p == 0:
        #Creamos una malla de celdas en cero de tamaño shape[0]xshape[1] (mxn)
        cells = np.zeros(tamanio_celdas)

    elif p == 1:
        cargatxt = np.loadtxt("pufferfishrake.txt", dtype=int)
        cells = cargatxt
    else: #La probabilidad es diferente de cero por lo tanto debemos detallar la malla con dicho valor p
        cells = MatrizProbabilidad(tamanio_celdas[0], tamanio_celdas[1], p)
        
    tamanio_celdas = (cells.shape[0], cells.shape[1])
    tamanio_malla = (cells.shape[0]*10,cells.shape[1]*10)
    pygame.display.set_caption("Conway's Game of Life, Malla de " + str(tamanio_celdas) + " | Presiona Barra espaciadora para iniciar o detener.")
    screen = pygame.display.set_mode((tamanio_malla[1], tamanio_malla[0])) #Las matrices son filas por columnas, las pantallas son columnas por filas, se debe invertir el valor
    #cells = np.zeros(tamanio_celdas)
    screen.fill(color_malla)
    ReglasGameOfLife(screen, cells, 10)
    pygame.display.flip()
    pygame.display.update()
    velocidad = 0.0001 #La velocidad detalla la velocidad de refrescado de la pantalla
    running = False
    EstadoJuego(tamanio_malla, tamanio_celdas, velocidad)
    while True:
        #Variables generales para la evolucion del jugo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    ReglasGameOfLife(screen, cells, 10)
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print('Velocidad anterior=', velocidad)
                    velocidad = velocidad / 10
                    print('Velocidad actual=', velocidad)
                    EstadoJuego(tamanio_malla, cells.size, velocidad)
                elif event.key == pygame.K_DOWN:
                    print('Velocidad anterior=', velocidad)
                    velocidad = velocidad * 10
                    print('Velocidad actual=', velocidad)
                    EstadoJuego(tamanio_malla, cells.size, velocidad)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                ReglasGameOfLife(screen,cells, 10)
                pygame.display.update()
                
        screen.fill(color_malla)
        if running:
            cells = ReglasGameOfLife(screen, cells, 10, estado_ejecucion=True)
            pygame.display.update()
        
        time.sleep(velocidad)

if __name__ == '__main__':
    main()                