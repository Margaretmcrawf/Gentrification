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

    def __init__(self, m, n=None, p_subsidized=0.0, avg_rent=12000, start_pop=1000, sub_housing_rate = 0.50 **kwargs):
        n = m if n is None else n
        self.m = m
        self.n = n
        self.p_subsidized = p_subsidized #percentage of agents who can get subsidized housing
        self.start_pop = start_pop
        self.allow_development = True
        self.sub_housing_rate = sub_housing_rate

        # initialize cell values
        self.setup_landuse(range(7), LU_PROPS, m, n)
        self.amenities = np.zeros((m,n))
        self.pop_count = np.zeros((m,n)) # count of agents on patch - used to classify patches as high density residential
        self.pop_dens = np.zeros((m,n))
        self.occupancy_start = None
        self.percent_full = np.zeros((m,n), np.float)
        self.rent_start = np.ones((m, n))
        self.rent_current = np.random.normal(avg_rent, avg_rent/4, (m,n))
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
        self.displaced = set()
        self.displaced_history = []
        self.p_creative_space_history = []
        self.num_displaced_this_step_history = []

        self.initialize_agents(start_pop)
        self.setup_creative_space()

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
        for patch, occupant_idxs in self.occupants.items():
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
        residential = self.landuse == LU_RESIDENTIAL # logical array
        residential_locs = np.transpose(np.nonzero(residential))
        return residential_locs

    def step(self):

        num_displaced_this_step = 0
        for i, agent in enumerate(self.agents):
            old_loc = agent.loc
            new_loc = agent.step(self, self.rent_current[old_loc])
            if new_loc:
                self.occupants[new_loc].add(i)
                self.occupants[old_loc].discard(i)
                if i not in self.displaced:
                    self.displaced.add(i)
                num_displaced_this_step += 1
        self.displaced_history.append(len(self.displaced))
        self.num_displaced_this_step_history.append(num_displaced_this_step)

        #update the populations.
        for patch, occupant_idxs in self.occupants.items():
            self.pop_count[patch] = len(occupant_idxs)
            self.pop_count_cr_h[patch] = np.sum([self.agents[idx].creativity == 10 for idx in occupant_idxs])
            self.pop_count_cr_m[patch] = np.sum([self.agents[idx].creativity == 5 for idx in occupant_idxs])
            self.pop_count_cr[patch] = self.pop_count_cr_h[patch] + self.pop_count_cr_m[patch]

            if self.pop_count_cr[patch] >= self.creative_dens_p:
                self.creative_space[patch] = 1
            else:
                self.creative_space[patch] = 0

            self.creative_value[patch] = self.pop_count_cr_h[patch] * 10 + self.pop_count_cr_m[patch] * 5

            if self.creative_value[patch] >= 500:
                self.rent_current[patch] *= 2
            elif self.creative_value[patch] >= 300:
                self.rent_current[patch] *= 1.5
            elif self.creative_value[patch] >= 100:
                self.rent_current[patch] *= 1.1
            elif self.creative_value[patch] >= 50:
                self.rent_current[patch] *= 1.05

        self.p_creative_space_history.append(self.measure_p_creative_space())

    def initialize_agents(self, n_agents_to_start):
        self.agents = []
        self.incomes = []
        self.occupants = defaultdict(set)

        self.add_agents(n_agents_to_start)

    def add_agents(self, n_agents_to_add):
        """
        n_agents_to_add: number of agents to add
        """
        # determine which locations are fair game to move to (residential)

        residential = self.landuse == LU_RESIDENTIAL # logical array
        residential_locs = np.transpose(np.nonzero(residential))

        current_n_agents = len(self.agents)
        for idx in range(current_n_agents, current_n_agents + n_agents_to_add):
            ind = np.random.randint(len(residential_locs))
            loc = tuple(residential_locs[ind])

            self.agents.append(agent.Agent(loc, sub_housing_rate=self.sub_housing_rate))
            self.occupants[loc].add(idx)
            self.incomes.append(self.agents[idx].income)

        threshold = self.get_subsidization_threshold()
        #update the is_subsidized bool for the agents who qualify.
        for idx in range(current_n_agents, current_n_agents + n_agents_to_add):
            if self.agents[idx].income <= threshold:
                self.agents[idx].is_subsidized = True

    def get_subsidization_threshold(self):
        incomes = sorted(self.incomes)
        return incomes[int(self.p_subsidized*len(self.incomes))]

    def measure_p_creative_space(self):
        """Returns percentage of residential cells that are creative spaces"""
        residential = self.landuse == LU_RESIDENTIAL # logical array
        return float(np.sum(self.creative_space)) / np.sum(residential)

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


class PopulationViewer(Cell2DViewer):
    colors = ['#fdc086', '#cd6302', '#d3d3d3']
    cmap = make_cmap({1: colors[0],
                      5: colors[1],
                      0: colors[2]})
    options = dict(interpolation='none', alpha=0.8)


if __name__ == '__main__':
    t = TransformingCity(10)
    t.step()


