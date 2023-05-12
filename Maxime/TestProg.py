from vpython import *
import math,random,time,os
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class Sommet:
    def __init__(self,x,y,z,color=(0,0,0),neighbors=[]):
        self.x = x
        self.y = y
        self.z = z
        self.color = (color)
        self.neighbors = neighbors
        self.marque = False

canvas(title='Coverage on 3D surface',
     width=1000, height=1000,
     center=vector(0,0,0), background=color.black)

# Informations des sommets du graphe
tailleSommet = 0.7
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
calculSommet = []
a = 25
b = 25
for i in range(a) :    #à modifier pour nbre sommet en x
    sommet.append([])
    calculSommet.append([])
    for j in range(b) : #à modifier pour nbre sommet en y
        calculSommet[i].append(Sommet(i,j,0))
        sommet[i].append(sphere(pos = vector(i-a/2,0,j-b/2),radius = tailleSommet,color = color.white,neighbors = []))
        val = math.cos((i+a/2)/4)+math.cos((j+b/2)/4)
        if val<0 :
            val = 0
        sommet[i][j].pos.y=val*4
        calculSommet[i][j].z = val*4
for i in range(len(sommet)) :    #à modifier pour nbre sommet en x
    for j in range(len(sommet[i])) : #à modifier pour nbre sommet en y
        neighborsSomm = []
        for k in range (-1,2):
            for l in range (-1,2) :
                if k==0 and l==0 or i+k<0 or j+l<0 or i+k>=len(sommet) or j+l>=len(sommet[i]):
                    continue
                else :
                    neighborsSomm.append(calculSommet[i+k][j+l])
        calculSommet[i][j].neighbors = neighborsSomm


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
for i in range(3):
    robot.append([i,i,0])
if debut == True : 
    RobotInit(robot)
    
def EstRobot (a,b):
    global sommet,robot
    for k in range(len(robot)):
        if a==robot[k][0] and b==robot[k][1]:
            calculSommet[a][b].color =color.red
            return True
    return False

def GestionEvent() :
    global running,robot,oldRobot
    k = keysdown()
    if ' ' in k:
            if debut == True : 
                RobotInit(robot)
            else : 
                for i in range(9):
                    robot[i] = [i,i,0]
            AppartenanceSommet()
            oldRobot=[]        

def ParcoursLargeur(start, end):
    f = Queue()
    f.put(start)    
    visited = set()
    visited.add(start)

    predecessor = {}
    predecessor[start] = None

    while not f.empty():
        start = f.get()
        if start == end:
            break
        for neighbor in start.neighbors:
            if neighbor not in visited:
                f.put(neighbor)
                visited.add(neighbor)
                predecessor[neighbor] = start
    # Reconstruction du plus court chemin
    path = []
    node = end
    val = 0

    while node is not None:
        path.insert(0, node)
        node = predecessor[node]
    for i in range (len(path)-1) : 
        val += math.sqrt((math.pow(path[i].x - path[i+1].x, 2) + math.pow(path[i].y - path[i+1].y, 2)+ math.pow(path[i].z - path[i+1].z, 2)))

    return val
    
def calcul(delta: list, i, j):
    for k in range(len(delta)):
        delta[k] = ParcoursLargeur(calculSommet[i][j], calculSommet[robot[k][0]][robot[k][1]])
    test = min(delta)
    for k in range(len(robot)):
        if test == delta[k]:
            calculSommet[i][j].color = coulSommet[k]
            break

def AppartenanceSommet():
    global sommet, coulSommet
    delta = []
    for i in range(len(robot)):
        delta.append(500)
    for i in range(len(sommet)):
        for j in range(len(sommet[i])):
            if EstRobot(i, j) == False:
                calcul(delta, i, j)

def calcul_parallel(delta: list, i, j):
    delta_val = ParcoursLargeur(calculSommet[i][j], calculSommet[robot[0][0]][robot[0][1]])
    delta.put((i, j, delta_val))

def AppartenanceSommet_parallel():
    global sommet, coulSommet
    delta = Queue()
    for i in range(len(sommet)):
        for j in range(len(sommet[i])):
            if EstRobot(i, j) == False:
                pool.submit(calcul_parallel, delta, i, j)
    pool.shutdown()

    while not delta.empty():
        i, j, delta_val = delta.get()
        calculSommet[i][j].color = coulSommet[delta_val]
        
                

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
with ProcessPoolExecutor(max_workers=2) as pool:
    while running:
        GestionEvent()
        AppartenanceSommet_parallel()
        tempsFin = time.time() - tempsDebut
        if tempsFin > 0.05:
            tempsDebut = time.time()
            CentreMasse()
