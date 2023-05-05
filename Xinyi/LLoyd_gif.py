import numpy as np
import matplotlib.pyplot as plt
import imageio

def lloyd_algorithm(data, k, num_iterations=25):
    # Initialize centroids randomly
    centroids = np.random.uniform(low=np.min(data), high=np.max(data), size=(k, data.shape[1]))

    # Initialize plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(data[:, 0], data[:, 1])

    frames = []

    # Run the algorithm for the specified number of iterations
    for i in range(num_iterations):
        # Assign data points to the nearest centroid
        distances = np.linalg.norm(data[:, np.newaxis, :] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Update centroids to the mean of assigned data points
        for j in range(k):
            centroids[j] = np.mean(data[labels == j], axis=0)

        # Update plot
        scatter.set_offsets(data)
        scatter.set_color([plt.cm.tab10(i) for i in labels])
        ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
        plt.pause(0.01)
        create_frame(i)
        image = imageio.v2.imread(f'./img_{i}.png')
        frames.append(image)
    
    imageio.mimsave('./example.gif', # output gif
                frames,          # array of input frames
                duration = 200)         # optional: frames per second
    
    # Return the final centroids and labels
    return centroids, labels


def create_frame(t):
    plt.savefig(f'./img/img_{t}.png', 
                transparent = False,  
                facecolor = 'white'
               )


# # Generate some random data
# data = np.random.normal(size=(1000, 2))

# Generate a grid of points
n = 40
x = np.linspace(-1, 1, n)
y = np.linspace(-1, 1, n)
xx, yy = np.meshgrid(x, y)
data = np.c_[xx.ravel(), yy.ravel()]

# Run the Lloyd algorithm with k=5 clusters
centroids, labels = lloyd_algorithm(data, k=10)
