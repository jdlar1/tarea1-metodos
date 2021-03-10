import os

import numpy as np
import meshio

malla = meshio.read(os.path.join('mallas', 'knight.msh'))
pts = malla.points
tets = malla.cells[0].data


V=0

for i in tets:
    C=pts[i,:]
    a=C[0]
    b=C[1]
    c=C[2]
    d=C[3]

    e1=a-d
    e2=b-d
    e3=c-d

    c1=np.cross(e2,e3)
    v=abs(np.dot(e1,c1)/6)

    V += v


print(f"El volumen de la pieza de ajedrez es de {V/1000:.4f} cm^3")






