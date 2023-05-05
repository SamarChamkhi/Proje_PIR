import pygame,math,random

# Initialisation de Pygame
pygame.init()
xFenetre = 800
yFenetre = 600

# Création d'une fenêtre
screen = pygame.display.set_mode((xFenetre, yFenetre))

# Informations de l'objet
diam = 10
coul = (200,200,200)

# Définition des coordonnées des sommets
sommets=[[],[],[]]

for i in range(1,10) :
    sommets[0].append(i/10)
    val = math.cos(i)
    if val<0 :
        val = 0
    sommets[2].append(val)
for i in range(1,4,1) :
    sommets[1].append(i/10)

def rand(tab) :
    val = random.randint(0, len(tab)-1)
    val = tab[val]
    return val
    
def posInit(robots : list) :
    xVal = random.randint(0, len(sommets[0])-1)
    robots[0].append(sommets[0][xVal])
    yVal = random.randint(0, len(sommets[1])-1)
    robots[1].append(sommets[1][yVal])
    for i in range (2) : 
        nouv = False
        while nouv==False :
            xVal = random.randint(0, len(sommets[0])-1)
            xVal=sommets[0][xVal]
            for j in range (len(robots[0])):
                if xVal==robots[0][j] :
                    nouv=False
                else :
                    nouv = True
        robots[0].append(xVal)
            
        nouv = False
        while nouv==False :
            yVal = random.randint(0, len(sommets[1])-1)
            yVal=sommets[1][yVal]
            for j in range (len(robots[1])):
                if yVal==robots[1][j] :
                    nouv=False
                else :
                    nouv = True
        robots[1].append(yVal)
    for i in range(len(robots[0])):
        val = math.cos(robots[0][i]*10)
        if val<0 :
            val = 0
        robots[2].append(val)
    return 0

def repartSommets() :
    mult=10
    repart = []
    for i in range (len(sommets[0])) : 
        repart.append([])
        for j in range (len(sommets[1])) :
            repart[i].append(0)
            delta = [500]*len(robots[0])
            for k in range(len(delta)):
                delta[k]=math.sqrt((math.pow(mult*(robots[0][k]-sommets[0][i]), 2) + math.pow(mult*(robots[1][k]-sommets[1][j]), 2)+ math.pow(mult*(robots[2][k]-sommets[2][j]),2)))
            test = min(delta)
            if test == delta[0] :
                repart[i][j]= 0
            elif test == delta[1] :
                repart[i][j]= 1
            else : 
                repart[i][j]= 2
    return repart

#Définition des positions aléatoires initiales des robots
robots = [[],[],[]]
posInit(robots)
repart = repartSommets()
print(repart)
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Effacer l'écran
    screen.fill((255, 255, 255))
    
    #Dessin des sommets vue de côté
    xTaille = xFenetre
    yTaille = 3*yFenetre/4
    for i in range (len(sommets[2])-1):        
        pygame.draw.line(screen, (0, 0, 255), (sommets[0][i]*xTaille,yTaille-sommets[2][i]*yTaille/4),(sommets[0][i+1]*xTaille,yTaille-sommets[2][i+1]*yTaille/4))
    for i in range (len(sommets[2])):
            pygame.draw.circle(screen, coul, (sommets[0][i]*xTaille, yTaille-sommets[2][i]*yTaille/4),diam)
    
    #Dessin des sommets vue de dessus
    xTaille = xFenetre
    yTaille = yFenetre
        
        #lignes 
    for i in range (len(sommets[0])):
        for j in range (len(sommets[1])-1):        
            pygame.draw.line(screen, (0, 0, 255), (sommets[0][i]*xTaille, sommets[1][j]*yTaille),(sommets[0][i]*xTaille, sommets[1][j+1]*yTaille))
    for i in range (len(sommets[0])-1):
        for j in range (len(sommets[1])):        
            pygame.draw.line(screen, (0, 0, 255), (sommets[0][i]*xTaille, sommets[1][j]*yTaille),(sommets[0][i+1]*xTaille, sommets[1][j]*yTaille))
    for i in range (len(sommets[0])-1):
        for j in range (len(sommets[1])-1):        
            pygame.draw.line(screen, (0, 0, 255), (sommets[0][i]*xTaille, sommets[1][j]*yTaille),(sommets[0][i+1]*xTaille, sommets[1][j+1]*yTaille))
            pygame.draw.line(screen, (0, 0, 255), (sommets[0][i+1]*xTaille, sommets[1][j]*yTaille),(sommets[0][i]*xTaille, sommets[1][j+1]*yTaille))
    pygame.draw.line(screen, (0), (0,yFenetre/2),(xFenetre,yFenetre/2),4)        
        
        #sommets
    for i in range (len(sommets[0])):
        for j in range (len(sommets[1])):
            pygame.draw.circle(screen, coul, (sommets[0][i]*xTaille, sommets[1][j]*yTaille),diam)
    
        #Robots
    nbRobot=[[1,0,0],[0,1,0],[0,0,1]]
    for i in range (3):
            pygame.draw.circle(screen,(255*nbRobot[i][0], 255*nbRobot[i][1], 255*nbRobot[i][2]) , (robots[0][i]*xTaille, robots[1][i]*yTaille),diam)
    yTaille = 3*yFenetre/4
    for i in range (3):
            pygame.draw.circle(screen, (255*nbRobot[i][0], 255*nbRobot[i][1], 255*nbRobot[i][2]), (robots[0][i]*xTaille, yTaille-robots[2][i]*yTaille/4),4*(10*robots[1][i]))
    
    

    # Création de la police de caractères
    font = pygame.font.SysFont('Arial', 24)
    # Création de la surface de texte
    text = font.render('Dessus', True, (0, 0, 0))
    # Dessiner la surface de texte sur l'écran
    screen.blit(text, (0,0))
    text = font.render('Côté', True, (0, 0, 0))
    # Dessiner la surface de texte sur l'écran
    screen.blit(text, (0,(yFenetre/2)))
    
    
    
    
    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()