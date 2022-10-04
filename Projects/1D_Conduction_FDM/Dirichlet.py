#%%
from scipy.integrate import quad
import numpy as np
import  matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# Setting BC's
T_0 = 100
T_F = 10
# setting conductivity to a random (physically realisable) value
k = .3
# Length of the rod
length=10
# Number of Nodes
N = 4
def n_j(x):
    return x/length
def n_i(x):
    return 1-x/length
def dni_dx(x):
    return (-1/length)
def dnj_dx(x):
    return 1/length
def dni_dx2(x):
    return dni_dx(x)*dni_dx(x)
# Convenvtion term
def P(x):
    return 0*x
def dnj_dx2(x):
    return dni_dx(x)*dni_dx(x)
def Q(x):
    return 0*x
def pn_i2(x):
    return P(x)*n_i(x)*n_i(x)
def pn_j2(x):
    return P(x)*n_j(x)*n_j(x)
def dn_idn_j_dx(x):
    return dni_dx(x)*dnj_dx(x)
def pn_in_j(x):
    return P(x)*n_i(x)*n_j(x)
def dirichlet(n, bc1, bc2, l):
    """

    :param n: Number of Nodes
    :param bc1: Boundary condition at x = 0
    :param bc2: Boundary Condition at x = L
    :param l: Length of cross-section
    :return: A matrix as np array, u as np array and x as np arraay
    """
    import numpy as np
    x = np.linspace(0.0, l, n)

    A = np.zeros([n,n])
    b = np.zeros(n-2)
    start = 0
    step = l/n
    for i in range(0, n):
        end = start + step

        if i == 0:
            # Diagonal
            A[i, i] = k*quad(dni_dx2, start, end)[0] - quad(pn_i2, start, end)[0]
            # Upper Diagonal
            A[i, i+1] = k*quad(dn_idn_j_dx, start, end)[0] - quad(pn_in_j, start, end)[0]
            # b[i] = 0
        elif i < n-1:
            # Lower Diagonal
            A[i, i-1] = k*quad(dn_idn_j_dx, start, end)[0] - quad(pn_in_j, start, end)[0]
            # Diagonal (Int{xi}^xJ + Int{xj}^xk)
            A[i, i] = (k*quad(dnj_dx2, start, end)[0] - quad(pn_j2, start, end)[0]) + (k*quad(dnj_dx2, end, end+step)[0] - quad(pn_j2, start, end+step)[0])
            # Upper Diagonal
            A[i ,i +1] = k*quad(dn_idn_j_dx, end, end+step)[0] - quad(pn_in_j, end, end+step)[0]
        else:
            A[i, i] =  k*quad(dnj_dx2, end, end+step)[0] - quad(pn_j2, start, end)[0]
            A[i, i-1] =  k*quad(dn_idn_j_dx, end, end+step)[0] - quad(pn_in_j, start, end)[0]
            # b[i] = 0
        start+=step
    A = [list(A[i][1:-1]) for i in range(np.shape(A)[0]-2)]
    u = np.linalg.solve(A, b)
    return A, u, x
_, u, x = dirichlet(1000, T_0, T_F, length)

plt.plot(x[2:], u)
plt.show()