import math
import numpy as np
import time 
from multiprocessing import Process
import multiprocessing
import os
import ctypes
import matplotlib.pyplot as plt

taillemap=16
nbRobots=4
ko=25
k1=40
b = 0.1
vx=0
vy=0
dt = 0.1
m_i=1.0


class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def deplacement(robots, carte,barrier, lock,nb,im,plt): 
    global vx
    global vy
    global taillemap
    global nbRobots
    global ko
    global k1
    global b
    global dt
    global m_i

    #chaque robot change 100 fois de position
    for i in range(10):
        
        
        ra=robots.x
        rb=robots.y
        F_friction_x = -b * vx
        F_friction_y = -b * vy
        F_obs_x =0
        F_obs_y=0
        #on attend que tous les robots soit à cette étape pour avoir une meilleure cohérence
        barrier.wait()
        #lock pour éviter superposition
        with lock:
            for xm in range(taillemap):
                for ym in range(taillemap):
                    distance=math.sqrt(math.pow((ym-rb),2)+math.pow((xm-ra),2))
                    #si dans rayon du robot il y a un obstacle ou robot
                    if  (xm-ra)**2+(ym-rb)**2<=25:
                            #si obstacle calcul des forces
                            if carte[xm][ym]==1 :
                                if ra-xm!=0:
                                    
                                    F_obs_x += ko*(((ra-xm)/distance**(3/2)))
                                    F_friction_x = -b * vx
                                    
                                if rb-ym!=0:
                                    
                                    F_obs_y += ko*(((rb-ym)/distance**(3/2)))
                                    F_friction_y = -b * vy
                            #si robots calcul des forces
                            if carte[xm][ym]==0:
                                if ra-xm!=0:
                                    F_obs_x += k1*(((ra-xm)/distance**(3/2)))
                                    F_friction_x = -b * vx
                                if rb-ym!=0:
                                    F_obs_y += k1*((rb-ym)/distance**(3/2))
                                    F_friction_y = -b * vy

                   
                    #si meilleure approximation on arrête le robot
                    if F_obs_y==0 and F_obs_x==0:
                        vx=0
                        vy=0
                        F_friction_x=0
                        F_friction_y=0
                    
                    #juste pour l'affichage
                    if nb==nbRobots:
                        if carte[xm][ym]==5:
                            print(" ",end='')
                        else:
                            print(carte[xm][ym],end='')
                if nb==nbRobots:
                    print("")
           
        # Calcul de la somme des forces
        F_total_x =F_friction_x+F_obs_x
        F_total_y = F_friction_y+F_obs_y

        # Calcul de l'accélération
        ax = F_total_x / m_i
        ay = F_total_y / m_i
       
        # Mise à jour de la vitesse
        vx += ax * dt
        vy += ay * dt
           
        # Mise à jour de la position
        with lock:
            if carte[robots.x+int(np.sign(vx))][robots.y+int(np.sign(vy))]!=0 and carte[robots.x+int(np.sign(vx))][robots.y+int(np.sign(vy))]!=1:
                carte[robots.x][robots.y]=5
                robots.x = robots.x+int(np.sign(vx*dt))
                robots.y = robots.y+int(np.sign(vy*dt))  
                carte[robots.x][robots.y] = 0
                im.set_data(carte)
                
            else:
                carte[ra+int(np.sign(vx))][rb+int(np.sign(vy))]=0
                print("ici")
        
        barrier.wait()
        print("robot num ",nb," x ",robots.x," y ", robots.y)
        barrier.wait()
        """for a in range(taillemap):
            for b in range(taillemap):
                if nb==nbRobots:
                    if carte[a][b]==5:
                        print(" ",end='')
                    else:
                        print(carte[a][b],end='')
            if nb==nbRobots:
                print("")"""
        #print(carte)
        
        time.sleep(1)
    

if __name__ == '__main__':
    
    # Créer une Array partagée de taille `taillemap * taillemap` contenant des entiers signés de 32 bits
    carte = multiprocessing.Array(ctypes.c_int, taillemap*taillemap)
    # Convertir l'Array partagée en un tableau Numpy
    carte = np.ctypeslib.as_array(carte.get_obj())
    # Redimensionner le tableau Numpy en une matrice de taille `taillemap x taillemap`
    carte = carte.reshape(taillemap, taillemap)
    carte[:,:] = [[5 for j in range(taillemap)] for i in range(taillemap)]
    
    
    #initialisation obsatcles murs et robots
    
    carte[5][1]=1
    carte[5][2]=1
    carte[1][8]=1
    carte[2][8]=1 
    carte[3][8]=1 
    carte[4][8]=1
    carte[8][1]=1 
    carte[8][2]=1
    carte[8][3]=1 
    carte[8][4]=1   
    
    """robot1=Robot(4, 4)
    robot2 = Robot(8, 9)
    robot3 = Robot(9, 8)
    robot4 = Robot(8, 8)
    robot5 = Robot(8, 10)
    robot6 = Robot(9, 10)
    robot7 = Robot(10, 8)
    robot8 = Robot(10, 10)
    robot9 = Robot(10,9)"""
    robot1=Robot(2, 4)
    robot2 = Robot(2, 5)
    robot3 = Robot(3, 4)
    robot4 = Robot(3, 5)
    robots = [robot1, robot2,robot3,robot4]
    
    for xm in range(taillemap):
        for ym in range(taillemap):
            if xm==0 or xm==taillemap-1 or ym==0 or ym==taillemap-1:
                carte[xm][ym]=1

    # Créer une liste de couleurs : 0 = vert, 1 = noir, 5 = blanc
    couleurs = ['green', 'black', 'white']

    # Créer une carte de couleurs personnalisée
    cmap = plt.cm.colors.ListedColormap(couleurs)
    bounds = [0, 0.5, 1.5, 5.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    # Créer une figure et un axe
    fig, ax = plt.subplots()
    # Afficher le tableau avec des couleurs
    im = ax.imshow(carte, cmap=cmap, norm=norm)
    
    # Masquer les graduations sur les axes x et y
    ax.set_xticks([])
    ax.set_yticks([])

    # Afficher la figure initiale
    plt.show(block=False)
    
    
    processes = []
    barrier = multiprocessing.Barrier(nbRobots)
    processes = []
    lock = multiprocessing.Lock()
 
 
    for i in range(nbRobots):
        carte[robots[i].x][robots[i].y] = 0
        im.set_data(carte)
        plt.pause(1)
        #pour chaque robot on lance un process
        p = multiprocessing.Process(target=deplacement, args=(robots[i], carte, barrier,lock,i+1,im,plt))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
    plt.show()
    



