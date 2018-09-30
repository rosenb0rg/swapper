import numpy as np

# import scipy.io as 
def align(vertices, can_vert):
#    canonical_vertices = np.load('Data/uv-data/canonical_vertices.npy')
    canonical_vertices = np.load(can_vert)

    vertices_homo = np.hstack((vertices, np.ones([vertices.shape[0],1]))) #n x 4
    P = np.linalg.lstsq(vertices_homo, canonical_vertices)[0].T # Affine matrix. 3 x 4
    front_vertices = vertices_homo.dot(P.T)

    return front_vertices
