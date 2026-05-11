import numpy as np

def model(X):
    X = np.array(X,ndmin=2)
    # Matlab syntax: 20 - (X(:,1)-X(:,2)).^2 - 8*(X(:,1)+X(:,2)-4).^3
    return  20 - (X[:,0] - X[:,1])**2 - 8*(X[:,0] + X[:,1]-4)**3