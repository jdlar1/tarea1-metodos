import os

import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

# Seleccionar lo que se desea hacer
# Calcular el área tarda alrededor de 12 min

VOLUME = True
GRAPH = False


def load_dataset():
    pts = np.loadtxt('mallas/valle_aburra-quads.pts')/1000
    quads = np.loadtxt('mallas/valle_aburra-quads.quad', dtype=np.int64)
    return pts, quads

def output_image(pts):
    X = pts[:, 0]
    Y = pts[:, 1]
    Z = pts[:, 2]

    X.shape = 272, 173
    Y.shape = 272, 173
    Z.shape = 272, 173

    graph = plt.contourf(X, Y, Z, cmap='viridis')
    plt.contour(X, Y, Z, colors="black")
    plt.axis("image")
    plt.colorbar(graph)
    plt.savefig(os.path.join('outputs', 'punto5-contour.png'), dpi=500)

    fig = plt.figure()

    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap="viridis")

    fig.savefig(os.path.join('outputs', 'punto5-surface.png'), dpi=500)


# Definición de las funciones que se explica más claramente en el documento
def translate_to_origin(pts):
    '''
    Translada puntos del elemento de 0.045 x 0.045 para que queden centrados sobre el eje xy
    '''

    points = pts

    _min_x = points[:, 0].min()
    _min_y = points[:, 1].min()

    points[:, 0] = points[:, 0] - _min_x - 0.045
    points[:, 1] = points[:, 1] - _min_y - 0.045

    return points

def interpolate(points):
    '''
    Retorna una interpolación de Lagrange para los 4 puntos del elemento dado
    '''

    x, y = sym.symbols('x y')

    NA = (1/4)*((1/0.045)**2)*(0.045 - x)*(0.045 + y)
    NB = (1/4)*((1/0.045)**2)*(0.045 - x)*(0.045 - y)
    NC = (1/4)*((1/0.045)**2)*(0.045 + x)*(0.045 - y)
    ND = (1/4)*((1/0.045)**2)*(0.045 + x)*(0.045 + y)

    return NA*points[0, 2] + NB*points[1, 2] + NC*points[2, 2] + ND*points[3, 2]

def gaussian_quad(function: sym.core.add.Add):
    '''Cuadratura gaussiana de n = 3 dada una función. Límites entre [-0.045, 0.045]'''

    x, y = sym.symbols('x y')

    _lim = [-0.045, 0.045]
    _p_and_w = [[-np.sqrt(3/5), 5/9],[0, 8/9], [np.sqrt(3/5), 5/9]]

    _coef = (_lim[1] -_lim[0]) / 2

    var = lambda xi: (_coef*xi) + ((_lim[1] + _lim[0]) / 2)
    
    summ = 0


    for _y in _p_and_w:
        res = 0
        
        for _x in _p_and_w:
            
            res += function.subs({x: var(_x[0])})*_x[1]
        
        summ += res.subs({y: var(_y[0])})*_y[1]
        
    return _coef**2*summ

def compute_volume(pts, quads):

    # Se definen los puntos normalizados, restando el z mínimo
    n_points = pts.copy()
    n_points[:, 2] = n_points[:, 2] - n_points[:, 2].min()

    total_vol = 0

    for idx, quad in enumerate(quads):

        elem = n_points[quad]
        t_points = translate_to_origin(elem)
        i_funct = interpolate(t_points)

        vol = gaussian_quad(i_funct)

        print(f'Volumen del elemento {idx}: {vol:.4f} km^3')

        total_vol += vol
    
    print()
    print(f'Volumen total: {total_vol} km^3')

    
def main():
    pts, quads = load_dataset()

    if GRAPH:
        output_image(pts)
    if VOLUME:
        compute_volume(pts, quads)


if __name__ == '__main__':
    main()
