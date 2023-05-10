from vpython import *

# Création de la fenêtre graphique
scene = canvas()

# Création de la surface
surface = ParametricSurface(
    func=lambda u, v: vector(u, v, sin(u*v)),
    umin=-5, umax=5, vmin=-5, vmax=5,
    texture=textures.earth
)

# Ajout de la surface à la scène
scene.append(surface)

# Ajout d'une source lumineuse
scene.lights = [distant_light(direction=vector(0.2, 0.2, 0.2))]

# Boucle de rendu
while True:
    rate(30)  # Limite le taux de rafraîchissement à 30 images par seconde
