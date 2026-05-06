import numpy as np


def model(X):
    """calculates the deflection of a Simply Supported Beam on 9 equally-spaced 
    points along the beam length. X refers to a sample of the input random variables: [b h L E p]. 
    The points for which the deflection is calculated are xi = (1:9)/10*L.
    The vector Y contains the displacement at each of the 9 points.

    Parameters
    ----------
    X: ndarray
        5-column matrix\\
        x[:,0]: beam width (m)\\
        x[:,1]: beam height (m)\\
        x[:,2]: length (m)\\
        x[:,3]: Young modulus (Pa)\\
        x[:,4]: uniform load (N)
        
    
    Returns
    -------
    ndarray
        Y[:,0]: deflection at xi=1/10*L\\
        ...\\
        Y[:,8]: deflection at xi=9/10*L
    """
    X = np.array(X,ndmin=2)
    b = X[:, 0]; # beam width  (m)
    h = X[:, 1]; # beam height (m)
    L = X[:, 2]; # Length (m)
    E = X[:, 3]; # Young modulus (Pa)
    p = X[:, 4]; # uniform load (N)
    
    # The beam is considered primatic, therefore:
    I = b* np.power(h,3) / 12; # the moment of intertia
    Y = np.empty((X.shape[0],9))
    for j in np.arange(0,9):
        xi = (j+1)/10*L
        Y[:,j] = -p*xi*(np.power(L,3)-2*np.power(xi,2)*L + xi**3)/(24*E*I);
    
    return Y
