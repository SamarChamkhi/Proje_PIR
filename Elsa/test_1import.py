import random
from scipy.spatial import Voronoi

# Définition de la grille de points
n_points = 50
points = [(random.uniform(0, 1), random.uniform(0, 1)) for i in range(n_points)]

# Définition des positions des robots
robot_positions = [(0, 0), (1, 0), (0, 1), (1, 1)]

# Détermination des cellules de Voronoi pour chaque robot
cell_regions = []
for i in range(len(robot_positions)):
    distances = [(points[j][0] - robot_positions[i][0])**2 + (points[j][1] - robot_positions[i][1])**2 for j in range(n_points)]
    indices = sorted(range(n_points), key=lambda k: distances[k])[:5]
    region = Voronoi([points[k] for k in indices]).regions
    cell_regions.append(region)

# Définition des portées de détection des robots
detection_range = 0.2

# Assignation des cellules à chaque robot
assigned_cells = [[] for i in range(len(robot_positions))]
for i in range(n_points):
    for j in range(len(robot_positions)):
        if min([(points[i][0] - robot_positions[j][0])**2 + (points[i][1] - robot_positions[j][1])**2 for j in range(len(robot_positions))]) < detection_range**2:
            assigned_cells[j].append(i)

# Calcul des trajectoires pour chaque robot
trajectories = []
for i in range(len(robot_positions)):
    current_pos = robot_positions[i]
    cells_to_cover = assigned_cells[i]
    trajectory = []
    while cells_to_cover:
        distances = [(points[cells_to_cover[j]][0] - current_pos[0])**2 + (points[cells_to_cover[j]][1] - current_pos[1])**2 for j in range(len(cells_to_cover))]
        index = distances.index(min(distances))
        trajectory.append(cells_to_cover[index])
        current_pos = points[cells_to_cover[index]]
        cells_to_cover.pop(index)
    trajectories.append(trajectory)

# Simulation du mouvement des robots pour couvrir les cellules
time_step = 0.1
n_iterations = 1000
for i in range(n_iterations):
    for j in range(len(robot_positions)):
        if trajectories[j]:
            next_point = trajectories[j][0]
            direction = (points[next_point][0] - robot_positions[j][0], points[next_point][1] - robot_positions[j][1])
            if direction[0]**2 + direction[1]**2 < 0.01:
                trajectories[j].pop(0)
            else:
                robot_positions[j] = (robot_positions[j][0] + direction[0] * time_step, robot_positions[j][1] + direction[1] * time_step)