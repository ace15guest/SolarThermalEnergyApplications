#Use these packages to build the diagonal matrix
from scipy.sparse import diags
from scipy.integrate import quad
import numpy as np
# Setting BC's
T_0 = 100
T_F = 10
l=1
# setting conductivity to a random (physically realisable) value
k = 1
# k = [np.ones(N-1),1*np.ones(N),np.ones(N-1)]
offset = [-1,0,1]

A = diags(k,offset).toarray()
def n_j(x):
    return 1-x/l
def n_i(x):
    return x/l
def dni_dx(x):
    return (-x/l)
def dni_dx2(x):
    return dni_dx(x)*dni_dx(x)
def dnj_dx(x):
    return x/l
def dnj_dx2(x):
    return dni_dx(x)*dni_dx(x)
def P(x):
    return 0
def Q(x):
    return 0

def pn_i2(x):
    return P(x)*n_i(x)*n_i(x)

def dn_idn_j_dx(x):
    return dni_dx(x)*dnj_dx(x)

def pn_in_j(x):
    return P(x)*n_i(x)*n_j(x)



def dirichlet(n, bc1, bc2, l):
    """

    :param n:
    :param bc1:
    :param bc2:
    :param l:
    :return:
    """
    import numpy as np
    x = np.linspace(0.0, l, n)

    A = np.zeros([n,n])
    b = np.zeros(n)
    start = 0


    step = l+n
    for i in range(0, n):
        end = start + step
        int_range = [start, end]
        if (i == 0):
            # Diagonal
            A[i, i] = k*quad(dni_dx2, start, end)[0] - quad(pn_i2, start, end)[0]
            # Upper Diagonal
            A[i, i+1] = k*quad(dn_idn_j_dx, start, end)[0] - quad(pn_in_j, start, end)[0]
            b[i] = bc1
        elif (i < n-1):
            # Lower Diagonal
            A[i, i-1] = k*quad(dn_idn_j_dx, start, end)[0] - quad(pn_in_j, start, end)[0]
            # Diagonal
            A[i, i] = 1
            # Upper Diagonal
            A[i ,i +1] = k*quad(dn_idn_j_dx, start, end)[0] - quad(pn_in_j, start, end)[0]

        else:
            A[i, i] = 1.0
            b[i] =bc2
        start+=step
    u = np.linalg.solve(A, b)
    return A, u
dirichlet(10, 1, 2, 10)