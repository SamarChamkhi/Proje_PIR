TAILLE = 6
NOMBRE_ROBOTS = 4
PORTEE = 2 # portee de detection, la portee de couverture du robot en fait la moitié


def espace (size) :
    global tab
    tab = [[' ' for j in range(size)] for i in range(size)]

    for i in range (size) :
        tab[i][0]= '1'
        tab[i][size-1] = '1'

    for j in range (size) :
        tab [0][j] = '1'
        tab [size-1][j] = '1'
    
    affiche(tab, size)
        

def creer_robots (number, size, t):
    for i in range (round(number/2)) :
        for j in range (round(number/2)) :
            t[round(size/2)+i-1][round(size/2)+j-1] = '0'
    affiche(t, size)
   

def mouvement_robots (t, size, stable, portee) :
    while stable == False :
        stable = True
        for i in range (size-1) :
            for j in range (size-1) :
                if t[i][j] == '0' : # si on arrive a la position d'un robot
                    for k in range (portee) :
                        for l in range (portee) :
                            if t[i+k-round(portee/2)][j+l-round(portee/2)] == '1' : # s'il y a un obstable dans sa portee de couverture
                                t[i][j] = ' '
                                t[i-k+round(portee/2)][j-l+round(portee/2)] = '0' # le robot se déplace à l'opposé
                                stable = False
                                affiche(t, size)
                    for k in range (2*portee) :
                        for l in range (2*portee) :
                            if t[i+k-portee][j+l-portee] == '0' and (k-portee!='0' or l-portee!='0') : # s'il y a un obstacle dans sa portee de détection
                                t[i][j] = ' '
                                if k-portee > 0 and l-portee > 0:
                                    t[i-1][j-1] = '0'
                                    stable = False
                                    affiche(t, size)
                                elif k-portee == 0 and l-portee > 0:
                                    t[i][j-1] = '0'
                                    stable = False
                                    affiche(t, size)  
                                elif k-portee < 0 and l-portee > 0:
                                    t[i+1][j-1] = '0'
                                    stable = False
                                    affiche(t, size)  
                                elif k-portee > 0 and l-portee < 0:
                                    t[i-1][j+1] = '0'
                                    stable = False
                                    affiche(t, size)
                                elif k-portee == 0 and l-portee < 0:
                                    t[i][j+1] = '0'
                                    stable = False
                                    affiche(t, size)     
                                elif k-portee < 0 and l-portee < 0:
                                    t[i+1][j+1] = '0'
                                    stable = False
                                    affiche(t, size)
                                elif k-portee > 0 and l-portee == 0:
                                    t[i-1][j] = '0'
                                    stable = False
                                    affiche(t, size)   
                                elif k-portee < 0 and l-portee == 0:
                                    t[i+1][j] = '0'
                                    stable = False
                                    affiche(t, size)   
                                    
                                
                            
                                


def affiche (t, size) :
    for i in range (size) :
        for j in range (size) :
            print (t[i][j], end ="")
        print("")
    print("\n")

if __name__ == '__main__':

    espace(TAILLE+2)
    creer_robots(NOMBRE_ROBOTS,TAILLE+2,tab)
    stable = False # renseigne l'état du système
    mouvement_robots(tab, TAILLE+2, stable, PORTEE)
