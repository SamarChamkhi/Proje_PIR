import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import datetime



nb_robots = 7
num_iteration_intruder = 3  # pour implémenter le petit mouvement de  cible
move_intruder = 20
alpha = 50
# Paramètres du mouvement circulaire
rayon = 0.5  # Rayon du cercle
centre = np.array([0.0, 0.0])  # Centre du cercle
vitesse_angulaire = 0.01  # Vitesse angulaire du mouvement
speed = rayon * vitesse_angulaire


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
    # ------------------second intruder-----------------------------------
    poids_centrale2 = np.zeros(data.shape[1])
    poids_centrale2[0] = rayon
    poids_centrale2[1] = 0.0
    mvn2 = multivariate_normal(poids_centrale2, cov=cov)
    cdm2 = np.zeros((k, data.shape[1]))
    cdm2[:, 0] = poids_centrale2[0]
    cdm2[:, 1] = poids_centrale2[1]
    # # --------------------------third intruder-------------------------------------------
    xp3 = np.random.uniform(low=-0.7, high=0.5)
    yp3 = np.random.uniform(low=-0.7, high=0.7)
    poids_centrale3 =  np.zeros(data.shape[1])
    poids_centrale3[0] = xp3
    poids_centrale3[1] = yp3
    print(' poids ',poids_centrale3)
    mvn3 = multivariate_normal(poids_centrale3, cov=cov)
    cdm3 = np.zeros((k, data.shape[1]))
    cdm3[:,0] = xp3
    cdm3[:,1] = yp3
    # # ------------------forth intruder-----------------------------------
    poids_centrale4 =  np.zeros(data.shape[1])
    poids_centrale4[0] = 0.9
    poids_centrale4[1] = 0.0
    mvn4= multivariate_normal(poids_centrale4, cov=cov)
    cdm4 = np.zeros((k, data.shape[1]))
    cdm4[:,0] = poids_centrale4[0]
    cdm4[:,1] = poids_centrale4[1]
    # # ---------------------------------------------------------------------

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=-0.7, high=-0.2, size=k)
    centroids[:, 1] = np.random.uniform(low=-0.4, high=0.4, size=k)
    robot_positions = centroids.copy()

    # Initialize plot
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect('equal', adjustable='box')
    scatter = ax.scatter(data[:, 0], data[:, 1])
    frames = []
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
                weights2 = mvn2.pdf(points - cdm2[j])
                weights3 = mvn3.pdf(points - cdm3[j])
                weights4 = mvn4.pdf(points - cdm4[j])
                w = (weights+weights2+weights3+weights4)*alpha
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
            ax.scatter(
                poids_centrale2[0], poids_centrale2[1], marker='*', color='white')
            ax.scatter(poids_centrale3[0], poids_centrale3[1], marker='*', color='blue')
            ax.scatter(poids_centrale4[0], poids_centrale4[1], marker='*', color='white')
            ax.scatter(centroids[:, 0], centroids[:, 1],
                       marker='x', color='red', s=5)
            ax.scatter(
                robot_positions[:, 0], robot_positions[:, 1], marker='o', color='black', s=5)
            # ax.contour(x, y, z)
            plt.pause(0.01)
            # update intruder position
            cdm[:, 0], cdm[:, 1], poids_centrale = new_position_i_random(
                poids_centrale, num_iteration_intruder, ax)
            mvn = multivariate_normal(poids_centrale, cov=cov)
            rv = multivariate_normal(mean=poids_centrale, cov=cov)
            # update intruder2 position
            pos_func = new_position_i_circle(
                centre, num_iteration_intruder, ax, 0.01, rayon, m)
            poids_centrale2 = pos_func
            cdm2[:, 0] = pos_func[0]
            cdm2[:, 1] = pos_func[1]
            mvn2 = multivariate_normal(pos_func, cov=cov)
            # update intruder3 position
            cdm3[:,0], cdm3[:,1], poids_centrale3= new_position_i_random(poids_centrale3,num_iteration_intruder,ax)
            mvn3 = multivariate_normal(poids_centrale3, cov=cov)
            # update intruder4 position
            pos_func4 = new_position_i_circle(centre,num_iteration_intruder,ax,vitesse_angulaire,0.9,m)
            poids_centrale4 = pos_func4
            cdm4[:,0] = pos_func4[0]
            cdm4[:,1] = pos_func4[1]
            mvn4 = multivariate_normal(pos_func4, cov=cov)
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
