import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import imageio

def lloyd_algorithm(data, k, num_iterations=200):

    # Define Gaussian density function
    cov = np.cov(data.T)
    poids_centrale = [0.2, -1]
    mvn = multivariate_normal(poids_centrale, cov=cov)

    # Evaluate the density function at each point on the grid
    rv = multivariate_normal(mean=poids_centrale, cov=cov)
    z = rv.pdf(pos)
    

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=-1.5, high=-1, size=k)
    centroids[:, 1] = np.random.uniform(low=-1.5, high=-1, size=k)
    robot_positions = centroids.copy()


    # Initialize plot
    # fig, ax = plt.subplots()
    # scatter = ax.scatter(data[:, 0], data[:, 1])

    frames = []
    costs = np.zeros(num_iterations)

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
            weights = mvn.pdf(points - centroids[j])
            centroids[j] = np.average(points, axis=0, weights=weights)

        cost = 0
        for j in range(k):
            points = data[labels == j]
            weights_cost = mvn.pdf(points - robot_positions[j])
            cost_func = np.linalg.norm(points - robot_positions[j], axis=1)
            cost += np.sum((cost_func)**2 * weights_cost)
        costs[i] = cost


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


        # # Update plot
        # scatter.set_offsets(data)
        # scatter.set_color([plt.cm.tab20(i) for i in labels])
        # ax.scatter(poids_centrale[0], poids_centrale[1], marker='.', color='blue')
        # ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
        # ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='o', color='black')
        # ax.contour(x, y, z)
        # plt.xlim(-2, 2)
        # plt.ylim(-2, 2)
        # ax.set_aspect('equal', adjustable='box')
        # plt.pause(0.01)

        # create_frame(i)
        # image = imageio.v2.imread(f'./img/img_{i}.png')
        # frames.append(image)
    
    fig2 = plt.figure()
    ax = fig2.add_subplot(111)
    ax.plot(range(num_iterations), costs)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Cost')
    plt.show()

    # plt.plot(range(num_iterations), costs)
    # plt.xlabel('Iteration')
    # plt.ylabel('Cost')
    # plt.show()


    # imageio.mimsave('./img/example.gif', # output gif
    #             frames,          # array of input frames
    #             duration = 200)         # optional: frames per second
    
    # Return the final centroids and labels
    return centroids, labels

def create_frame(t):
    plt.savefig(f'./img/img_{t}.png', 
                transparent = False,  
                facecolor = 'white'
               )

# Generate grid data 
n = 500
x = np.linspace(-2,2,n)
y = np.linspace(-2,2,n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=18)
