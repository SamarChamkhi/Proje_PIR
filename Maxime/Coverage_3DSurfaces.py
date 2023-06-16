from vpython import *
import math,random,time
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
        self.distRobProche = 0

canvas(title='Coverage on 3D surface',
     width=1000, height=1000,
     center=vector(0,0,0), background=color.black)

# Informations des sommets du graphe
tailleSommet = 0.7
coulSommet = [
    color.green,    #Vert 
    color.white,   #Blanc
    color.blue,   # Bleu
    color.cyan,   # Cyan
    color.magenta,   # Magenta
    color.orange,   # Orange
    color.purple,   # Violet
    color.yellow, # Jaune
    color.black,   #Noir
]
sommet=[]
calculSommet = []
repet =0

#Changement des paramètres

a = 55     #modification nombre de sommets en x
b = 55    #modification nombre de sommets en y
debut = True #placer les robots aléatoirement
euclid = True #changer la méthode de calcul
nbreRobot =  3
max = 1    #nombre de boucles pour moyennage des mesures de temps et de distance moyenne robot/sommet
nbreGaussiennes = 10 
alea = False     #placement aléatoire des gaussiennes (False = 1 gaussienne placée au centre)


def Carre() :
    global sommet,calculSommet
    for i in range(len(sommet)) :     
        for j in range(len(sommet[i])) :
            val = len(sommet)/4
            if i<=len(sommet)/4 or i>len(sommet)*3/4 or j<=len(sommet[i])/4 or j>len(sommet[i])*3/4:
                val = 0
            sommet[i][j].pos.y=calculSommet[i][j].z = val
def Cos() :
    global sommet,calculSommet
    for i in range(len(sommet)) :
        for j in range(len(sommet[i])) :
            val = 0
            val = math.cos((i+a/2)/4)+math.cos((j+b/2)/4)
            if val<0 :
                val = 0
            sommet[i][j].pos.y=calculSommet[i][j].z = 4*val
    
def Gaussienne(nbre = 1) :
    global sommet,calculSommet,alea
    courbes = []
    for k in range (nbre) :
        courbes.append([0,0,0])
        courbes[k][0] = random.randint(1,15)
        courbes[k][1] = random.randint(1, len(sommet)-1)
        courbes[k][2] = random.randint(1, len(sommet[0])-1)
    if alea == False : 
        for i in range(len(sommet)) :
            for j in range(len(sommet[i])) : 
                sommet[i][j].pos.y=calculSommet[i][j].z = 1/2*a*math.exp(-1/(a*6)*math.pow(i-a/2,2)-1/(b*6)*math.pow(j-b/2,2))
    else :
       for i in range(len(sommet)) :
            for j in range(len(sommet[i])) : 
                val = 0
                for k in range (nbre) :
                    val += courbes[k][0]*math.exp(-1/(courbes[k][1])*math.pow(i-courbes[k][1],2)-1/(courbes[k][2])*math.pow(j-courbes[k][2],2))
                sommet[i][j].pos.y=calculSommet[i][j].z = val

#Initialisation

moyRes = []
moyCouv = []
tempsExec = 0
couverture = 0
for i in range(a) :
    sommet.append([])
    calculSommet.append([])
    for j in range(b) :
        calculSommet[i].append(Sommet(i,j,0))
        sommet[i].append(sphere(pos = vector(i-a/2,0,j-b/2),radius = tailleSommet,color = color.white,neighbors = []))

Gaussienne(nbreGaussiennes)
#Carre()
#Cos()

for i in range(len(sommet)) :
    for j in range(len(sommet[i])) : 
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
for i in range(nbreRobot):
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
def Relance ():
    global running,robot,oldRobot,tempsTot
    if debut == True : 
        RobotInit(robot)
    else : 
        for i in range(len(robot)):
            robot[i] = [i,i,0]
    AppartenanceSommet()
    oldRobot=[]
    running = True
    tempsTot = time.time()
    Gaussienne(nbreGaussiennes)
            
