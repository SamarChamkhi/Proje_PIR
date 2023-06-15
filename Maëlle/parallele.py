import math
import numpy as np
import time 
from multiprocessing import Process, Manager, Value
import multiprocessing
from multiprocessing import Array
from matplotlib import animation
import os
import ctypes
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, x, y,va,vb,aa,ab):
        self.x = Value('d', x)
        self.y = Value('d', y)
        self.va = Value('d', va)
        self.vb = Value('d', vb)
        self.aa = Value('d', aa)
        self.ab = Value('d', ab)
class Obstacle:
    def __init__(self, x, y):
        self.x = Value('d', x)
        self.y = Value('d', y)
        
def obstacle_on_line_of_sight(P1, P2x,P2y, obstacles):
    x1=P1.x.value
    y1 = P1.y.value
    x2, y2 = P2x, P2y
    if x1 == x2:  # Vérifier si la ligne est verticale
        for obstacle in obstacles:
            if obstacle.x == x1 and min(y1, y2) <= obstacle.y <= max(y1, y2):
                return True
        return False
    else:
        if y1 == y2:  # Vérifier si la ligne est horizontale
            for obstacle in obstacles:
                if obstacle.y.value == y1 and min(x1, x2) <= obstacle.x.value <= max(x1, x2):
                    return True
            return False
        else:
            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1
            intersection_x = -b / m
            if (intersection_x < min(x1, x2) or intersection_x > max(x1, x2)):
                return False
            else:
                for obstacle in obstacles:
                    intersection_y = m * (obstacle.x.value - x1) + y1
                    if obstacle.y.value == intersection_y and min(x1, x2) <= obstacle.x.value <= max(x1, x2):
                        return True
                return False
                
                
                
taillemap=20

ko=30.0
k1=60.0
b = 6
rayon=16.01
dt = 0.3
m_i=1.0


def deplacement(robot,barrier, lock,nb,covered_cells,obstacles,robots): 
   
    global taillemap
    global nbRobots
    global ko
    global k1
    global b
    global dt
    global m_i
    all_stopped = False
    i=0
    while not all_stopped: 
        all_stopped = True
        F_friction_x = 0.0
        F_friction_y = 0.0
        ra=robot.x.value
        rb=robot.y.value
        F_obs_x =0.0
        F_obs_y=0.0
        with lock:
            for o in obstacles:
                xo=o.x.value
                yo=o.y.value
                distance = math.sqrt(math.pow((yo - rb), 2) + math.pow((xo - ra), 2))

                if  distance<=rayon:
                    if rb-yo!=0 or ra-xo!=0 : 
                        F_obs_x += ko*(((ra-xo)/distance**3))   
                        F_obs_y += ko*(((rb-yo)/distance**3))
                   
            for rr in robots:
                xr=rr.x.value
                yr=rr.y.value
                distance = math.sqrt(math.pow((yr - rb), 2) + math.pow((xr - ra), 2))

                if  distance<=rayon:
                    if rb-yr!=0 or ra-xr!=0 : 
                        F_obs_x += k1*(((ra-xr)/(distance)**3))   
                        F_obs_y += k1*(((rb-yr)/(distance)**3))
                        
            if F_obs_y==0 and F_obs_x==0:
                robot.va.value=0
                robot.vb.value=0
                F_friction_x=0
                F_friction_y=0
                
            F_friction_x = -b * robot.va.value
            F_friction_y = -b * robot.vb.value
            F_total_x =F_friction_x+F_obs_x
            F_total_y = F_friction_y+F_obs_y
        
            if F_total_x==0 and F_total_y==0:
                robot.va.value=0
                robot.vb.value=0
            ax = F_total_x / m_i
            ay = F_total_y / m_i
            
            if abs(ax) > 20:
                ax = 20 if ax > 0 else -20
            if abs(ay) > 20:
                ay = 20 if ay > 0 else -20
            if abs(ax) < 10:
                ax = 0 if ax > 0 else -0
            if abs(ay) < 10:
                ay = 0 if ay > 0 else -0
            
            robot.aa.value=ax
            robot.ab.value=ay
            robot.va.value =robot.va.value+robot.aa.value*dt
            robot.vb.value = robot.vb.value+robot.ab.value*dt
            
            if abs(robot.va.value) < 3.3 and abs(robot.vb.value) < 3.3:
                robot.va.value = 0
                robot.vb.value = 0
        
       
        
        robot.x.value =robot.x.value+robot.va.value*dt
        robot.y.value = robot.y.value+robot.vb.value*dt
        
      
      
        barrier.wait()
        
        
        for pa in robots:
            if abs(pa.va.value) > 3.3 or abs(pa.vb.value)> 3.3 :
                all_stopped = False
             
      
        barrier.wait()
        i+=1
        
        
        
    

