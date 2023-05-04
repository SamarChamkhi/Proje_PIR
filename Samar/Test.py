import numpy as np
import matplotlib.pyplot as plt


xmin, ymin = 0, 0
xmax, ymax = 60, 60
speed = 0.1

# Initialiser la position du point aléatoirement
position = np.random.uniform(low=[xmin, ymin], high=[xmax, ymax])

# Définir la figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_title('Intrus en mouvement')

# Initialiser les listes pour stocker les positions du point
x_positions = [position[0]]
y_positions = [position[1]]

# Dessiner le point initial
intruder, = ax.plot(position[0], position[1], 'ro')
trace, = ax.plot(x_positions, y_positions, '-k')


# Faire bouger le point de manière aléatoire
while True:
    # Générer une direction de mouvement aléatoire
    direction = np.random.uniform(low=0, high=5, size=2)

    # Normaliser la direction et la multiplier par la vitesse
    direction = speed * direction / np.linalg.norm(direction)

    # Calculer la nouvelle position du point
    new_position = position + direction

    # Vérifier que la nouvelle position est à l'intérieur du plan
    if xmin <= new_position[0] <= xmax and ymin <= new_position[1] <= ymax:
        # Mettre à jour la position du point et ajouter les coordonnées à la liste
        position = new_position
        x_positions.append(position[0])
        y_positions.append(position[1])

        # Mettre à jour la position du point et le dessiner
        position = new_position
        intruder.set_xdata(position[0])
        intruder.set_ydata(position[1])
        trace.set_xdata(x_positions)
        trace.set_ydata(y_positions)
        plt.pause(0.2)
