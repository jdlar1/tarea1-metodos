import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator


import numpy as np
import matplotlib

# Seleccionar lo que se desea hacer, graficar demora unos 5 minutos
AREA = False
GRAPH = True


def load_dataset():
    pts = np.loadtxt('mallas/valle_aburra-quads.pts')/1000
    quads = np.loadtxt('mallas/valle_aburra-quads.quad', dtype=np.int64)
    return pts, quads


def output_image(pts, quads):

    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)


def compute_area(pts, quads):

    z_min = np.amin(pts[:, 2])  # Valor mínimo de z para calcular el area

    n_pts = pts - z_min         # Normalizar los puntos respecto al valor mínimo

    area = 0

    for verts in quads:  # Asumiendo que todos los elementos son paralelogramos

        '''
        print(verts)
        print(pts[verts])
        '''

        _w = np.abs(pts[verts[0], 0] - pts[verts[2], 0])
        _l = np.abs(pts[verts[0], 1] - pts[verts[1], 1])
        _h = (n_pts[verts][:, 2]).mean()

        area += _w * _h*_l

    print(f'Volumen: {area:.4f} km^3')


def main():
    pts, quads = load_dataset()

    if GRAPH:
        output_image(pts, quads)
    elif AREA:
        compute_area(pts, quads)
    else:
        print('No options selected')


if __name__ == '__main__':
    main()
