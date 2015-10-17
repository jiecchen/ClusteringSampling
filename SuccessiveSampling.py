import numpy as np


def dist(x, y):
    return abs(x - y)

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
    arr = np.concatenate([np.random.normal(c, 2, rpt) for c in ct])
    return arr

def successive_sampling(U, alpha, beta):
    """
    U -- set of points
    alpha -- integer, to control number of samples
    beta -- real in (0, 1)
    Return: outliers and a configuration
    """
    config = {}
    while len(U) > alpha:
        print "tot =", len(U) + len(config)
        # sample 
        S = np.random.choice(U, alpha)
        # assign each x in U to its nearest point in S
        dists = {}
        assigned = {}
        for x in U:
            assigned[x] = find_nearest(x, S)
            dists[x] = dist(x, assigned[x])
        # compute minimal v to make Ball(S, v) > beta * |U|
        vs = np.array(dists.values())
        t = int(beta * len(U))
        if t < len(vs):
            v = min(vs[np.argpartition(vs, t)[t:]])
        else:
            v = max(vs)
            print "tot =", len(U) + len(config)
        # add configuration for points in Ball(S, v)
        for x in U:
            if dists[x] < v:
                config[x] = assigned[x]
                
        # remove Ball(S, v) from U
        U = [x for x in U if dists[x] >= v]
        print "tot =", len(U) + len(config)
    return U, config

if __name__ == '__main__':
    U = get_data(100, 5) # return a list
    U = [x for x in U]
    U.extend([-1000, 10000, 5000])
    outliers, config = successive_sampling(U, 3, 0.5)
    print outliers
    print len(config)
    print config
