import numpy as np
import sets


def dist(x, y):
    return np.linalg.norm(x - y)


class Assoc:
    """
    Associate a vector with its nearest neighbor
    """
    def __init__(self, _me, _nearest):
        self.vector = _me
        self.nearest = _nearest
    def getDist(self):
        return dist(self.vector, self.nearest)
    def __str__(self):
        return self.vector.__str__() + '-->' + self.nearest.__str__()

def find_nearest(x, S):
    m_dist = 1e10
    best = 0
    for y in S:
        if dist(x, y) < m_dist:
            m_dist = dist(x, y)
            best = y
    return best

def get_data(n=1000, k=20):
    ct = [i * 100 for i in xrange(k)]
    rpt = n / k;
    arr = np.concatenate([np.random.normal(c, 5, rpt) for c in ct])
    arr = [int(x) for x in arr]
    return arr

def successive_sampling(U, nOutliers, alpha, beta):
    """
    U -- set of points
    alpha -- integer, to control number of samples in each iteration
    beta -- real in (0, 1)
    Return: outliers and a configuration
    """
    config = []
    # nOutliers should be larger than alpha
    n_iter = 0
    centers = []
    max_dist = 0.
    while len(U) > 5 * nOutliers / (1. - beta):
        n_iter += 1
        print '>>>>> n_iter =', n_iter
        print '|U| =', len(U)
        # sample 
        S = np.random.choice(U, alpha)
        # add as centers
        centers.extend([x for x in S])
        # assign each x in U to its nearest point in S
        assign = [Assoc(x, find_nearest(x, S)) for x in U]

        # compute minimal v to make Ball(S, v) > beta * |U|
        vs = np.array([a.getDist() for a in assign])
        t = int(beta * len(U))
        vs = sorted(vs)
        v = vs[t]
        if v > max_dist:
            max_dist = v
        # add configuration for points in Ball(S, v)
        for a in assign:
            if a.getDist() < v:
                config.append(a)
                
        # remove Ball(S, v) from U
        U = [a.vector for a in assign if a.getDist() >= v]

    # now we want to remove the false positive
    U = [x for x in U if dist(x, find_nearest(x, S)) > max_dist]
        
    return U, config

if __name__ == '__main__':
    U = get_data(10000, 20) # return a list
    U = [x for x in U]
    nOutliers = 3
    U.extend([5000 * i for i in xrange(1, nOutliers + 1)])
    outliers, config = successive_sampling(U, nOutliers, 5, 0.8)
    print outliers
    print np.unique(np.array([a.nearest for a in config]))
