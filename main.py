import random
import matplotlib.pyplot as plt
import datetime as dt

'''
Algorithm BuildRRT
    Input: Initial configuration qinit,
           number of vertices in RRT K,
           incremental distance Δq)
    Output: RRT graph G

    G.init(qinit)
    for k = 1 to K do
        qrand ← RAND_CONF()
        qnear ← NEAREST_VERTEX(qrand, G)
        qnew ← NEW_CONF(qnear, qrand, Δq)
        G.add_vertex(qnew)
        G.add_edge(qnear, qnew)
    return G
'''


class RRTlist:
    def __init__(self, xstart=0, ystart=0, minbound=-50, maxbound=50, dq=1.0):
        self.nodes = [[xstart, ystart]]
        self.edges = []
        self.minbound = minbound
        self.maxbound = maxbound
        self.dq = dq

    def rand_conf(self):
        return [self._generate_random(),
                self._generate_random()]

    def _generate_random(self):
        return random.random() * \
               (self.maxbound - self.minbound) \
               + self.minbound

    def nearest_node(self, pt_rnd):
        _min_dist = 9999999
        _min_index = -1
        for i, p in enumerate(self.nodes):
            _cur_dist = self._find_distance(p, pt_rnd)
            if _cur_dist < _min_dist:
                _min_dist = _cur_dist
                _min_index = i

        return _min_index

    def _find_distance(self, pt_from, pt_to):
        return ((pt_to[0] - pt_from[0])**2 +
                (pt_to[1] - pt_from[1])**2) ** 0.5

    def new_conf(self, pt_near_index, pt_rnd):
        _dx = pt_rnd[0] - self.nodes[pt_near_index][0]
        _dy = pt_rnd[1] - self.nodes[pt_near_index][1]
        _dist = self._find_distance(
            self.nodes[pt_near_index],
            pt_rnd
        )
        scalar = self.dq / _dist if self.dq < _dist else 1.0

        return [
            self.nodes[pt_near_index][0] + _dx * scalar,
            self.nodes[pt_near_index][1] + _dy * scalar,
        ]

    def add_node(self, newNode):
        self.nodes.append(newNode)

    def add_edge(self, nearNodeIndex, newNode):
        self.edges.append([self.nodes[nearNodeIndex], newNode])

    def plot_result(self):
        for i, n in enumerate(self.edges):
            _x = [n[0][0], n[1][0]]
            _y = [n[0][1], n[1][1]]
            plt.plot(_x, _y)
        plt.axis('equal')
        plt.xlim(self.minbound, self.maxbound)
        plt.ylim(self.minbound, self.maxbound)
        plt.show()


if __name__ == '__main__':
    timestart = dt.datetime.now()
    maxiter = 500
    G = RRTlist()

    for iter in range(maxiter):
        qRand = G.rand_conf()
        qNearIndex = G.nearest_node(qRand)
        qNew = G.new_conf(qNearIndex, qRand)
        G.add_node(qNew)
        G.add_edge(qNearIndex, qNew)

    timestop = dt.datetime.now()
    print(f'Total time: {timestop - timestart}')
    G.plot_result()
