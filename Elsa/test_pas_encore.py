import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import imageio

def lloyd_algorithm(data, k, num_iterations=60):

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=0, high=0.5, size=k)
    centroids[:, 1] = np.random.uniform(low=-0.5, high=0, size=k)
    robot_positions = centroids.copy()

    # Initialize labels array
    labels = np.zeros(data.shape[0], dtype=int)

    # Initialize plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(data[:, 0], data[:, 1])

    frames = []

    # Run the algorithm for the specified number of iterations
    for i in range(num_iterations):
        # Assign data points to the nearest centroid
        distances = cdist(data, robot_positions)
        masked_distances = np.where(distances < detection_range, distances, np.inf)
        labels = np.argmin(masked_distances, axis=1)

        # Update centroids to the mean of assigned data points
        for j in range(k):
            mask = labels == j
            points = data[mask]
            cost = Hr(robot_positions, detection_range)
            print("Cost: ", cost)
            print()
            if len(points) > 0:
                centroids[j] = np.mean(points, axis=0)

        # Move robots towards centroids
        for j in range(k):
            # Calculate distances between robot and centroids
            direction = centroids[j] - robot_positions[j]
            distances = np.linalg.norm(robot_positions[j] - centroids[j], axis=0)

            if distances == 0:
                step_size = 1
            else:
                step_size = 0.3

            if distances < step_size: # if distance is less than step size, move the robot to the centroid
                robot_positions[j] = centroids[j]
            else:
                new_position = robot_positions[j] + (step_size * direction/ distances) # update robot position by step size towards the centroid
                robot_positions[j] = new_position

        # Update plot
        scatter.set_offsets(data)
        #ax.set_facecolor('white')
        #fig.patch.set_facecolor('white')
        scatter.set_color(plt.cm.tab20(0))
        scatter.set_color([plt.cm.tab20(labels[i]) for i in range(2,len(labels))])
        ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
        ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='.', color='black')
        plt.pause(0.01)


        create_frame(i)
        image = imageio.v2.imread(f'./img/img_{i}.png')
        frames.append(image)

    imageio.mimsave('./img/example.gif', # output gif
                frames,          # array of input frames
                duration = 200)         # optional: frames per second
    
    

    # Return the final centroids and labels
    return centroids, labels  


"""
        # Update plot
        ax.clear()
        ax.set_facecolor('white')
        for j in range(k):
            mask = labels == j
            points = data[mask]
            ax.fill(*zip(*points), edgecolor='white', facecolor=plt.cm.tab10(j), alpha=1)
            ax.scatter(centroids[j, 0], centroids[j, 1], marker='x', color='red', zorder=10)
            ax.scatter(robot_positions[j, 0], robot_positions[j, 1], marker='.', color='black', zorder=10)
"""

def Hr(robot_positions, r):
       import numpy as np

def Hr_V(P, r):
    """
    Calcule la fonction de couverture Hr V (P) pour un ensemble de points P, un paramètre r et une fonction phi donnée.

    Args:
        P (ndarray): Un ensemble de points, représenté sous la forme d'un tableau numpy à deux dimensions avec N lignes et M colonnes, où N est le nombre de points et M est la dimension de chaque point.
        r (float): Un paramètre qui détermine la distance maximale entre les points pour lesquels la contribution de la fonction phi est non nulle.
        phi (callable): Une fonction qui calcule la contribution de chaque point en fonction de sa distance à un point donné.

    Returns:
        float: La valeur de Hr V (P)
    """
    N = P.shape[0]
    V = np.ones(N)
    for i in range(N):
        for j in range(N):
            if i != j:
                d = np.linalg.norm(P[i] - P[j])
                if d <= r:
                    V[i] += d
    return -np.sum(V * np.log(V))





def create_frame(t):
    plt.savefig(f'./img/img_{t}.png', 
                transparent = False,  
                facecolor = 'white'
               )

# Generate grid data 
n = 100
x = np.linspace(-2,2,n)
y = np.linspace(-2,2,n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))
detection_range = 0.7

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=15)