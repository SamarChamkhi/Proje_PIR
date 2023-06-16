import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import datetime
import imageio


nb_robots = 7
num_iteration_intruder = 3  # pour implémenter le petit mouvement de  cible
move_intruder = 210
alpha = 50
# Paramètres du mouvement circulaire
rayon = 0.5  # Rayon du cercle
centre = np.array([0.0, 0.0])  # Centre du cercle
vitesse_angulaire = 0.01  # Vitesse angulaire du mouvement
speed = rayon * vitesse_angulaire


def lloyd_algorithm(data, k, num_iterations=6):

    # Define Gaussian density function
    cov = [[0.5, 0], [0, 0.5]]
    poids_centrale2 = np.zeros(data.shape[1])
    poids_centrale2[0] = rayon
    poids_centrale2[1] = 0.0
    mvn2 = multivariate_normal(poids_centrale2, cov=cov)
    cdm2 = np.zeros((k, data.shape[1]))
    cdm2[:, 0] = poids_centrale2[0]
    cdm2[:, 1] = poids_centrale2[1]

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=-0.7, high=-0.2, size=k)
    centroids[:, 1] = np.random.uniform(low=-0.4, high=0.4, size=k)
    robot_positions = centroids.copy()

    # Initialize plot
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect('equal', adjustable='box')
    scatter = ax.scatter(data[:, 0], data[:, 1])
   
    for m in range(move_intruder):
        i, j = 0, 0
        print('test  ', m, 'time ', datetime.datetime.now())
        # Run the algorithm for the specified number of iterations
        for i in range(num_iterations):
            # Assign data points to the nearest centroid
            distances = np.linalg.norm(
                data[:, np.newaxis, :] - robot_positions, axis=2)
            labels = np.argmin(distances, axis=1)

            # Update centroids to the mean of assigned data points
            for j in range(k):
                points = data[labels == j]
                weights2 = mvn2.pdf(points - cdm2[j])
                w = weights2*alpha
                centroids[j] = np.average(points, axis=0, weights=w)

            # Move robots towards centroids
            for j in range(k):
                # Calculate distances between robot and centroids
                direction = centroids[j] - robot_positions[j]
                distances = np.linalg.norm(
                    robot_positions[j] - centroids[j], axis=0)
                if distances == 0:
                    step_size = 1
                else:
                    step_size = 0.3

                if distances < step_size:  # if distance is less than step size, move the robot to the centroid
                    robot_positions[j] = centroids[j]
                else:
                    # update robot position by step size towards the centroid
                    new_position = robot_positions[j] + \
                        (step_size * direction / distances)
                    robot_positions[j] = new_position

            # Update plot
            scatter.set_offsets(data)
            scatter.set_color([plt.cm.tab10(i) for i in labels])
            ax.scatter(
                poids_centrale2[0], poids_centrale2[1], marker='*', color='blue')
            ax.scatter(centroids[:, 0], centroids[:, 1],
                       marker='x', color='red', s=5)
            ax.scatter(
                robot_positions[:, 0], robot_positions[:, 1], marker='o', color='black', s=5)
            # ax.contour(x, y, z)
            plt.pause(0.01)
            
        if m < move_intruder - 1:
            # update intruder position
            pos_func = new_position_i_circle(
                centre, num_iteration_intruder, ax, vitesse_angulaire, rayon, m)
            poids_centrale2 = pos_func
            cdm2[:, 0] = pos_func[0]
            cdm2[:, 1] = pos_func[1]
            mvn2 = multivariate_normal(pos_func, cov=cov)
        else:
            continue
    # Return the final centroids and labels
    plt.show()
    return centroids, labels

def new_position_i_circle(centre, nii, axe, v_ang, r, p):
    # point = last position of the intruder
    # nii = number intruder iteration
    # axe = axe du plot
    # v_ang = vitesse angulaire
    # r = rayon
    # p = itération
    for j in range(nii):
        angle = (nii*p + j) * v_ang
        new_position = centre + np.array([np.cos(angle), np.sin(angle)]) * r
        if x[0] <= new_position[0] <= x[-1] and y[0] <= new_position[1] <= y[-1]:
            # Mettre à jour la position du point et ajouter les coordonnées à la liste
            position = new_position
            axe.scatter(position[0], position[1], marker='*', color='white')
        else:
            position = position
    # returnnnew position of the intruder
    return position

# Generate grid data
n = 80
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=nb_robots)
