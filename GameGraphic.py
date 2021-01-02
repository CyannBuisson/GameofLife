#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 17:40:22 2020

@author: cyann
"""

import tkinter as tk
import numpy as np
import math
import time

#__________création de la fenêtre de jeu__________

fn = tk.Tk()
fn.title("John Conway's Game of Life")

# __________creation de la grille de jeu__________

w=1000 #width
h=700 #height
p=20 # pas de la grille
grille=tk.Canvas(fn,bg="white",width=w,height=h)
grille.grid(row=1, column=0, columnspan=3)

for i in range (0, w, p):
    grille.create_line((i,0),(i,w)) #colonnes
    grille.create_line((0,i),(w,i)) #lignes

#__________initialisation : placer les cellules sur la grille__________

Xmax=math.floor(w/p) #nbr cubes dans longueur grille = taille matrice monde
Ymax=math.floor(h/p) #nbr cubes dans hauteur grille = taille matrice monde
Monde=np.zeros((Xmax,Ymax)) #tableau du Monde initial
Monde2=np.zeros((Xmax,Ymax)) #tableau calculé

def naissance(event):
    
    x, y = event.x, event.y #clic coordinates

    x2=(x//p)*p
    y2=(y//p)*p

    grille.create_rectangle(x2, y2, x2+p, y2+p, fill="black")#la case devient noire
    
    #INITIALISATION DU MONDE
    global Monde 
    Monde[y//p,x//p]=1 #abscisse x =colonnes et ordonnée y=lignes de Monde

grille.bind('<Button-1>', naissance) 



#__________le jeu démarre__________

def vois1(M,i,j):
    if M[i,j]==1: #la cellule est vivante
        nbrV=-1 #pour ne pas compter la cellule vivante elle-même
    if M[i,j]==0: #la cellule est non vivante
        nbrV=0
    for o in range (i-1,i+2):
        for p in range (j-1,j+2):
            if o>=Xmax or p>=Ymax or o<0 or p<0: #si l'index sort du tableau
                nbrV=nbrV #n'affecte pas le nombre de voisins
            else:
                if M[o,p]==1:
                    nbrV+=1
    return nbrV

def game():

    global Monde,Monde2
    global onoff
    onoff=1
    x=0 #booléen pour l'itération
    t=0 #nbr iteration
    
    while x==0:        
        if onoff==1:
            t+=1 
            #calcul du monde initial dans le monde suivant
            for i in range (Xmax):
                for j in range (Ymax):
                    if Monde[i,j]==1: #traitement d'une cellule vivante
                        if vois1(Monde,i,j)==2 or vois1(Monde,i,j)==3:
                            Monde2[i,j]=1 #la cellule reste vivante
                        else:
                            Monde2[i,j]=0 #la cellule meurt
                            grille.create_rectangle(j*p, i*p, j*p+p, i*p+p, fill="white")#la case devient blanche
                            
                    else: #traitement d'une cellule non vivante
                        if vois1(Monde,i,j)==3:
                            Monde2[i,j]=1 #la cellule nait
                            grille.create_rectangle(j*p, i*p, j*p+p, i*p+p, fill="black")#la case devient noire

            if  np.array_equiv(Monde, Monde2):
                x=1 #break le while
            else:
                #Copie du monde créé vers le monde initial:
                for i in range (Xmax) :
                    for j in range (Ymax) :
                            Monde[i,j]=Monde2[i,j]

            #affichage itération-temps:
            iteration.configure(text='Temps = {}'.format(t))
            #gérer la vitesse d'itération + affichage:
            time.sleep(speed)
            speedt.configure(text='Speed = {}'.format(speed))
            #affichage visible des carrés:
            fn.update()
        
#__________pause/arret du jeu__________

def pause():
    global onoff
    onoff=0
    
#__________variation vitesse du jeu__________

speed=1
def speedplus():
    global speed
    speed=speed+0.25
    
def speedless():
    global speed
    speed=speed-0.25

#__________éléments graphiques de jeu__________

#boutons du jeu
start=tk.Button(fn, text="Start",command=game) #lance les itérations du jeu 
pause=tk.Button(fn, text="Pause",command=pause) #pause dans l'itération du jeu
leave=tk.Button(fn,text="Quitter",command=fn.destroy) #quitte le jeu

start.grid(row=3,column=0)
pause.grid(row=3,column=1)
leave.grid(row=3,column=2)

#régler la vitesse d'itération
speed_canvas=tk.Canvas(fn, width=170, height=30)
speed_canvas.grid(row=2,column=1)

speedm=tk.Button(speed_canvas, text="-", command=speedless)
speedm.configure(bg="white")
sspeedm_window=speed_canvas.create_window(0,15, anchor=tk.W, window=speedm)

speedp=tk.Button(speed_canvas, text="+",command=speedplus)
speedp.configure( bg="white")
speedp_window=speed_canvas.create_window(130,15, anchor=tk.W, window=speedp)

speedt=tk.Label(speed_canvas,padx=4,pady=3,text="Speed = 0")
sspeedt_window=speed_canvas.create_window(40,15, anchor=tk.W, window=speedt)

# Itérations du jeu
iteration=tk.Label(fn, text="Time = 0") #donne le numéro d'itération
expl=tk.Label(fn, text="Click on the white cases to make them live, and observe their evolution!")

iteration.grid(row=2,column=0)
expl.grid(row=0,column=0,columnspan=3)


#__________ Lancement du jeu__________
fn.mainloop()
