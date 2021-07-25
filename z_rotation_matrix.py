import numpy as np

def z_rotation_matrix(theta):
    #rotation by the angle theta (in radians) about the z-axis
    #returns matrix of shape (3,3)
    rotation_matrix = np.array([[np.cos(theta), np.sin(theta), 0],
    [-np.sin(theta), np.cos(theta), 0], 
    [0, 0, 1]])
    return rotation_matrix
