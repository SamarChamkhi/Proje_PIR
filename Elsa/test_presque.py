import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
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

    # Compute Voronoi diagram and finite Voronoi polygons
    vor = Voronoi(centroids)
    regions, vertices = voronoi_finite_polygons_2d(vor)

    # Plot Voronoi diagram with centroids and robots
    fig, ax = plt.subplots()
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='gray', line_width=0.5)
    ax.scatter(data[:, 0], data[:, 1])
    ax.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='red')
    ax.scatter(robot_positions[:, 0], robot_positions[:, 1], marker='.', color='black')
    ax.set_xlim([0, 0.5])
    ax.set_ylim([-0.5, 0])
    plt.show()

    # Create image with Voronoi cells
    voronoi_image = np.zeros((n, n))
    for i, polygon in enumerate(regions):
        polygon_indices = np.array([np.where((data == point).all(axis=1))[0][0] for point in vertices[polygon]])
        polygon_coords = data[polygon_indices]
        polygon_coords_int = np.int32(polygon_coords*n)
        cv2.fillConvexPoly(voronoi_image, polygon_coords_int, i+1)
    voronoi_image = np.uint8(255*(voronoi_image>0))

    return centroids, labels, voronoi_image

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite
    regions.
    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # Finite region
            new_regions.append(vertices)
            continue

        # Reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # Finite ridge: already in the region
                continue

            # Compute the direction of the ridge
            t = vor.points[p2] - vor.points[p1]
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])

            # Find the midpoint of the ridge
            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # Sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


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
detection_range = 1

# Run the Lloyd algorithm with k=10 clusters
centroids, labels = lloyd_algorithm(data, k=5)