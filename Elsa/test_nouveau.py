import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Définition de la grille de points
n_points = 100
points = np.random.rand(n_points, 2)

# Définition des positions des robots
n_robots = 4
robot_positions = np.random.rand(n_robots, 2)

# Définition des portées de détection des robots
detection_range = 0.2

# Détermination des cellules de Voronoi pour chaque robot
cell_regions = []
for i in range(len(robot_positions)):
    distances = np.sqrt((points[:, 0] - robot_positions[i][0])**2 + (points[:, 1] - robot_positions[i][1])**2)
    indices = np.argsort(distances)
    region = Voronoi(points[indices[:5]]).regions
    cell_regions.append(region)

# Assignation des cellules à chaque robot
assigned_cells = [[] for i in range(len(robot_positions))]
for i in range(n_points):
    distances = np.sqrt((points[i][0] - robot_positions[:, 0])**2 + (points[i][1] - robot_positions[:, 1])**2)
    indices = np.where(distances < detection_range)[0]
    if indices.size > 0:
        for j in indices:
            if len(assigned_cells[j]) == 0:
                assigned_cells[j].append(i)
            else:
                cells_to_cover = assigned_cells[j]
                is_covered = False
                for cell in cells_to_cover:
                    if len(cells_to_cover) > 1:
                        distances = [np.sqrt((cell[0] - robot_positions[j, 0])**2 + (cell[1] - robot_positions[j, 1])**2) for cell in cells_to_cover if isinstance(cell, tuple)]
                        sorted_indices = np.argsort(distances)
                        cells_to_cover = [cells_to_cover[i] for i in sorted_indices]
                if not is_covered:
                    assigned_cells[j].append(i)


# Initialisation de l'affichage graphique
fig, ax = plt.subplots()
vor = voronoi_plot_2d(Voronoi(points), ax=ax)
robot_plots = [ax.plot([], [], 'o', markersize=10)[0] for i in range(len(robot_positions))]

# Simulation du mouvement des robots pour couvrir les cellules
time_step = 0.01
n_iterations = 10000
for i in range(n_iterations):
    # Vérifier si les robots sont positionnés de manière optimale
    distances = np.min(np.sqrt((points[:, None, 0] - robot_positions[:, 0])**2 + (points[:, None, 1] - robot_positions[:, 1])**2), axis=1)
    if np.all(distances < detection_range):
        break

    for j in range(len(robot_positions)):
        if assigned_cells[j]:
            distances = np.sqrt((points[assigned_cells[j], 0] - robot_positions[j][0])**2 + (points[assigned_cells[j], 1] - robot_positions[j][1])**2)
            cells_to_cover = assigned_cells[j][distances < detection_range]
            if cells_to_cover.size > 0:
                next_point = cells_to_cover[0]
                direction = points[next_point] - robot_positions[j]
                if np.linalg.norm(direction) < 0.01:
                    assigned_cells[j].remove(next_point)
                else:
                    robot_positions[j] += direction * time_step
        robot_plots[j].set_xdata(robot_positions[j][0])
        robot_plots[j].set_ydata(robot_positions[j][1])
        print("Robot", j, "is assigned to cells", assigned_cells[j])
    plt.pause(0.01)

plt.show
