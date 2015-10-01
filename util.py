import numpy as np

def find(U):
    """
    Returns the indices of the elements that are True in U.

    Parameters
    ----------
    U: A flat 2D array filled with ones and zeros.
    """
    args = np.argwhere(U)
    U = args[:, 1]
    return np.array([U])
