import math
import numpy as np
import time 
import matplotlib.pyplot as plt
class Robot:
    def __init__(self, x, y,va,vb):
        self.x = x
        self.y = y
        self.va = va
        self.vb = vb
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
def obstacle_on_line_of_sight(P1, P2, obstacles):
    x1=P1.x
    y1 = P1.y
    x2, y2 = P2.x, P2.y
    if x1 == x2:  # Vérifier si la ligne est verticale
        for obstacle in obstacles:
            if obstacle.x == x1 and min(y1, y2) <= obstacle.y <= max(y1, y2):
                return True
        return False
    else:
        if y1 == y2:  # Vérifier si la ligne est horizontale
            for obstacle in obstacles:
                if obstacle.y == y1 and min(x1, x2) <= obstacle.x <= max(x1, x2):
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
                    intersection_y = m * (obstacle.x - x1) + y1
                    if obstacle.y == intersection_y and min(x1, x2) <= obstacle.x <= max(x1, x2):
                        return True
                return False

        
taillemap=30

ko=20.0
k1=40.0
b = 6
rayon=1000.01
dt = 0.3
m_i=1.0



#initialisation obsatcles murs et robots
"""
obstacle1=Obstacle(16.0,8.0)
obstacle3=Obstacle(10.0,6.0)
obstacle4=Obstacle(10.0,7.0)
obstacle5=Obstacle(9.0,7.0)
obstacle6=Obstacle(9.0,6.0)"""
robot1=Robot(14.0, 14.0,0.0,0.0)
robot2 = Robot(14.0, 15.0,0.0,0.0)
robot3 = Robot(14.0, 16.0,0.0,0.0)
robot4 = Robot(15.0, 14.0,0.0,0.0)
robot5 = Robot(15.0, 15.0,0.0,0.0)
robot6 = Robot(15.0, 16.0,0.0,0.0)
robot7 = Robot(16.0, 14.0,0.0,0.0)
robot8 = Robot(16.0, 15.0,0.0,0.0)
robot9 = Robot(16.0, 16.0,0.0,0.0)
robot10 = Robot(10.0, 7.0,0.0,0.0)
robot11 = Robot(10.0, 6.0,0.0,0.0)
robot12 = Robot(11.0, 5.0,0.0,0.0)
robot13 = Robot(11.0, 8.0,0.0,0.0)
robot14 = Robot(11.0, 9.0,0.0,0.0)
robot15 = Robot(11.0, 4.0,0.0,0.0)
robot16=Robot(11.0, 3.0,0.0,0.0)
robots = [robot1,robot2,robot3,robot4,robot5,robot6,robot7,robot8,robot9]
""",robot2,robot3,robot4,robot5,robot6,robot7,robot8,robot9,robot10,robot11,robot12,robot13,robot14,robot15,robot16 """
obstacles=[]
nbRobots=len(robots)
fig, axmap = plt.subplots()

#création graphique couverture
fig2 = plt.figure(figsize=(15, 10))
ax_couv=fig2.add_subplot(3, 2, 1)
ax_couv.set_title("couverture")
ax_couv.set_ylabel("m²")


for xm in range(taillemap):
    for ym in range(taillemap):
        if xm==0 or xm==taillemap-1 or ym==0 or ym==taillemap-1:
            nom_obstacle = f"Obstacle_{xm}_{ym}"
            # Création de l'obstacle et ajout dans la liste avec le nom correspondant  
            nom_obstacle = Obstacle(xm,ym)
            obstacles.append(nom_obstacle)



for obstacle in obstacles:
    axmap.plot(obstacle.x, obstacle.y, 'ro')

    # Tracer les robots en bleu
for robot in robots:
    axmap.plot(robot.x, robot.y, 'bo')

# Ajouter des étiquettes d'axe et un titre
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Carte avec obstacles et robots')
plt.pause(25)
    # Créer une figure et un axe
