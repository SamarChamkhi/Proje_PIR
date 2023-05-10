from vpython import *
import pygame,math,random,time

# Informations des sommets du graphe
tailleSommet = 1
coulSommet = [
    color.green,     
    color.black,     
    color.blue,   # Jaune
    color.cyan,   # Magenta
    color.magenta,   # Cyan
    color.orange,   # Orange
    color.purple,   # Violet
    color.white, # Beige
    color.yellow,   # Vert lime
]
sommet=[]
a = 50
b = 50
for i in range(a) :    #à modifier pour nbre sommet en x
    sommet.append([])
    for j in range(b) : #à modifier pour nbre sommet en y
        sommet[i].append(sphere(pos = vector(i-a/2,0,j-b/2),radius = tailleSommet,color = color.white))
        val = math.cos(i/4)+math.cos(j/4)
        if val<0 :
            val = 0
        sommet[i][j].pos.y=val

def RobotInit(robot:list):
    robot[0][0] = random.randint(0, len(sommet)-1)
    robot[0][1] = random.randint(0, len(sommet[0])-1)
    for i in range (1,len(robot)) : 
        nouv = False
        while nouv==False :
            xVal = random.randint(0, len(sommet)-1)
            yVal = random.randint(0, len(sommet[0])-1)
            for j in range (len(robot)):
                if robot[j]!=[] :
                    if xVal==robot[j][0] and yVal==robot[j][1]:
                        nouv=False
                    else :
                        nouv = True
        robot[i][0] = xVal
        robot[i][1] = yVal
    for i in range(len(robot)):
        robot[i][2] = sommet[robot[i][0]][robot[i][1]].pos.y
robot=[]
oldRobot=[]
debut = True
for i in range(9):
    robot.append([i,i,0])
if debut == True : 
    RobotInit(robot)
    
def EstRobot (a,b):
    global sommet,robot
    for k in range(len(robot)):
        if a==robot[k][0] and b==robot[k][1]:
            sommet[a][b].color =color.red
            return True
    return False

def GestionEvent() :
    global running,robot,oldRobot
    k = keysdown()
    if 'left' in k:
            if debut == True : 
                RobotInit(robot)
            else : 
                for i in range(9):
                    robot[i] = [i,i,0]
            AppartenanceSommet()
            oldRobot=[]        
          
def AppartenanceSommet() :
    global sommet,coulSommet
    delta = []
    for i in range(len(robot)):
        delta.append(500)
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) :
            if EstRobot (i,j)==False :    
                for k in range(len(delta)):
                    delta[k]=math.sqrt((math.pow(robot[k][0]-i, 2) + math.pow(robot[k][1]-j, 2)+ math.pow(robot[k][2]-sommet[i][j].pos.y, 2)))
                test = min(delta)
                for k in range(len(robot)):
                    if test == delta[k]:
                        sommet[i][j].color = coulSommet[k]
                        break

def ProjSurface(k,robot : list) :
    global sommet
    delta = []
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) :
            val = math.sqrt((math.pow(robot[k][0]-i, 2) + math.pow(robot[k][1]-j, 2)+ math.pow(robot[k][2]-sommet[i][j].pos.y, 2)))
            delta.append(val)
    test = min(delta)
    for i in range (len(delta)) :
        if delta[i]==test : 
            a = math.floor(i/len(sommet[0]))
            b = i%len(sommet[0])
            break
    robot[k][0] = a
    robot[k][1] = b
    robot[k][2] = sommet[a][b].pos.y
    
def CentreMasse():
    global sommet,coulSommet,robot,oldRobot
    centre=[]
    nbSommet=[]
    for i in range (len(robot)):
        centre.append([0,0,0])
        nbSommet.append(1)      
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) : 
            for k in range (len(robot)):
                if (sommet[i][j].color==coulSommet[k]):
                    centre[k][0]+=i
                    centre[k][1]+=j
                    centre[k][2]+=sommet[i][j].pos.y
                    nbSommet[k]+=1
                    break
    for i in range(len(robot)):
        oldRobot.append([robot[i][0],robot[i][1]])
        robot[i][0]=int(centre[i][0]/nbSommet[i])
        robot[i][1]=int(centre[i][1]/nbSommet[i])
        robot[i][2] = int(centre[i][2]/nbSommet[i])


running = True
tempsDebut = time.time()
while running:
    rate(60)
    GestionEvent()
    AppartenanceSommet()
    tempsFin = time.time() - tempsDebut
    if tempsFin >0.05 :
        tempsDebut = time.time()
        CentreMasse()
    