import pygame
import numpy as np
import random

# définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_RADIUS = 10
CELL_COLOR = (255, 255, 255)
ROBOT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
MAX_STEP_SIZE = 5
MAX_ITERATIONS = 1000

# définition de la classe Robot
class Robot:
    def __init__(self, pos):
        self.pos = pos
        self.color = random.choice(ROBOT_COLORS)
    
    def move(self, target):
        diff = target - self.pos
        if np.linalg.norm(diff) > MAX_STEP_SIZE:
            diff = diff / np.linalg.norm(diff) * MAX_STEP_SIZE
        self.pos += diff

# définition de la classe Cell
class Cell:
    def __init__(self, vertices, bounds):
        self.vertices = vertices
        self.bounds = bounds
        self.centroid = np.mean(vertices, axis=0)
    
    def contains_point(self, point):
        from matplotlib.path import Path
        path = Path(self.vertices)
        return path.contains_point(point)
    
    def get_nearest_point(self, point):
        min_dist = np.inf
        nearest_point = None
        for vertex in self.vertices:
            dist = np.linalg.norm(vertex - point)
            if dist < min_dist:
                min_dist = dist
                nearest_point = vertex
        return nearest_point

# initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Partitionnement de Voronoi pour la couverture de surface")

# définition de la fonction de partitionnement de Voronoi
def get_voronoi_cells(points, bounds):
    from scipy.spatial import Voronoi, voronoi_plot_2d
    vor = Voronoi(points)
    voronoi_plot_2d(vor, ax=None, show_vertices=False, line_colors='orange',
                    line_width=1, line_alpha=0.5, point_size=2)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    cells = [Cell(vertices[region], bounds) for region in regions]
    return cells

# définition de la fonction qui calcule les polygones de Voronoi finis
def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : ndarray
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max
