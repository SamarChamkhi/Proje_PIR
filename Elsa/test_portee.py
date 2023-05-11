import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import random

# Définition de la grille de points
n_points = 4
points = np.random.rand(n_points, 2)

# Définition des positions des robots
n_robots = 4
robot_positions = np.random.rand(n_robots, 2)

# Détermination des cellules de Voronoi pour chaque robot
cell_regions = []
for i in range(len(robot_positions)):
    distances = np.sqrt((points[:, 0] - robot_positions[i][0])**2 + (points[:, 1] - robot_positions[i][1])**2)
    indices = np.argsort(distances)
    region = Voronoi(points[indices[:5]]).regions
    cell_regions.append(region)

# Définition des portées de détection des robots
detection_range = 0.3

# Assignation des cellules à chaque robot
assigned_cells = [[] for i in range(len(robot_positions))]
for i in range(n_points):
    distances = np.sqrt((points[i][0] - robot_positions[:, 0])**2 + (points[i][1] - robot_positions[:, 1])**2)
    for j in range(n_robots):
        if distances[j] < detection_range:
            assigned_cells[j].append(i)

# Calcul des trajectoires pour chaque robot
trajectories = []
for i in range(len(robot_positions)):
    current_pos = robot_positions[i]
    cells_to_cover = assigned_cells[i]
    trajectory = []
    while cells_to_cover:
        distances = np.sqrt((points[cells_to_cover, 0] - current_pos[0])**2 + (points[cells_to_cover, 1] - current_pos[1])**2)
        index = np.argmin(distances)
        trajectory.append(cells_to_cover[index])
        current_pos = points[cells_to_cover[index]]
        cells_to_cover.pop(index)
    trajectories.append(trajectory)

# Initialisation de l'affichage graphique
fig, ax = plt.subplots()
vor = voronoi_plot_2d(Voronoi(points), ax=ax)
robot_plots = [ax.plot([], [], 'o', markersize=10)[0] for i in range(len(robot_positions))]
circle_plots = [ax.add_patch(plt.Circle((robot_positions[i][0], robot_positions[i][1]), detection_range, fill=False)) for i in range(len(robot_positions))]

# Simulation du mouvement des robots pour couvrir les cellules
time_step = 0.1
n_iterations = 1000
for i in range(n_iterations):
    # Vérifier si les robots sont positionnés de manière optimale
    distances = np.min(np.sqrt((points[:, None, 0] - robot_positions[:, 0])**2 + (points[:, None, 1] - robot_positions[:, 1])**2), axis=1)
    if np.all(distances < detection_range):
        break
    
    for j in range(len(robot_positions)):
        if trajectories[j]:
            next_point = trajectories[j][0]
            direction = points[next_point] - robot_positions[j]
            if np.linalg.norm(direction) < 0.01:
                trajectories[j].pop(0)
            else:
                robot_positions[j] += direction * time_step
        robot_plots[j].set_xdata(robot_positions[j][0])
        robot_plots[j].set_ydata(robot_positions[j][1])
        circle_plots[j].center = robot_positions[j]
    plt.pause(0.001)
    

    
plt.show()
