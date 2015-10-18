import numpy as np
import sets
import sys

def dist(x, y):
    return np.linalg.norm(x - y)


class Assoc:
    """
    Associate this with other
    """
    def __init__(self, _me, _nearest):
        self.this = _me
        self.other = _nearest
    def getDist(self):
        return dist(self.this, self.other)
    def __str__(self):
        return self.this.__str__() + '-->' + self.other.__str__()

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

def detect_outliers(U, nOutliers, alpha=0.001, beta=0.05, M=20):
    # alpha << beta
    N = len(U)
    while len(U) > beta * N:
        S = np.random.choice(U, alpha * N)
        
        
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
    pre_len_U = 0
    while len(U) > nOutliers / (1. - beta) / 3:
        if len(U) == pre_len_U:
            beta -= 0.1
        pre_len_U = len(U)
        n_iter += 1
        print '>>>>> n_iter =', n_iter
        print '|U| =', len(U)
        print 'beta =', beta
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
        U = [a.this for a in assign if a.getDist() >= v]
        

    # now we want to remove the false positive
    U = [x for x in U if dist(x, find_nearest(x, S)) > max_dist]
        
    return U, config

def read_from_file(fileName, n_skip = 1):
    lineN = 0
    data = []
    outliers = []
    with open(fileName, 'r') as fin:
        for line in fin:
            lineN += 1
            if lineN > n_skip:
                line = line.split(',')
                data.append(float(line[1]))
                if int(line[2]) == 1:
                    outliers.append(float(line[1]))

    return data, outliers

if __name__ == '__main__':
    U, outliers = read_from_file(sys.argv[1])
    # U = get_data(10000, 20) # return a list
    nOutliers = len(outliers)
    print 'median =', np.median(U)
    
    # U.extend([5000 * i for i in xrange(1, nOutliers + 1)])

    outliers_est, config = successive_sampling(U, nOutliers, 5, 0.9)
    outliers = sets.Set(outliers)
    outliers_est = sets.Set(outliers_est)
    print 'Ext:', sorted(outliers)
    print 'Est:', sorted(outliers_est)    
    print 'diff:', outliers.difference(outliers_est)
    
    print 'Centers:', np.unique(np.array([a.other for a in config]))
