import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.spatial.distance import cdist
import datetime 

# controle variables
num_iteration_intruder = 10
move_intruder = 1
alpha = 1

def lloyd_algorithm(data, k, num_iterations=60):
    
    # Define Gaussian density function
    cov = np.cov(data.T)
    xp = np.random.uniform(low=-1.2, high=0.7)  
    yp = np.random.uniform(low=-0.9, high=1.9)
    poids_centrale =  np.zeros(data.shape[1])
    print(' poids ',poids_centrale)
    poids_centrale[0] = xp
    poids_centrale[1] = yp
    mvn = multivariate_normal(poids_centrale, cov=cov)

    # Evaluate the density function at each point on the grid
    rv = multivariate_normal(mean=poids_centrale, cov=cov)
    z = rv.pdf(pos)
    

    # Initialize centroids randomly
    centroids = np.zeros((k, data.shape[1]))
    centroids[:, 0] = np.random.uniform(low=-1.8, high=-1.3, size=k)
    centroids[:, 1] = np.random.uniform(low=-2, high=-1.6, size=k)
    robot_positions = centroids.copy()


    # Initialize plot
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect('equal',adjustable='box')
    scatter = ax.scatter(data[:, 0], data[:, 1])

    #This global for is to determine the number of times our intruder will move 
    #after each new position of the intruder our robots recalculate their positions
    for m in range(move_intruder) :
        i,j = 0, 0 
        print('test  ',m, 'time ',datetime.datetime.now())
        
        # Run the algorithm for the specified number of iterations
        for i in range(num_iterations):
          
            # Assign data points to the nearest centroid
            distances = np.linalg.norm(data[:, np.newaxis, :] - robot_positions, axis=2)
            labels = np.argmin(distances, axis=1)

            # Update centroids 
            for j in range(k):
                points = data[labels == j]
                weights = mvn.pdf(points - centroids[j])
                centroids[j] = np.average(points, axis=0, weights=weights*alpha)

            # Move robots towards centroïds
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
            ax.scatter(poids_centrale[0], poids_centrale[1], marker='*', color='blue')
            ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
            ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='o', color='black')
            #ax.contour(x, y, z)
            

        # update intruder position and the density function 
        nxp = np.random.uniform(low=-1.2, high=0.7)
        nyp = np.random.uniform(low=-0.9, high=1.9)
        npoids_centrale = np.zeros(data.shape[1])
        npoids_centrale[0] = nxp
        npoids_centrale[1] = nyp
        direction_in = np.zeros((1, data.shape[1]))
        mvn = multivariate_normal(npoids_centrale, cov=cov)
        # move the intruder to it's new position 
        for j in range( num_iteration_intruder) : 
            direction_in= npoids_centrale- poids_centrale
            distances = np.linalg.norm( poids_centrale- npoids_centrale, axis=0)

            if distances == 0:
                step_size = 1
            else:
                step_size = 0.1

            if distances < step_size: 
                poids_centrale = npoids_centrale
            else:
                new_position = poids_centrale + (step_size * direction_in/ distances) 
                poids_centrale = new_position
            # update intruder position on the graph
            ax.scatter(poids_centrale[0], poids_centrale[1], marker='*', color='blue')
        rv = multivariate_normal(mean=poids_centrale, cov=cov)
        z = rv.pdf(pos)
        plt.pause(0.02)
        
    # Return the final centroids and labels
    return centroids, labels

# Generate grid data 
n = 150
x = np.linspace(-5,5,n)
y = np.linspace(-5,5,n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]
pos = np.dstack((xx, yy))

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=5)
