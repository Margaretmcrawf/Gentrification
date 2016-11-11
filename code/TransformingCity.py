import numpy as np
from Cell2D import Cell2D, Cell2DViewer
from matplotlib.colors import LinearSegmentedColormap

# Land Use Enum
LU_UNDEVELOPED = 0
LU_RESIDENTIAL = 1
LU_COMMERCIAL = 2
LU_GRAY = 3 # can't develop, e.g. airport, gray area, etc.
LU_HIGHDENSITY = 4
LU_WATER = 5
LU_GREEN = 6

# TODO(rlouie): Starting at line 90 in netlogo, the proportions coded/commented mismatch. Rectify this
# LU_PROPS = (0.24, 0.31, 0.06, 0.06, 0.0, 0.19, 0.09)
LU_PROPS = (0.0, 0.6, 0.1, 0.1, 0.0, 0.1, 0.1)

class TransformingCity(Cell2D):

    def __init__(self, m, n=None, **kwargs):
        n = m if n is None else n
        self.m = m
        self.n = n

        # initialize cell values
        self.landuse = self.init_landuse(range(7), LU_PROPS, m, n)
        self.amenities = np.zeros((m,n))
        self.pop_count = np.zeros((m,n)) # count of agents on patch - used to classify patches as high density residential
        self.pop_dens = np.zeros((m,n))
        self.occupancy_start = np.zeros((m,n))
        self.percent_full = np.zeros((m,n), np.float)
        self.rent_start = np.ones((m, n))
        self.rent_current = np.ones((m, n))
        self.creative_space = np.zeros((m,n), np.bool)
        self.creative_value = np.zeros((m,n))
        self.creative_dens_p = np.zeros((m,n))
        self.num_satisfied = np.zeros((m,n))
        # TODO(rlouie): add creative population counts to assign creative value (line 63, netlogo model)

    def init_landuse(self, landtypes, props, m, n):
        """
        landtypes: list/tuple, integer values
        props: list/tuple, len(landtypes), float values
        """
        assert abs(sum(props) - 1.0) < 0.001, "Sum of props should add to 1, it now is %f" % sum(props)
        return np.random.choice(landtypes, (n, m), p=props).astype(np.int8)

    def get_residential_neighbors(self, loc):
        residential = self.landuse == 1
        print(residential)
        return residential

    def step(self):
        pass


def make_cmap(color_dict, vmax=None, name='mycmap'):
    """Makes a custom color map.

    color_dict: map from numbers to colors
    vmax: high end of the range,
    name: string name for map

    If vmax is None, uses the max value from color_dict

    returns: pyplot color map
    """
    if vmax is None:
        vmax = max(color_dict.keys())

    colors = [(value/vmax, color) for value, color in color_dict.items()]

    cmap = LinearSegmentedColormap.from_list(name, colors)

    return cmap

class LandUseViewer(Cell2DViewer):

    # colors from http://colorbrewer2.org/#type=qualitative&scheme=Accent&n=7
    colors = ['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f','#bf5b17']
    cmap = make_cmap({LU_GREEN:colors[0], # green
                      LU_WATER:colors[4], # blue
                      LU_RESIDENTIAL:colors[2], # light orange
                      LU_HIGHDENSITY:colors[6], # dark orange/brown
                      LU_COMMERCIAL:colors[3], # yellow
                      LU_UNDEVELOPED: colors[1],
                      LU_GRAY: colors[5]})
    options = dict(interpolation='none', alpha=0.8)