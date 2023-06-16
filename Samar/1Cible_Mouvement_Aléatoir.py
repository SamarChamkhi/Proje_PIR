import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import datetime

nb_robots = 7
num_iteration_intruder = 3  # pour implémenter le petit mouvement de  cible
move_intruder = 40 # Nombre d'itératons pour bouger les cibles
alpha = 50

def lloyd_algorithm(data, k, num_iterations=6):

    # Define Gaussian density function
    cov = [[0.5, 0], [0, 0.5]]
    xp = np.random.uniform(low=-0.7, high=0.5)
    yp = np.random.uniform(low=-0.7, high=0.7)
    poids_centrale = np.zeros(data.shape[1])
    poids_centrale[0] = xp
    poids_centrale[1] = yp
    print(' poids ', poids_centrale)
    mvn = multivariate_normal(poids_centrale, cov=cov)
    cdm = np.zeros((k, data.shape[1]))
    cdm[:, 0] = xp
    cdm[:, 1] = yp

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
                weights = mvn.pdf(points - cdm[j])
                w = weights*alpha
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
                poids_centrale[0], poids_centrale[1], marker='*', color='blue')
            
            ax.scatter(centroids[:, 0], centroids[:, 1],
                       marker='x', color='red', s=5)
            ax.scatter(
                robot_positions[:, 0], robot_positions[:, 1], marker='o', color='black', s=5)
            # ax.contour(x, y, z)
            plt.pause(0.01)
        if m < move_intruder - 1:
            # update intruder position
            cdm[:, 0], cdm[:, 1], poids_centrale = new_position_i_random(
                poids_centrale, num_iteration_intruder, ax)
            mvn = multivariate_normal(poids_centrale, cov=cov)
            rv = multivariate_normal(mean=poids_centrale, cov=cov)
        else:
            continue
    # Return the final centroids and labels
    plt.show()
    return centroids, labels

def new_position_i_random(point, nii, axe):
    # point = last position of the intruder
    # nii = number intruder iteration
    # axe = axe du plot
    nxp = np.random.uniform(low=-1, high=1)
    nyp = np.random.uniform(low=-1, high=1)
    npoids_centrale = np.zeros(data.shape[1])
    npoids_centrale[0] = nxp
    npoids_centrale[1] = nyp
    direction_in = np.zeros((1, data.shape[1]))
    for j in range(nii):
        direction_in = npoids_centrale - point
        distances = np.linalg.norm(point - npoids_centrale, axis=0)
        if distances == 0:
            step_size = 0.1
        else:
            step_size = 0.01

        if distances < step_size:  # if distance is less than step size, move the robot to the centroid
            point = npoids_centrale
        else:
            # update robot position by step size towards the centroid
            new_position = point + (step_size * direction_in / distances)
            point = new_position
        axe.scatter(point[0], point[1], marker='*', color='blue')
    # return new position x and y of intruder, new position of the intruder
    return nxp, nyp, point

# Generate grid data
n = 80
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=nb_robots)
