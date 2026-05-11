import numpy as np

def model(X):
    X = np.array(X,ndmin=2)
    return  X[:,0] - X[:,1]