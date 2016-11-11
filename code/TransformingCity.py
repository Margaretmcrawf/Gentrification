import numpy as np
from Cell2D import Cell2D, Cell2DViewer
from matplotlib.colors import LinearSegmentedColormap
import agent
from collections import defaultdict

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

        self.allow_development = True

        # initialize cell values
        self.setup_landuse(range(7), LU_PROPS, m, n)
        self.amenities = np.zeros((m,n))
        self.pop_count = np.zeros((m,n)) # count of agents on patch - used to classify patches as high density residential
        self.pop_dens = np.zeros((m,n))
        self.occupancy_start = None
        self.percent_full = np.zeros((m,n), np.float)
        self.rent_start = np.ones((m, n))
        self.rent_current = np.ones((m, n))
        self.creative_space = np.zeros((m,n), np.bool)
        self.creative_value = np.zeros((m,n))
        self.creative_dens_p = 3 # threshold that defines how many creative people it takes to define a patch as a creative space
        self.num_satisfied = np.zeros((m,n))
        # creative population counts used to assign creative value and creative space
        self.pop_count_cr = np.zeros((m,n))
        self.pop_count_crt = np.zeros((m,n))
        self.pop_count_cr_h = np.zeros((m,n)) # high creative
        self.pop_count_cr_m = np.zeros((m,n)) # medium creative
        self.pop_count_cr_ht = np.zeros((m,n))
        self.pop_count_cr_mt = np.zeros((m,n))
        self.pop_count_cr_n = np.zeros((m,n)) # TODO(rlouie): what does these pop counts mean in the code
        self.pop_count_cr_diff = np.zeros((m,n)) # diff of count of creative pop to current count of creative pop if negative then gained value, otherwise decrease
        # TODO(rlouie): if this is a factor, should it just be a single number and not a number for each cell?
        self.pop_count_cr_minus = np.zeros((m,n)) # factor to subtract for loss of creative value

        self.make_agents()
        self.setup_creative_space()

    @staticmethod
    def make_locs(n, m):
        """Makes array where each row is an index in an `n` by `m` grid.
        
        n: int number of rows
        m: int number of cols
        
        returns: NumPy array
        """
        left = np.repeat(np.arange(m), n)
        right = np.tile(np.arange(n), m)
        return np.transpose([left, right])


    def setup_landuse(self, landtypes, props, m, n):
        """
        landtypes: list/tuple, integer values
        props: list/tuple, len(landtypes), float values
        """
        assert abs(sum(props) - 1.0) < 0.001, "Sum of props should add to 1, it now is %f" % sum(props)
        self.landuse = np.random.choice(landtypes, (n, m), p=props).astype(np.int8)

    def setup_creative_space(self):
        """create creative space to start based on density of creatives present,
        assigns creative value, bumps up rent on creative-space
        """
        # TODO(rlouie): these pop count functions could be resuable, and dont seem specific to setup only
        for patch, occupant_idxs in self.occupants.iteritems():
            self.pop_count[patch] = len(occupant_idxs)
            self.pop_count_cr_h[patch] = np.sum([self.agents[idx].creativity == 10 for idx in occupant_idxs])
            self.pop_count_cr_m[patch] = np.sum([self.agents[idx].creativity == 5 for idx in occupant_idxs])
            self.pop_count_cr[patch] = self.pop_count_cr_h[patch] + self.pop_count_cr_m[patch]

            if self.pop_count_cr[patch] >= self.creative_dens_p:
                # TODO(rlouie): update this conditional with patches related to outside neighborhoods (nlogo ln 222)
                if self.allow_development:
                    self.creative_space[patch] = 1
                    self.rent_start[patch] *= 2
                    self.creative_value[patch] = self.pop_count_cr_h[patch] * 10 + self.pop_count_cr_m[patch] * 5

        self.occupancy_start = self.pop_count

    def get_residential_neighbors(self, loc):
        residential = self.landuse == 1
        return residential

    def step(self):
        a = agent.Agent((0, 0), education=False)
        a.step(self, 20000)

    def make_agents(self):
        a = []
        occupants = defaultdict(list)
        locs = TransformingCity.make_locs(self.n, self.m)
        residential = self.landuse == LU_RESIDENTIAL # logical array
        # TODO(rlouie): rename locs_where
        residential_locs = np.transpose(np.nonzero(residential))        
        # residential_locs = [loc for loc in locs if self.landuse[loc] == LU_RESIDENTIAL]

        for i in range(400): #change to initializing number of agents...
            ind = np.random.randint(len(residential_locs))
            loc = tuple(residential_locs[ind])
            a.append(agent.Agent(loc))
            occupants[loc].append(i)

        self.agents = a
        self.occupants = occupants


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

if __name__ == '__main__':
    t = TransformingCity(10)
    t.step()
