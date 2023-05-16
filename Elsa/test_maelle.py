from turtle import distance
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import imageio


def lloyd_algorithm(data, k, num_iterations=60):

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=15, high=15.5, size=k)
    centroids[:, 1] = np.random.uniform(low=14.5, high=15, size=k)
    robot_positions = centroids.copy()

    # Initialize labels array
    labels = np.zeros(data.shape[0], dtype=int)

    # Initialize plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(data[:, 0], data[:, 1])

    frames = []
    costs = np.zeros(num_iterations)

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
            if len(points) > 0:
                centroids[j] = np.mean(points, axis=0)

        cost1 = 0
        cost2 = 0
        for j in range(k):
            points = data[labels == j]
            #weights_cost = mvn.pdf(points - robot_positions[j])
            cost_func1 = np.linalg.norm(points - robot_positions[j], axis=1)
            cost_func2 = 1
            cost1 += np.sum((cost_func1)**2)
            cost2 += np.sum(cost_func2)
        costs[i] = -cost1 -detection_range**2*cost2
        print (round(costs[i]))


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
        scatter.set_color([plt.cm.tab20(labels[i]) for i in range(0,len(labels))])
        ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red', edgecolors='none', plotnonfinite= True)
        ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='.', color='black')
        plt.xlim(0,30)
        plt.ylim(0,30)
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
x = np.linspace(0,30,n)
y = np.linspace(0,30,n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))
detection_range = 6

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=9)