all_stopped = False
i=0
start_time = time.time()
while not all_stopped: 
    all_stopped = True
    for robot in robots:
        F_friction_x = 0.0
        F_friction_y = 0.0
        ra=robot.x
        rb=robot.y
        F_obs_x =0.0
        F_obs_y=0.0
        
        for o in obstacles:
            xo=o.x
            yo=o.y
            distance=math.sqrt(math.pow((yo-rb),2)+math.pow((xo-ra),2))
            if  distance<=rayon:
                if rb-yo!=0 or ra-xo!=0 : 
                    F_obs_x += ko*(((ra-xo)/distance**3))   
                    F_obs_y += ko*(((rb-yo)/distance**3))
               
        for rr in robots:
            xr=rr.x
            yr=rr.y
            distance=math.sqrt((yr-rb)**2+(xr-ra)**2)
            if  distance<=rayon:
                if rb-yr!=0 or ra-xr!=0 : 
                    F_obs_x += k1*(((ra-xr)/(distance)**3))   
                    F_obs_y += k1*(((rb-yr)/(distance)**3))
                    
        if F_obs_y==0 and F_obs_x==0:
            robot.va=0
            robot.vb=0
            F_friction_x=0
            F_friction_y=0
            
        F_friction_x = -b * robot.va
        F_friction_y = -b * robot.vb
        F_total_x =F_friction_x+F_obs_x
        F_total_y = F_friction_y+F_obs_y
        if F_total_x==0 and F_total_y==0:
            robot.va=0
            robot.vb=0
        ax = F_total_x / m_i
        ay = F_total_y / m_i
        
        if abs(ax) > 30:
            ax = 30 if ax > 0 else -30
        if abs(ay) > 30:
            ay = 30 if ay > 0 else -30
        if abs(ax) < 18:
            ax = 0 if ax > 0 else -0
        if abs(ay) < 18:
            ay = 0 if ay > 0 else -0
        
        
        robot.va =robot.va+ ax * dt
        robot.vb = robot.vb+ay * dt
        
        if abs(robot.va) < 3.3 and abs(robot.vb) < 3.3:
            robot.va = 0
            robot.vb = 0
        
        """if abs(robot.va) >=3.4:
            robot.va =robot.va+ ax * dt
        if abs(robot.vb) >=3.4:
            robot.vb = robot.vb+ay * dt"""
       
      
        robot.x =robot.x+robot.va*dt
        robot.y = robot.y+robot.vb*dt
        
        if robot.va != 0 or robot.vb != 0 :
            all_stopped = False
        

        
    # Dessiner les obstacles en rouge
    for obstacle in obstacles:
        axmap.plot(obstacle.x, obstacle.y, 'ro')
        

    # Tracer les robots en bleu
    for azzzz in robots:
        axmap.plot(azzzz.x,azzzz.y, 'bo')

        
    covered_cells = set()  # Créer un ensemble pour stocker les cellules déjà couvertes
    couvrance=0
    for r in range(len(robots)):
        for xc in range(taillemap):
            for yc in range(taillemap):
                if  (xc-robots[r].x)**2+(yc-robots[r].y)**2<=rayon:
                    if (xc, yc) not in covered_cells :
                        for o in obstacles:
                            if obstacle_on_line_of_sight(robots[r], o, obstacles)==False:
                                #couvrance += 1  # Compter la cellule non comptée
                                covered_cells.add((xc, yc))
    ax_couv.plot(i, len(covered_cells)*100/(taillemap*taillemap), 'ro')
    # Ajouter des étiquettes d'axe et un titre
    plt.pause(0.0001)
    if all_stopped==False:
        axmap.cla()
    i+=1
finally_time = time.time()
print("c'est fini")
print("temps d'exécution =",finally_time-start_time)
print("couverture de",len(covered_cells)*100/(taillemap*taillemap),"%")
plt.pause(50)
plt.show()
# covered_cells = set()  # Créer un ensemble pour stocker les cellules déjà couvertes
# couvrance=0   
# for r in range(len(robots)):
    # for xc in range(taillemap):
        # for yc in range(taillemap):
            # if  (xc-robots[r].x)**2+(yc-robots[r].y)**2<=rayon:
                # if (xc, yc) not in covered_cells :
                    # obstacle_on_line_of_sight(robots[r],o , obstacles)
                    # couvrance += 1  # Compter la cellule non comptée
                    # covered_cells.add((xc, yc))  # Ajouter la cellule au ensemble des cellules déjà couverte
# couvrance2=0                       
# for xc in range(taillemap):
        # for yc in range(taillemap):
                # if  (xc-10)**2+(yc-10)**2<=16.01:
                    # couvrance2 += 1
                        
# couvrance2=couvrance2*nbRobots
# print("On a une couvrance de ", couvrance, "m² soit ", couvrance*100/(taillemap*taillemap), " % ou bien", couvrance*100/couvrance2, " de la couvrance possible")
# couvrance2=0
# for xc2 in range(taillemap):
    # for yc2 in range(taillemap):
            # if  (xc2-10)**2+(yc2-10)**2<=16.01:
                # couvrance2 += 1
                    




