import pygame,math,random,time

#création de l'objet file : 
class File:
    def __init__(self,val=[]):
        self.val = val

    def Enfiler(self,val):
        self.val.append(val)
        
    def Defiler(self) :
        x = self.val[len(self.val)-1]
        self.val.pop()
        return x
        
    def FileVide(self) :
        if self.val==[]: return True
        else : return False

class Sommet:
    def __init__(self,z,color=(0,0,0)):
        self.z = z
        self.color = (color)
    
    def Afficher(self):
        print("Coordonnee z = "+str(self.z)+"\nCouleur : "+str(self.color)+"\n")

# Initialisation de Pygame
pygame.init()

xFenetre = 1000
yFenetre = 1000
screen = pygame.display.set_mode((xFenetre, yFenetre))

# Informations des sommets du graphe
tailleSommet = 4
coulSommet = [
    (0, 255, 0),     # Vert pur
    (0, 0, 255),     # Bleu pur
    (255, 255, 0),   # Jaune
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 128, 0),   # Orange
    (128, 0, 255),   # Violet
    (255, 255, 128), # Beige
    (128, 255, 0),   # Vert lime
    (0, 128, 255)    # Bleu ciel
]
sommet=[]
for i in range(200) :    #à modifier pour nbre sommet en x
    sommet.append([])
    for j in range(200) : #à modifier pour nbre sommet en y
        sommet[i].append(Sommet(0))
        val = math.cos(i/4)
        if val<0 :
            val = 0
        sommet[i][j].z=val

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
        robot[i][2] = sommet[robot[i][0]][robot[i][1]].z
robot=[]
oldRobot=[]
for i in range(10):
    robot.append([0,0,0])
RobotInit(robot)
print(robot)
    
def GestionEvent() :
    global running,robot,oldRobot
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                RobotInit(robot)
                AppartenanceSommet()
                oldRobot=[]
            elif event.key==pygame.K_BACKSPACE:
                CentreMasse()

            
def VueDessus() :
    global sommet,xFenetre,yFenetre,tailleSommet,robot
    xAdapt = xFenetre/len(sommet)
    yAdapt = yFenetre/(len(sommet[0]))
    #sommets
    for i in range (len(sommet)):
        for j in range(len(sommet[i])):
            pygame.draw.circle(screen, sommet[i][j].color, (i*xAdapt+xFenetre/(2*len(sommet)), (j*yAdapt+yFenetre/(2*len(sommet[i])))),tailleSommet)
    #robots
    for i in range(len(robot)):
        pygame.draw.circle(screen,(255,0,0), (robot[i][0]*xAdapt+xFenetre/(2*len(sommet)), (robot[i][1]*yAdapt+yFenetre/(2*len(sommet[robot[i][0]])))),tailleSommet)
    for i in range(len(oldRobot)):
        pygame.draw.circle(screen,(255,0,0), (oldRobot[i][0]*xAdapt+xFenetre/(2*len(sommet)), (oldRobot[i][1]*yAdapt+yFenetre/(2*len(sommet[oldRobot[i][0]])))),tailleSommet)

def VueCote() :
    global sommet,xFenetre,yFenetre,tailleSommet
    xAdapt = xFenetre/len(sommet)
    for i in range(len(sommet)):
        for j in range(0,len(sommet[i]),len(sommet[i])):
            zAdapt = sommet[i][j].z
            pygame.draw.circle(screen, sommet[i][j].color, (i*xAdapt+xFenetre/(2*len(sommet)),yFenetre - zAdapt*yFenetre/4-yFenetre/(2*len(sommet[i]))),tailleSommet)

def AppartenanceSommet() :
    global sommet,coulSommet
    delta = []
    for i in range(len(robot)):
        delta.append(500)
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) :
            for k in range(len(delta)):
                delta[k]=math.sqrt((math.pow(robot[k][0]-i, 2) + math.pow(robot[k][1]-j, 2)))
            test = min(delta)
            for k in range(len(robot)):
                if test == delta[k] :
                    sommet[i][j].color = coulSommet[k]
                    break

def CentreMasse():
    global sommet,coulSommet,robot,oldRobot
    centre=[]
    nbSommet=[]
    for i in range (len(robot)):
        centre.append([0,0])
        nbSommet.append(0)      
    for i in range (len(sommet)):
        for j in range (len(sommet[i])) : 
            for k in range (len(robot)):
                if (sommet[i][j].color==coulSommet[k]):
                    centre[k][0]+=i
                    centre[k][1]+=j
                    nbSommet[k]+=1
                    break
    for i in range(len(robot)):
        oldRobot.append([robot[i][0],robot[i][1]])
        robot[i][0]=int(centre[i][0]/nbSommet[i])
        robot[i][1]=int(centre[i][1]/nbSommet[i])
        robot[i][2] = sommet[robot[i][0]][robot[i][1]].z
    

#Exécution en boucle

running = True
tempsDebut = time.time()
while running:
    GestionEvent()
    screen.fill((255, 255, 255)) 
    #VueCote()
    VueDessus()
    AppartenanceSommet()
    tempsFin = time.time() - tempsDebut
    if tempsFin >0.05 :
        tempsDebut = time.time()
        CentreMasse()
    
    # Texte
    """font = pygame.font.SysFont('Arial', 24)
    text = font.render('Dessus ^', True, (0, 0, 0))
    screen.blit(text, (50,(yFenetre/2)+50))
    text = font.render('Côté v', True, (0, 0, 0))
    screen.blit(text, ((xFenetre/2),(yFenetre/2)+50))"""
  
    
    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()