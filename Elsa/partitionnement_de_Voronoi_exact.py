import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import imageio

def lloyd_algorithm(data, k, num_iterations=60):

    """
    # Define Gaussian density function
    cov = np.cov(data.T)
    poids_centrale = [1, 0.5]
    mvn = multivariate_normal(poids_centrale, cov=cov)

    # Evaluate the density function at each point on the grid
    rv = multivariate_normal(mean=poids_centrale, cov=cov)
    z = rv.pdf(pos)

    """   

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=0, high=0.5, size=k)
    centroids[:, 1] = np.random.uniform(low=-0.5, high=0, size=k)
    robot_positions = centroids.copy()


    # Initialize plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(data[:, 0], data[:, 1])

    frames = []

    # Run the algorithm for the specified number of iterations
    for i in range(num_iterations):
        # Assign data points to the nearest centroid
        distances = np.linalg.norm(data[:, np.newaxis, :] - robot_positions, axis=2)
        labels = np.argmin(distances, axis=1)

        # Update centroids to the mean of assigned data points
        # for j in range(k):
        #     centroids[j] = np.mean(data[labels == j], axis=0)
        for j in range(k):
           points = data[labels == j]
           centroids[j] = np.average(points, axis=0)

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
        scatter.set_color([plt.cm.tab10(i) for i in labels])
        ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
        ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='.', color='black')
        #ax.contour(x, y)
        plt.pause(0.01)

        create_frame(i)
        image = imageio.v2.imread(f'./img/img_{i}.png')
        frames.append(image)
    
    imageio.mimsave('./img/example.gif', # output gif
                frames,          # array of input frames
                duration = 200)         # optional: frames per second
    
    # Return the final centroids and labels
    return centroids, labels

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
detection_range = 0.5

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=5)