def GestionEvent() :
    global running,robot,oldRobot,tempsTot,boucle
    k = keysdown()
    if ' ' in k :
        Relance()

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
    
def calcul(delta :list,i,j) :
    for k in range(len(delta)):
        if euclid ==False :
            delta[k]=ParcoursLargeur(calculSommet[i][j], calculSommet[robot[k][0]][robot[k][1]])
        else : 
            delta[k]=math.sqrt((math.pow(robot[k][0]-i, 2) + math.pow(robot[k][1]-j, 2)+ math.pow(robot[k][2]-sommet[i][j].pos.y, 2)))
        test = min(delta)
        for k in range(len(robot)):
            if test == delta[k]:
                calculSommet[i][j].color = coulSommet[k]
                calculSommet[i][j].distRobProche=test
                break
     
def AppartenanceSommet() :
    global sommet,coulSommet
    delta = []
    pool = ThreadPoolExecutor (max_workers=2)  # Nombre de threads ou de processus souhaité --> NE MARCHE PAS AU FINAL
    for i in range(len(robot)):
        delta.append(500)
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) :
            if EstRobot (i,j)==False :
                pool.submit(calcul(delta,i,j))
            sommet[i][j].color = calculSommet[i][j].color
    pool.shutdown()
                

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
    if len(oldRobot)>=len(robot)*2 :
            for i in range(len(robot)):
                oldRobot.pop(0)
    for i in range(len(robot)):
        oldRobot.append([robot[i][0],robot[i][1]])
        robot[i][0]=int(centre[i][0]/nbSommet[i])
        robot[i][1]=int(centre[i][1]/nbSommet[i])
        robot[i][2] = int(centre[i][2]/nbSommet[i])


#Boucle : 
running = True
tempsDebut = time.time()
tempsTot = time.time()
boucle = 1
while True : 
    GestionEvent()
    while running:
        AppartenanceSommet()
        tempsFin = time.time() - tempsDebut
        tempsDebut = time.time()
        CentreMasse()
        test = 0
        if len(oldRobot) >= 2*len(robot) :
            for k in range (len(robot)) :
                if oldRobot[k][0] == oldRobot[k+len(robot)][0] and oldRobot[k][1] == oldRobot[k+len(robot)][1] :
                    test +=1
        if test >=len(robot) :
            fin = time.time()
            moyRes.append(fin - tempsTot)
            val = 0
            if euclid == True :
                euclid = False
                delta=[]
                for i in range(len(robot)):
                    delta.append(500)
                for i in range(len(calculSommet)):
                    for j in range(len(calculSommet[i])) :
                        if EstRobot (i,j)==False :
                            calcul(delta,i,j)
                            val+=calculSommet[i][j].distRobProche
                euclid = True
            for i in range(len(calculSommet)):
                    for j in range(len(calculSommet[i])) :
                            val+=calculSommet[i][j].distRobProche
            val = val/(len(calculSommet)*len(calculSommet[0]))
            moyCouv.append(val)
            tempsExec=0
            couverture=0
            for i in range (len(moyRes)):
                tempsExec+=moyRes[i]
            tempsExec = tempsExec/len(moyRes)
            for i in range (len(moyCouv)):
                couverture+=moyCouv[i]
            couverture = couverture/len(moyCouv)
            
            if (boucle<max):
                Relance()
                boucle+=1
            else :
                if (euclid ==True):
                    print("En distance euclidienne :")
                else : 
                    print("En parcours en largeur :")
                print("Fin de convergence : \nTemps d'execution moyen : ",tempsExec,"s pour ",boucle," de fois\nDistance moyenne des sommets a leur robots : ",couverture,"\nEuclid = ",euclid,"\n\n") 
                repet +=1
                if repet>=2:
                    running = False
                else :
                    boucle=1
                    euclid = False