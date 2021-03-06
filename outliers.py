import numpy as np
import sys
import os





# a vector is represented via a tuple

def dist(x, y):
    return np.linalg.norm(np.array(x) - np.array(y))



def find_nearest(x, S):
    m_dist = 1e10
    best = 0
    for y in S:
        if dist(x, y) < m_dist:
            m_dist = dist(x, y)
            best = y
    return best

def get_data(n=1000, k=20, nOutliers=10):
    ct = [i * 100 for i in xrange(k)]
    rpt = n / k;
    arr = np.concatenate([np.random.normal(c, 1, rpt) for c in ct])
    arr = [(x) for x in arr]
    ot = [i * 10000 for i in xrange(1, nOutliers + 1)]
    arr.extend(ot)
    return arr, ot



def try_append(x, y, lst, M):
    if len(lst) < M:
        lst.append(x)
    else:
        j = np.argmax([dist(y, z) for z in lst])
        if dist(x, y) < dist(y, lst[j]):
            lst[j] = x

def k_th_dist(y, lst, k):
    arr = np.array([dist(y, x) for x in lst])
    return sorted(arr)[k-1]


def find_nearest_k(x, U, k):
    """
    find nearest k neighbors of x from U
    """
    arr = [(dist(x, y), y) for y in U]
    arr = sorted(arr)[:k]
    S = [y for x, y in arr]
    return dist(S[-1], x), S 

def outliers_DBnk(U, n, k, alpha, beta):
    """
    Outliers Detection using DB^n_k definition
    """
    ###### phase one ####################
    N = len(U)
    U_bak = U
    i_iter = 0
    while len(U) > beta * N:
        i_iter += 1
        print '>>>>> i_iter =', i_iter
        print '|U| =', len(U)
        # sample centers
        m = int(alpha * len(U)) + 1
        print '|S| =', m
        S = np.random.choice(U, m)
        # for each s in S, find its nearest k neighbors
        hyper_balls = [find_nearest_k(s, U, k + 1) for s in S]
        m = np.median([x for x, y in hyper_balls])
        # now construct the set that need to be removed
        to_remove = set([])
        for d, y in hyper_balls:
            if d <= m:
                to_remove |= set([id(x) for x in y])
        # remove points in to_remove
        U = [u for u in U if id(u) not in to_remove]
    ###### phase two #####################
    arr = [(k_th_dist(x, U_bak, k), x) for x in U]
    return [y for x, y in sorted(arr)[-n:]]
    
    

def detect_outliers(U, nOutliers, k, alpha=0.001, beta=0.01, gamma=0.8):
    ##### phase one
    # alpha << beta
    N = len(U)
    U_fixed = U
    
    i_iter = 0
    while len(U) > beta * N:
        i_iter += 1
        print '>>>> i_iter =', i_iter
        print '|U| =', len(U), 'gamma =', gamma
        # sample centers
        nSamples = int(alpha * len(U)) + 1
        print 'nSamples =', nSamples
        S = np.random.choice(U, int(alpha * N))
        assign = {}
        obj = {id(x):x for x in U}
        for x in U:
            assign[id(x)] = find_nearest(x, S)
        vt = [dist(obj[i], y) for i, y in assign.items()]
        t = int(gamma * len(U))
        v = sorted(vt)[t]
        print 't =', t, 'v =', v
        U = [x for x in U if dist(x, assign[id(x)]) >= v]
        # gamma =  gamma - gamma**4
        
    #### phase two
    arr = [(k_th_dist(x, U_fixed, k), x) for x in U]
    return [y for x, y in sorted(arr)[-nOutliers:]]

        
        
            
# def successive_sampling(U, nOutliers, alpha, beta):
#     """
#     U -- set of points
#     alpha -- integer, to control number of samples in each iteration
#     beta -- real in (0, 1)
#     Return: outliers and a configuration
#     """
#     config = []
#     # nOutliers should be larger than alpha
#     n_iter = 0
#     centers = []
#     max_dist = 0.
#     pre_len_U = 0
#     while len(U) > nOutliers / (1. - beta) / 3:
#         if len(U) == pre_len_U:
#             beta -= 0.1
#         pre_len_U = len(U)
#         n_iter += 1
#         print '>>>>> n_iter =', n_iter
#         print '|U| =', len(U)
#         print 'beta =', beta
#         # sample 
#         S = np.random.choice(U, alpha)
#         # add as centers
#         centers.extend([x for x in S])
#         # assign each x in U to its nearest point in S
#         assign = [Assoc(x, find_nearest(x, S)) for x in U]

#         # compute minimal v to make Ball(S, v) > beta * |U|
#         vs = np.array([a.getDist() for a in assign])
#         t = int(beta * len(U))
#         vs = sorted(vs)
#         v = vs[t]
#         if v > max_dist:
#             max_dist = v
#         # add configuration for points in Ball(S, v)
#         for a in assign:
#             if a.getDist() < v:
#                 config.append(a)
                
#         # remove Ball(S, v) from U
#         U = [a.this for a in assign if a.getDist() >= v]
        

#     # now we want to remove the false positive
#     U = [x for x in U if dist(x, find_nearest(x, S)) > max_dist]
        
#     return U, config

def read_from_file(fileName, n_skip = 1):
    lineN = 0
    data = []
    outliers = []
    with open(fileName, 'r') as fin:
        for line in fin:
            lineN += 1
            if lineN > n_skip:
                line = line.split(',')
                data.append((float(line[1])))
                if int(line[2]) == 1:
                    outliers.append(float(line[1]))

    return data, outliers

if __name__ == '__main__':
    # U, outliers = read_from_file(sys.argv[1])
    U, outliers = get_data(1000, 10) 
    nOutliers = len(outliers)
    print 'median =', np.median(U)
    
    # U.extend([5000 * i for i in xrange(1, nOutliers + 1)])

#    outliers_est, config = successive_sampling(U, nOutliers, 5, 0.9)
    outliers_est = outliers_DBnk(U, nOutliers, 4, 0.05, 0.09)
    outliers = set(outliers)
    outliers_est = set(outliers_est)
    print 'Ext:', sorted(outliers)
    print 'Est:', sorted(outliers_est)    

