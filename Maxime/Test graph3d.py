import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


# Définition des coordonnées des deux sommets
coordonnees = [0,2,4,6,8,10]
x = [0]*len(coordonnees)*len(coordonnees)
y = [0]*len(coordonnees)*len(coordonnees)
z = [0]*len(coordonnees)*len(coordonnees)

for i in range(len(coordonnees)) : 
    for j in range(len(coordonnees))  :
        x[i*len(coordonnees)+j]= coordonnees[j]
        y[i*len(coordonnees)+j]=coordonnees[i]
        z[i*len(coordonnees)+j]=0

# Variable pour la pause
paused = False

# Fonction pour calculer les coordonnées d'un point sur la ligne en interpolant entre les deux sommets
def interpolate_points(p1, p2, t):
    x_point = p1[0] + (p2[0] - p1[0]) * t
    y_point = p1[1] + (p2[1] - p1[1]) * t
    z_point = p1[2] + (p2[2] - p1[2]) * t
    return x_point, y_point, z_point

# Fonction pour la mise à jour de la position du point à chaque frame
def update(frame):
    
    # Paramètre t compris entre 0 et 1 pour l'interpolation entre les deux sommets
    t = (frame%100) / 100
    
    if not paused :
        # Coordonnées du point interpolé
        x_point, y_point, z_point = interpolate_points((x[0], y[0], z[0]), (x[1], y[1], z[1]), t)

        # Effacer la figure précédente
        ax.cla()

        # Tracer la ligne et le point
        #ax.plot(x, y, z)
        for i in range (len(x)) :
            ax.scatter(x[i], y[i], z[i],color='green', s=50)
        ax.scatter(x_point, y_point, z_point, color='red', s=50)

    return fig,

# Fonction pour mettre en pause ou reprendre l'animation
def toggle_pause(event):
    global paused
    paused = not paused
    
# Création de la figure et de l'objet Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Définition des limites de la figure
ax.set_xlim3d([min(x), max(x)])
ax.set_ylim3d([min(y), max(y)])
ax.set_zlim3d([min(z), max(z)])

# Création du bouton "pause"
button_ax = plt.axes([0.9, 0.05, 0.1, 0.075])
button = Button(button_ax, 'Pause')
button.on_clicked(toggle_pause)

# Création de l'animation
animation = FuncAnimation(fig, update, frames=100000, interval=1000000)

# Affichage de l'animation
plt.show()
print(x)