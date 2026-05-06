import numpy as np

def model(X,P):
    """
    Ishigami function with parameters a and b.

    Parameters
    ----------
    X : 2d-array[ N, M ]
        where N are the number of (realization) samples and M are the model inputsm M = 3 here.
    P : dict
        parameters, 'a' and 'b', of the model.

    Outputs
    ----------
    Y : 2d-array[ N, 1 ]\\
        function value (for each realization sample).
    """
    X = np.array(X,ndmin=2)
    T1 = np.sin(X[:,0])
    T2 = P['a']* np.power(np.sin(X[:,1]),2)
    T3 = P['b']*np.power(X[:,2],4)*np.sin(X[:,0])
    return  T1 + T2 + T3