import matplotlib.pyplot as plt 
import numpy as np 

def set_positions(self):
       """Uses polar coordinates to systematically set positions for arbitrary number of particles"""
       R = genpolar.make_list(self.num_balls)[0]
       T = genpolar.make_list(self.num_balls)[1]
       coords_x = []
       coords_y = []
       
       for r, t in genpolar.rtpairs(R, T):
            tempx = (r * np.cos(t))
            tempy = (r * np.sin(t))
            coords_x.append(tempx)
            coords_y.append(tempy)

       for i in range(len(self.list_of_balls)):
           self.list_of_balls[i].position[0] = coords_x[i]
           self.list_of_balls[i].position[1] = coords_y[i]

def make_list(num):
    R = np.array([0,1,2,3,4,5,6,7,8,9])
    T = np.zeros(shape=(1,10))
    
    T[0,0] = 1
    for i in range(1,9):
        T[0,i] = num/10
    T[0,9]= int(num - (1 + (8 * int(num/10))))

    new_T = []
    for item in T[0]:
        new_T.append(int(item))
    
    return (list(R),list(new_T))
    
def rtpairs(R,N):
    """ 
    yield uniformly distributed points on a circle for a given list of radii
    Args:    
        R: list of radii 
        N: list contain number of points to draw for each corresponding radius value in R  
    """

    for i in range(len(R)): 
        for j in range(0,N[i]):
            yield R[i],(2*np.pi/N[i])*j
        
def rtuniform(n,rmax,m):
    """
    Args:
        n: number of inner circles
        rmax: maximum radius to be drawn 
        m: number of points to draw for each circle
    """
    
    theta =[m*i for i in range(n)]
    theta[0]=1
    return rtpairs(list(np.linspace(0,rmax,n)),theta)      

P = make_list(45)[0]
Q = make_list(45)[1]

for r, t in rtpairs(P, Q):
    plt.plot(r * np.cos(t), r * np.sin(t), 'bo')

plt.show()
