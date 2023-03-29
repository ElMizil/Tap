from imutils.perspective import four_point_transform as FPT
from collections import Counter
import matplotlib.pyplot as plt
from imutils import contours
from skimage import io
import numpy as np
import imutils
import cv2
import re
import pyttsx3
import operator

xo = 1000
yo = 1000
xe = 0
ye = 0
global numero
numero = False

def findOrigin(x,y):
    global xo
    global yo
    if(x<=xo):
        xo = x
    if(y<=yo):
        yo = y

def findEnd(x,y):
    global xe
    global ye
    if(x>=xe):
        xe = x
    if(y>=ye):
        ye = y

def encontrarLineas():
    global ye,yo
    num = round((ye-yo)/42)
    if(num == 1):
        return 1
    else:
        return num/2

def encontrarRect(centro):
    global ye,yo
    yo = 1000
    ye = 0
    for i in centro:
        if(i[1]>=ye):
            ye = i[1]
        if(i[1]<=yo):
            yo = i[1]

def separarLineas(centros, puntos):
    #for i in range(0,len(puntos)):
        global p,yo,ye
        print(p,yo,ye)
        for j in centros:
            if(j[1]<yo+3*p+20):
                puntos[0].append(j)
            if(j[1]>yo+3*p+20 and j[1]<yo+12*p):
                puntos[1].append(j)
            if(j[1]>yo+12*p+10 and j[1]<ye+10):
                puntos[2].append(j)

def traducir(centro):
    #yo = 1000
    #ye = 0
    global letra
    global p
    global numero
    #for i in centro:
     #   if(i[1]>=ye):
      #      ye = i[1]
       # if(i[1]<=yo):
        #    yo = i[1]
    #letra = ""
    #print("Traducciendo")
    #print(ye,yo)
    palabra = ""
    #print(len(centro))
    cv2.rectangle(img,[centro[0][0]-round(p/2),yo-round(p/2)],[centro[0][0]+round(5*p/2),ye+round(p/2)],(0,0,255),2)
    #cv2.rectangle(img,[xo,yo],[xe,ye],(255,100,0),2)
    cv2.line(img,(centro[0][0]+p,yo-round(p/2)),[centro[0][0]+p,ye+round(p/2)],(0,0,255),2)
    cv2.line(img,(centro[0][0]-round(p/2),yo+p),[centro[0][0]+round(5*p/2),yo+p],(0,0,255),2)
    cv2.line(img,(centro[0][0]-round(p/2),yo+round(5*p/2)),[centro[0][0]+round(5*p/2),yo+round(5*p/2)],(0,0,255),2)
    for i in centro:
        if(i[0]<centro[0][0]+p and i[1]>=yo-p/2 and i[1]<yo+p):
            letra = letra +"1"
        if(i[0]>centro[0][0]+p and i[1]>=yo-p/2 and i[1]<yo+p):
            letra = letra+"2"
        if(i[0]<centro[0][0]+p and i[1]>=yo+p and i[1]<yo+5*p/2):
            letra = letra+"3"
        if(i[0]>centro[0][0]+p and i[1]>=yo+p and i[1]<yo+5*p/2):
            letra = letra+"4"
        if(i[0]<centro[0][0]+p and i[1]>=yo+5*p/2 and i[1]<ye+p/2):
            letra = letra+"5"
        if(i[0]>centro[0][0]+p and i[1]>=yo+5*p/2 and i[1]<ye+p/2):
            letra = letra+"6"
    if numero:
        letra = letra + "0"
    if letra == "2456":
        letra = ""
        numero = True
    return palabra.join(sorted(letra))
    

    
code_table = {
    'a': '1',
    'b': '13',
    'c': '12',
    'd': '124',
    'e': '14',
    'f': '123',
    'g': '1234',
    'h': '134',
    'i': '23',
    'j': '234',
    'k': '15',
    'l': '135',
    'm': '125',
    'n': '1245',
    'o': '145',
    'p': '1235',
    'q': '12345',
    'r': '1345',
    's': '235',
    't': '2345',
    'u': '156',
    'v': '1356',
    'w': '2346',
    'x': '1256',
    'y': '12456',
    'z': '1456',
    '?': '356',
    '#': '2456',
    '1': '10',
    '2': '130',
    '3': '120',
    '4': '1240',
    '5': '140',
    '6': '1230',
    '7': '12340',
    '8': '1340',
    '9': '230',
    '0': '2340',
    ' ': '000000'}

img = cv2.imread('images/braile5.jpeg', cv2.IMREAD_COLOR)
img = cv2.imread('images/braile2.png', cv2.IMREAD_COLOR)
#img = cv2.imread('images/braile4.jpeg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/Braile4.png', cv2.IMREAD_COLOR)
#img = cv2.imread('images/braile2.jpeg', cv2.IMREAD_COLOR)
img = cv2.imread('images/braile3.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/braile.jpg',cv2.IMREAD_COLOR)
vid = cv2.VideoCapture(0)
# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

_, threshold = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
  
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
i = 0
centers = []
# list for storing names of shapes
for contour in contours:
  
    # here we are ignoring first counter because 
    # findcontour function detects whole image as shape
    if i == 0:
        i = 1
        continue
  
    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
      
    # using drawContours() function
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 1)
    #print(round(cv2.arcLength(contour,True)))
    p = round(cv2.arcLength(contour, True)/np.pi)
  
    # finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
        findOrigin(x,y)
        findEnd(x,y)
        centers.append((x,y))
        #print(x,y)
centers.sort()
lineas = encontrarLineas()
puntos = []
for i in range(0,int(lineas)):
    puntos.append([])
#print(len(puntos))
separarLineas(centers,puntos)
#print(puntos[1])
#print(len(puntos[1]))
#print(lineas)
#print(puntos)
#print(xo,yo)
#print(xe,ye)
#xo = xo-9
#yo = yo-9
#xe = xe+9
#ye = ye+9


engine = pyttsx3.init() 
voices = engine.getProperty('voices')  
#for voice in voices:
    #print(voice, voice.id)              
engine.setProperty('rate', 150)
engine.setProperty('voice',"english")
#engine.setProperty('voice',"spanish-latin-am")

letra = ""
palabra=""
centros_letra = []
add_space = False
for h in puntos:
    encontrarRect(h)
    centers = h
    for i in range(0,len(centers)):
        if(not centros_letra):
            letra = ""
            centros_letra.append(centers[i])
        if i == len(centers)-1:
            #print(centros_letra)
            letra = traducir(centros_letra)
            #print(letra)
            try:
                palabra = palabra + list(code_table.keys())[list(code_table.values()).index(letra)]
                palabra = palabra + " "
            except:
                print("Digito no encontrado")
            centros_letra = []
            break
        #print(centers[i+1][0]-centers[i][0])
        if(centers[i+1][0]-centers[i][0] <= 25):
            #print(centers[i+1][0])
            centros_letra.append(centers[i+1])
        else:
            if(add_space):
                palabra = palabra + " "
                add_space = False
            #print(centros_letra)
            letra = traducir(centros_letra)
            #print(letra)
            try:    
                palabra = palabra + list(code_table.keys())[list(code_table.values()).index(letra)]
            except:
                print("Digito no encontrado")
            centros_letra = []
        if(centers[i+1][0]-centers[i][0] >= 70):
            add_space = True
            numero = False
    
print("Traduccion:")
print(palabra)
engine.say(palabra)
engine.runAndWait()

        
# displaying the image after drawing contours

cv2.imshow('shapes', img)
  
cv2.waitKey(0)
cv2.destroyAllWindows()