import numpy as np

def x_rotation_matrix(theta):
    #rotation by the angle theta (in radians) about the x-axis
    #returns matrix of shape (3,3)
    rotation_matrix = np.array([[1, 0, 0],
    [0, np.cos(theta), np.sin(theta)], 
    [0, -np.sin(theta), np.cos(theta)]])
    return rotation_matrix

