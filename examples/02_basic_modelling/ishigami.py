import numpy as np

def model(X):
    X = np.array(X,ndmin=2)
    a = 7
    b = 0.1
    T1 = np.sin(X[:,0])
    T2 = a* np.power(np.sin(X[:,1]),2)
    T3 = b*np.power(X[:,2],4)*np.sin(X[:,0])
    return  T1 + T2 + T3