if __name__ == '__main__':
    start=time.time()
    with Manager() as manager:
        covered_cells = manager.list()
        
        
        
        
        #initialisation obsatcles murs et robots

        #obstacle1=Obstacle(16.0,8.0)
        obstacle3=Obstacle(10.0,6.0)
        obstacle4=Obstacle(10.0,7.0)
        obstacle5=Obstacle(9.0,7.0)
        obstacle6=Obstacle(9.0,6.0)
        obstacle7=Obstacle(3.0,4.0)
        obstacle8=Obstacle(3.0,5.0)
        obstacle9=Obstacle(18.0,6.0)
        obstacle10=Obstacle(18.0,7.0)
        obstacle11=Obstacle(6.0,18.0)
        obstacle12=Obstacle(7.0,18.0)
        obstacle13=Obstacle(13.0,6.0)
        obstacle14=Obstacle(12.0,7.0)
        robot1=Robot(14.0, 14.0,0.0,0.0,0.0,0.0)
        robot2 = Robot(14.0, 15.0,0.0,0.0,0.0,0.0)
        robot3 = Robot(14.0, 16.0,0.0,0.0,0.0,0.0)
        robot4 = Robot(15.0, 14.0,0.0,0.0,0.0,0.0)
        robot5 = Robot(15.0, 15.0,0.0,0.0,0.0,0.0)
        robot6 = Robot(15.0, 16.0,0.0,0.0,0.0,0.0)
        robot7 = Robot(16.0, 14.0,0.0,0.0,0.0,0.0)
        robot8 = Robot(16.0, 15.0,0.0,0.0,0.0,0.0)
        robot9 = Robot(16.0, 16.0,0.0,0.0,0.0,0.0)
        robot10 = Robot(10.0, 7.0,0.0,0.0,0.0,0.0)
        robot11 = Robot(10.0, 6.0,0.0,0.0,0.0,0.0)
        robot12 = Robot(11.0, 5.0,0.0,0.0,0.0,0.0)
        robot13 = Robot(11.0, 8.0,0.0,0.0,0.0,0.0)
        robot14 = Robot(11.0, 9.0,0.0,0.0,0.0,0.0)
        robot15 = Robot(11.0, 4.0,0.0,0.0,0.0,0.0)
        robot16=Robot(11.0, 3.0,0.0,0.0,0.0,0.0)
        
        robots = [robot1, robot2, robot3, robot4, robot5, robot6, robot7, robot8, robot9]
        obstacles=[obstacle3,obstacle4,obstacle5,obstacle6,obstacle7,obstacle8,obstacle9,obstacle10,obstacle11,obstacle12,obstacle14]
        """obstacle3,obstacle4,obstacle5,obstacle6,obstacle7,obstacle8,obstacle9,obstacle10,obstacle11,obstacle12,obstacle14"""
        nbRobots=len(robots)

        for xm in range(taillemap):
            for ym in range(taillemap):
                if xm==0 or xm==taillemap-1 or ym==0 or ym==taillemap-1:
                    nom_obstacle = f"Obstacle_{xm}_{ym}"
                    # Création de l'obstacle et ajout dans la liste avec le nom correspondant  
                    nom_obstacle = Obstacle(xm,ym)
                    obstacles.append(nom_obstacle)
        fig, axmap = plt.subplots()
        for obstacle in obstacles:
            axmap.plot(obstacle.x.value, obstacle.y.value, 'ro')

        # Tracer les robots en bleu
        for robot in robots:
            axmap.plot(robot.x.value, robot.y.value, 'bo')
     
        processes = []
        barrier = multiprocessing.Barrier(nbRobots)
        processes = []
        lock = multiprocessing.Lock()
        
     
        for i in range(nbRobots):
            p = multiprocessing.Process(target=deplacement, args=(robots[i], barrier,lock,i+1,covered_cells,obstacles,robots))
            processes.append(p)
            p.start()
           
        for p in processes:
            p.join()
        
        
        covered_cells = set()  # Créer un ensemble pour stocker les cellules déjà couvertes
        couvrance=0
        for r in range(len(robots)):
            for xc in range(taillemap):
                for yc in range(taillemap):
                    if  (xc-robots[r].x.value)**2+(yc-robots[r].y.value)**2<=rayon:
                        if (xc, yc) not in covered_cells :
                            
                            if obstacle_on_line_of_sight(robots[r], xc, yc, obstacles)==False:
                                #couvrance += 1  # Compter la cellule non comptée
                                covered_cells.add((xc, yc))
        

        
        finish=time.time()
        print("temps", finish-start)
        axmap.cla()
        for obstacle in obstacles:
            axmap.plot(obstacle.x.value, obstacle.y.value, 'ro')

        # Tracer les robots en bleu
        for robot in robots:
            axmap.plot(robot.x.value, robot.y.value, 'bo')

        # Ajouter des étiquettes d'axe et un titre
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Carte avec obstacles et robots')
        print("la couverture est de ",len(covered_cells)*100/(taillemap*taillemap),"%")

        plt.pause(50)


