import numpy as np
z=2
x=[7.8+7.2*z**(-1), 6.8+5.7*z**(-1)];
H_z=np.array([[ 3.1+2.1*z**(-1), 2.7+9.3*z**(-1)],[5.2+9.6*z**(-1), 9.9+6.6*z**(-1)]])
#print(H_z)
d= np.dot(x,H_z)
print(d)