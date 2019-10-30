import numpy as np
import random

# Function for creating probabilities p(k|x)
def makeProbabilities(k, x):
    prob = np.random.randint(0, 100, (k, x))
    sums = np.sum(prob, axis = 0)
    prob = prob / sums[None,:]
    
    return prob

# Function for first risk (square) for first q
# In stead of calculating M(k|x)
# We are trying to find such k that risk is minimal
def R1forq1(k, x, prob):
    Rfull = 0.0
    for i in range(x):
        # For each x we are trying to find such k
        # That partial risk is minimal
        # And then we are just summing those minimal risks
        Rpartial = 1000000000.0
        for kwithstar in range(k):
            R = 0.0
            for j in range(k):
                R += prob[j][i] * ((kwithstar - j) ** 2)

            if (Rpartial > R):
                Rpartial = R
                
        Rfull += Rpartial
    # p(x) = 1/|X|, so we are just deviding R for |X|
    Rfull /= x
    
    return Rfull

# Function for second risk (binary) for first q
# In stead of calculating M(k|x)
# We are trying to find such k that risk is minimal
def R2forq1(k, x, prob):
    Rfull = 0.0
    for i in range(x):
        # For each x we are trying to find such k
        # That partial risk is minimal
        # And then we are just summing those minimal risks
        Rpartial = 1000000000.0
        for kwithstar in range(k):
            R = prob[kwithstar][i]

            if (Rpartial > R):
                Rpartial = R
                
        Rfull += Rpartial
    # p(x) = 1/|X|, so we are just deviding R for |X|
    Rfull /= x
    
    return 1 - Rfull

# Function for second q
def q2(k, x, alpha, prob):
    tprob = np.transpose(prob)
    indmax = np.where(tprob[x] == np.amax(tprob[x]))
    
    return indmax[0][0]

# Function for third q
def q3(k, x, alpha, prob):
    minsum = 1000000000.0
    indmin = 0
    for i in range(k):
        sump = 0.0
        for j in range(k):
            sump += prob[j][x] * ((j - i) ** 2)
        sump -= alpha * prob[i][x]
        if (minsum > sump):
            minsum = sump
            indmin = i
            
    return indmin

# Function for first risk (square) for second and third q
def R1forq23(k, x, alpha, prob, q):
    R = 0.0
    for i in range(x):
        # We are making optimization here
        # By not using q function every time in next cycle
        kwithstar = q(k, i, alpha, prob)
        for j in range(k):
            R += prob[j][i] * ((kwithstar - j) ** 2)
    # p(x) = 1/|X|, so we are just deviding R for |X|
    R /= x
    
    return R

# Function for second risk (binary) for second and third q
def R2forq23(k, x, alpha, prob, q):
    R = 0.0
    for i in range(x):
        R += prob[q(k, i, alpha, prob)][i]
    # p(x) = 1/|X|, so we are just deviding R for |X|
    R /= x
    # In strategy we need to use 1 - R
    # R(real) = Sum(k <> k with star) =
    # = 1 - Sum(k == k with start) = 1 - R(which we are counting above)
    
    return 1 - R

def test():
    delta = 0.0000001
    k = 2
    x = 3
    a = 0
    prob = makeProbabilities(k, x)
    prob[0][0] = 0.1
    prob[0][1] = 0.3
    prob[0][2] = 0.4
    prob[1][0] = 0.9
    prob[1][1] = 0.7
    prob[1][2] = 0.6

    assert (R1forq1(k, x, prob) > 4./15. - delta), 'Not passed'
    assert (R1forq23(k, x, alpha, prob, q2) > 4./15. - delta), 'Not passed'
    assert (R1forq23(k, x, a, prob, q3) > 4./15. - delta), 'Not passed'
    assert (R2forq1(k, x, prob) > 11./15. - delta), 'Not passed'
    assert (R2forq23(k, x, alpha, prob, q2) > 4./15. - delta), 'Not passed'
    assert (R2forq23(k, x, a, prob, q3) > 4./15. - delta), 'Not passed'

    assert (R1forq1(k, x, prob) < 4./15. + delta), 'Not passed'
    assert (R1forq23(k, x, alpha, prob, q2) < 4./15. + delta), 'Not passed'
    assert (R1forq23(k, x, a, prob, q3) < 4./15. + delta), 'Not passed'
    assert (R2forq1(k, x, prob) < 11./15. + delta), 'Not passed'
    assert (R2forq23(k, x, alpha, prob, q2) < 4./15. + delta), 'Not passed'
    assert (R2forq23(k, x, a, prob, q3) < 4./15. + delta), 'Not passed'

    print("Test passed")

# Main part
k = 25
x = 100
alpha = [0, 1, -1, 777, -777, 1000000, -1000000, 1000000000, -1000000000]

prob = makeProbabilities(k, x)
print(prob)

print('R1(q1) = {}'.format(R1forq1(k, x, prob)))
print('R1(q2) = {}'.format(R1forq23(k, x, alpha, prob, q2)))
for a in alpha:
    print('R1(q3, alpha = {}) = {}'.format(a, R1forq23(k, x, a, prob, q3)))
print('R2(q1) = {}'.format(R2forq1(k, x, prob)))
print('R2(q2) = {}'.format(R2forq23(k, x, alpha, prob, q2)))
for a in alpha:
    print('R2(q3, alpha = {}) = {}'.format(a, R2forq23(k, x, a, prob, q3))) 

print('TEST')
test()
