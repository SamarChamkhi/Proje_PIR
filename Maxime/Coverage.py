import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt


A = np.array([[1, 1], [1, 1]]) # 2 objets, relation 1-1
A = np.array([[1, 1], [1, 2]]) # 2 objets, relation réciproque plus forte dans un sens
#A = np.array([1,1,0,1,1,1,0,1,1]) ; A=A.reshape(3,3) # 3 objets
A = np.array([1,1,0,1,1,1,1,0,0,1,1,1,1,0,1,1]) ; A=A.reshape(4,4) # 4 objets

print(A)


G = nx.from_numpy_array(A)

nx.draw(G)

plt.show()