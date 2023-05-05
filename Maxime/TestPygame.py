import pygame,random,time

# Initialisation de Pygame
pygame.init()
xFenetre = 800
yFenetre = 600

# Création d'une fenêtre
screen = pygame.display.set_mode((xFenetre, yFenetre))

# Informations de l'objet
diam = 15
v = 4

# Définition des coordonnées des sommets
xCoordonnees = [0.2,0.4,0.5,0.6,0.8]
yCoordonnees = [0.2,0.4,0.6,0.8]

"""for i in range(10,40, 10):
    xCoordonnees.append(i/100)
for i in range(40, 60, 6):
    xCoordonnees.append(i/100)
for i in range(60, 90, 10):
    xCoordonnees.append(i/100)
for i in range(1, 9, 2):
    yCoordonnees.append(i/10)"""    

    
def robotCoord():
    xRobot = random.randint(0, len(xCoordonnees)-1)
    xRobot = xCoordonnees[xRobot]*xFenetre
    yRobot = random.randint(0, len(yCoordonnees)-1)
    yRobot = yCoordonnees[yRobot]*yFenetre
    return xRobot, yRobot

def deplacRobot(robotOldCoords:list,robotNewCoords:list) : 
    old = robotOldCoords[:]
    while (old[0]<robotNewCoords[0]-5 or old[0]>robotNewCoords[0]+5) and (old[1]<robotNewCoords[1]-5 or old[1]>robotNewCoords[1]+5) :
        deltaX = old[0]-robotNewCoords[0]
        deltaY = old[1]-robotNewCoords[1]
        old[0]+=(deltaX/v)
        old[1]+=(deltaY/v)
        background()
        pygame.draw.circle(screen, (0, 250, 0), (old[0], old[1]),diam)
    
        # Rafraîchir l'écran
        pygame.display.flip() 

def background() :
        # Effacer l'écran
        screen.fill((255, 255, 255))

        # Dessiner le pavage des cercles
        for i in range (len(xCoordonnees)):
            for j in range (len(yCoordonnees)):
                pygame.draw.circle(screen, (255, 131, 0), (xCoordonnees[i]*xFenetre, yCoordonnees[j]*yFenetre),diam)

 


# Boucle principale
robotNewCoords = robotCoord()
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Gestion des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        robotOldCoords = robotNewCoords
        robotNewCoords = robotCoord()
        #deplacRobot(robotOldCoords,robotNewCoords)
        time.sleep(0.1)
         
    background ()
               
    pygame.draw.circle(screen, (0, 250, 0), (robotNewCoords[0], robotNewCoords[1]),diam)

    # Rafraîchir l'écran
    pygame.display.flip()

# Quitter Pygame
pygame.quit()