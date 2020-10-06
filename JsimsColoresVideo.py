# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:25:59 2020
COLORES Y CONTORNOS OPENCV
Programa para recuperar las formas, el area, el perímetro, el color medio y la distancia entre objetos
findContours OPENCV
@author: Jsims
"""

# Importar opencv,Numpy y math 
import cv2 
import numpy as np
import math

""" ------------------------------------- """
""" Devuelve todos los puntos de la forma """
""" ------------------------------------- """
def puntosForma(contour):

    # Coger muestra color por cada RATIO_MUESTRAS pixeles (mas valor, menos precision pero más rápido)
    RATIO_MUESTRAS = 12
    
    # Extraer el rectangulo recto de los puntos del contorno
    (x, y, w, h) = cv2.boundingRect(contour)
    
    puntos = []
    
    # Recorrer todos los puntos del rectangulo
    for x_r in range(x,x+w,RATIO_MUESTRAS):
        
        for y_r in range(y,y+h,RATIO_MUESTRAS):
            
            # Comprobar si el punto está dentro del poligono
            result = cv2.pointPolygonTest(contour, (x_r,y_r), False) 
            if result > -1:
                
                # Recuperar el punto
                punto = (x_r,y_r)
                puntos.append(punto)
     
    # Devolver todos los puntos de la forma
    return puntos

""" --------------------------------------------------------------------------- """
""" Devuelve todos los puntos de la forma. Es mas lento que el metodo anterior. """
""" --------------------------------------------------------------------------- """
def puntosFormaBis(contour):

    mascara = np.zeros(escalaGrises.shape, np.uint8)
    cv2.drawContours(mascara, [contour], 0,255, -1)
    pixelpoints = np.transpose (np.nonzero (mascara))
     
    # Devolver todos los puntos de la forma
    return pixelpoints
 
""" ---------------------------------------------- """               
""" Devuelve el color medio de una serie de puntos """
""" ---------------------------------------------- """  
def colorMedioPuntos(imagen,puntos):
    
    blue = 0
    green = 0
    red = 0
        
    # Recorrer todos los puntos
    for p in puntos:
        
        # Recuperar el color de cada pixel
        b = imagen[p[1], p[0],0]
        g = imagen[p[1], p[0],1]
        r = imagen[p[1], p[0],2]
        
        # Sumar al total de colores
        blue += b
        green += g
        red += r

    # Numero de puntos del contorno
    num_puntos = len(puntos)
    
    # Recuperar la media de cada color
    blue = int(blue / num_puntos)
    green = int(green / num_puntos)
    red = int(red / num_puntos)
    
    # Devolver el color medio 
    return (blue,green,red)


""" --------------------------------------------------------------------------------------- """  
""" Dibuja el rectangulo recto (sin rotacion), por lo que puede no ser el rectangulo mínimo """
""" --------------------------------------------------------------------------------------- """  
def rectanguloRecto(contour, colorMedio):
    
    # Encontrar el rectangulo que encapsula el objeto
    (x_r, y_r, w, h) = cv2.boundingRect(contour)
    
     # Rectangulo del contorno
    cv2.rectangle(imagen, (x_r,y_r), (x_r+w, y_r+h), colorMedio, 2)


""" ------------------------------------------------------------------------------------------------------ """     
""" Dibuja el rectangulo girado (tiene en cuenta la rotación rotacion), que garantiza el rectangulo mínimo """
""" ------------------------------------------------------------------------------------------------------ """  
def rectanguloGirado(contour, colorMedio):
    
    # Recuperar el rectangulo de area minimo
    rectanguloMin  =  cv2.minAreaRect(contour) 
    
    # Recuperar los vertices del rectangulo mínimo
    vertices  =  cv2.boxPoints(rectanguloMin) 
    
    # Convertir y dibujar el rectangulo
    verticesInt  =  np.int0(vertices) 
    cv2.drawContours(imagen,[verticesInt],0,colorMedio,1)

""" ------------------------------------------------------- """  
""" Dibuja el círculo mínimo que engloba a todo el contorno """
""" ------------------------------------------------------- """ 
def circuloMinimo(contour, colorMedio):
    
    # Recuperar el circulo mínimo, punto central y radio
    (x_c, y_c), radio = cv2.minEnclosingCircle(contour)

    # Dibujar el circulo de mínimo área
    cv2.circle (imagen, (int (x_c), int (y_c)), int(radio), colorMedio, 2)

""" ---------------------------------------------- """ 
""" Recupera y muestra la informacion del contorno """
""" ---------------------------------------------- """ 
def printInfoContour(contour,num,area_contour):
    
    global puntosMedios
    
    # Constantes para colocar los mensajes
    X_OFFSET = -164
    X_MIN = 130
    Y_MAX = 125
    Y_MIN = 70

    # Recuperar el punto central de cada contorno utlizando el método moments
    M = cv2.moments(contour)
        
    # Evitar division por 0
    if(M["m00"] == 0):
        M["m00"] = 1
            
    # Coordenadas X e Y del centro de superficie
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    # Punto Medio
    puntoMedio = (x,y) 
    puntosMedios.append(puntoMedio)

    # Recuperar los puntos dentro del contorno
    puntos = puntosForma(contour)
    #puntos = puntosFormaBis(contour)

    # color medio de los puntos
    colorMedio = colorMedioPuntos(imagen, puntos)
    
    # Mostrar contorno o no
    if FLAG_MOSTRAR_CONTORNO:
    
        # Dibujar un RECTANGULO para el numero del contorno
        cv2.rectangle(imagen,(x+X_OFFSET,y-Y_MAX-35),(x+X_OFFSET+X_MIN,y-Y_MAX-20),colorMedio,-1)
        
        # Imprimir el número del contorno
        cv2.putText(imagen, "CONTOUR #" + str(num), (x+X_OFFSET+23,y-Y_MAX-24), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1,cv2.LINE_AA)
        
        # Dibujar un RECTANGULO para el area, el punto central y el perimetro
        cv2.rectangle(imagen,(x+X_OFFSET,y-Y_MAX),(x+X_OFFSET+X_MIN,y-Y_MIN),colorMedio,-1)
       
        # Mostrar el color medio
        cv2.putText(imagen, 'BGR ' + str(colorMedio),(x+X_OFFSET,y-Y_MAX-6), cv2.FONT_HERSHEY_SIMPLEX, 0.39, colorMedio,1,cv2.LINE_AA)
        
        # Mostrar el area
        cv2.putText(imagen, "Area: " + str(area_contour),(x+X_OFFSET+5,y-Y_MAX+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1,cv2.LINE_AA)
        
        # Mostrar el centro
        cv2.putText(imagen, "Center: " + str((x,y)),(x+X_OFFSET+5,y-Y_MAX+30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1,cv2.LINE_AA)
    
        # Mostrar el perimetro
        cv2.putText(imagen, "Perimeter: " + str(round(cv2.arcLength(contour,True),2)),(x+X_OFFSET+5,y-Y_MAX+45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255),1,cv2.LINE_AA)
        
        # Linea entre el centro y el rectangulo
        cv2.line(imagen, (x, y-2), (x+int(X_OFFSET/2), y-Y_MIN),colorMedio,2)
    
        # Punto medio (centro de superficie)
        cv2.putText(imagen, "X",puntoMedio, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2,cv2.LINE_AA)

    # Si hay que mostrar los rectangulos    
    if FLAG_MOSTRAR_RECT:
        # Dibujar el rectangulo recto
        rectanguloRecto(contour, colorMedio)
    
        # Dibujar el rectangulo girado minimo
        rectanguloGirado(contour, colorMedio)
    
        # Dibujar el circulo mínimo
        circuloMinimo(contour, colorMedio)

""" ----------------------------------------------- """ 
""" Dibuja la linea entre dos puntos y su distancia """
""" ----------------------------------------------- """
def dibujarLineaDistancia(p1,p2):
    
    # distancia entre los 2 puntos
    distancia = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    # Puntos medios
    x = int((p1[0] + p2[0]) / 2)
    y = int((p1[1] + p2[1]) / 2)

    # Linea entre el centro y el rectangulo
    cv2.line(imagen, p1, p2,(60,60,60),1)

    # Indicar la distancia
    cv2.putText(imagen,str(round(distancia,2)),(x,y), cv2.FONT_HERSHEY_TRIPLEX,0.5,(0,0,0),1)

""" -------------------------------- """ 
""" Dibujar lineas entre los objetos """
""" -------------------------------- """ 
def dibujarLineasObjetos(puntosMedios):
    
    # Si no hay puntos o sólo hay uno, bo hay lineas que mostrar
    if len(puntosMedios) < 2:
        return
    
    if len(puntosMedios) == 2:
      
        # Linea entre el centro y el rectangulo
        dibujarLineaDistancia(puntosMedios[0], puntosMedios[1])
        return

    # Recuperar el objeto inicial
    punI = puntosMedios[0]
        
    # Recorrer los objetos
    for pun in puntosMedios[1:]:
        
        # Dibujar la linea recta entre los 2 puntos
        dibujarLineaDistancia(punI, pun)
        
    # LLamada recursiva
    dibujarLineasObjetos(puntosMedios[1:])

""" ----------------------------------- """ 
""" Mostrar rectangulos y lineas ON/OFF """
""" ----------------------------------- """
def mostrarBotones():
            
    global MOSTRAR_LINEAS,MOSTRAR_RECT,MOSTRAR_CONTORNO
    
    cv2.rectangle(imagen,(40,780),(509,937),(0,0,0),-1)
    cv2.putText(imagen,"Jsims INFO CONTOUR (ESC for Exit)",(75,806), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
    
    # Mostrar informacion del contorno
    if FLAG_MOSTRAR_CONTORNO:
        cv2.rectangle(imagen,(45,820),(504,850),(0,200,0),-1)
        cv2.putText(imagen,"SHOW INFO CONTOUR - ON (mouse wheel)",(50,842), cv2.FONT_HERSHEY_PLAIN,1.3,(255,255,255),2)
    else: 
        cv2.rectangle(imagen,(45,820),(504,850),(0,0,255),-1)
        cv2.putText(imagen,"SHOW INFO CONTOUR - OFF (mouse wheel)",(47,842), cv2.FONT_HERSHEY_PLAIN,1.3,(255,255,255),2)
    
    # Mostrar rectangulos y circulos de contorno
    if FLAG_MOSTRAR_RECT:
        cv2.rectangle(imagen,(45,860),(504,890),(0,200,0),-1)
        cv2.putText(imagen,"SHOW RECTANGLES -  ON (mouse left)",(50,882), cv2.FONT_HERSHEY_PLAIN,1.4,(255,255,255),2)
    else: 
        cv2.rectangle(imagen,(45,860),(504,890),(0,0,255),-1)
        cv2.putText(imagen,"SHOW RECTANGLES - OFF (mouse left)",(50,882), cv2.FONT_HERSHEY_PLAIN,1.4,(255,255,255),2)
    
    # Mostrar Distancias
    if FLAG_MOSTRAR_LINEAS:
        cv2.rectangle(imagen,(45,900),(504,930),(0,200,0),-1)
        cv2.putText(imagen,"SHOW DISTANCES  -  ON (mouse right)",(50,922), cv2.FONT_HERSHEY_PLAIN,1.4,(255,255,255),2)
    else:
        cv2.rectangle(imagen,(45,900),(504,930),(0,0,255),-1)
        cv2.putText(imagen,"SHOW DISTANCES  - OFF (mouse right)",(50,922), cv2.FONT_HERSHEY_PLAIN,1.4,(255,255,255),2)
  
""" ------------------------------- """ 
""" Mostrar el numero de contornos  """
""" ------------------------------- """
def mostrarNumeroContornos(numContours):
            
    # Rectangulo y texto para el numero de contornos
    cv2.putText(imagen,"# Contours " + str(numContours),(45,70), cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,0),3)

      
""" ------------------------------------------------------------ """
""" Listener del ratón - Activa y desactiva rectangulos y lineas """
""" ------------------------------------------------------------ """
def clickEvent(event, x, y, flags, param):
            
    global FLAG_MOSTRAR_LINEAS,FLAG_MOSTRAR_RECT,FLAG_MOSTRAR_CONTORNO
    
    # Click Izquierdo
    if event == cv2.EVENT_LBUTTONDOWN:
        FLAG_MOSTRAR_RECT = not(FLAG_MOSTRAR_RECT)
        strXY = str(x) + ', ' + str(y)
        
    # Click Derecho
    elif event == cv2.EVENT_RBUTTONDOWN:
        FLAG_MOSTRAR_LINEAS = not(FLAG_MOSTRAR_LINEAS)

    # Click Botón Central
    elif event == cv2.EVENT_MBUTTONDOWN:
        FLAG_MOSTRAR_CONTORNO = not(FLAG_MOSTRAR_CONTORNO)
 

""" ------------------- """
""" INICIO DEL PROGRAMA """
""" ------------------- """

""" VARIABLES GLOBALES Y CONSTANTES """

# Area mínimo y maximo, los contornos de otros tamaños se descartan
AREA_MIN = 4000
AREA_MAX = 40000

# Flag para dibujar los contornos o no, se controlan con el raton
FLAG_DIBUJAR_CONTORNOS = False
FLAG_MOSTRAR_CONTORNO = False
FLAG_MOSTRAR_LINEAS = False
FLAG_MOSTRAR_RECT = False

# Grabar video o no
GRABAR = True

"""  INICIO BUCLE LECTURA  """

# Puntos Medios de los contornos
puntosMedios = []

""" CHANGE FOR YOUR VIDEO OR WEBCAM """
# Leer un video o directamente desde la WEBCAM 
cap = cv2.VideoCapture('snap2.mov')

# Ancho y alto del video
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# WRITE VIDEO
# si hay que grabar video con el resultado
if GRABAR:
    codigo = cv2.VideoWriter_fourcc(*'DVIX')
    grabador = cv2.VideoWriter('videoColor.mp4',codigo, 20,(ancho,alto))

# Mientras la camara esta abierta, capturar el frame
while cap.isOpened():
    
    # Capturar el nuevo frame desde el video
    ret, imagen = cap.read()
    if ret == False:
        break
    
    # Contador de contornos y puntos medios, reiniciar en cada captura de frame
    cnts = 0
    puntosMedios = []
    
    # Transformar la imagen a escala de grises
    escalaGrises = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        
    # Umbralizar la imagen con fondo negro
    _,umbral = cv2.threshold(escalaGrises, 190, 255, cv2.THRESH_BINARY_INV) 
        
    # Encontrar los contornos externos
    contornos,_ = cv2.findContours(umbral, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
    # Dibujar los contornos en la imagen original
    if FLAG_DIBUJAR_CONTORNOS:
        cv2.drawContours(imagen, contornos, -1, (0,255,0),2)
        
    # Recorrer los contornos
    for c in contornos:
            
        # Si el area es muy pequeña o grande, no tenerlo en cuenta, se deshecha
        area_contorno = int(cv2.contourArea(c))
        if AREA_MAX < area_contorno or area_contorno < AREA_MIN: 
            continue
    
        # Contador de contornos
        cnts = cnts + 1

        # Imprimir la informacion del contorno
        printInfoContour(c, cnts, area_contorno)
    
    # Dibujar lineas y distancias entre objetos
    if FLAG_MOSTRAR_LINEAS:
        dibujarLineasObjetos(puntosMedios)
    
    # Mostrar botones de control de que mostrar (flags)
    mostrarBotones()

    # Mostrar el numero de contornos
    mostrarNumeroContornos(cnts)

    # Umbral o threshold
    #cv2.imshow('Umbral', umbral) 

    # Imagen original   
    cv2.imshow('image',imagen) 
    
    # Si se está grabando video
    if GRABAR:
        grabador.write(imagen)
    
    # Listener del raton
    cv2.setMouseCallback('image', clickEvent)
    
    # Tecla de escape para salir (ESCAPE)
    if not(ret) or cv2.waitKey(40) == 27:
        break

# Liberar la camara
cap.release()

# Grabador
if GRABAR:
    grabador.release()

# Esperar a pulsar ESCAPE para salir
cv2.waitKey(0)
cv2.destroyAllWindows()