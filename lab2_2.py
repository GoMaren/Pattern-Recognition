import numpy as np
import random
import time
import matplotlib.pyplot as plt

# Counting sum of sub-array of 1-dimentional array
def sum1(a, l, r):
    
    return np.sum(a[l:r + 1])

# Counting sum of sub-array of 2-dimentional array
def sum2(a, l ,r):
    
    return np.sum(a[l[0]:r[0] + 1, l[1]:r[1] + 1])

# Counting sum of sub-array of 3-dimentional array
def sum3(a, l, r):
   
   return np.sum(a[l[0]:r[0] + 1, l[1]:r[1] + 1, l[2]:r[2] + 1])

# Smart sum array precalculating for 1-dimentional array
def sumAlg1(a, m):
    sumA = np.zeros(m)
    sumA = np.asarray(sumA, dtype = np.int32)
    sumA[0] = a[0]
    for i in np.arange(1, m, 1):
        sumA[i] = sumA[i - 1] + a[i]
        
    return sumA

# Smart sum array precalculating for 2-dimentional array
def sumAlg2(a, m):
    sumA = np.zeros((m, m))
    sumA = np.asarray(sumA, dtype = np.int32)
    sumA[0][0] = a[0][0]
    # Filling first column and first row
    for i in np.arange(1, m, 1):
        sumA[i][0] = sumA[i-1][0] + a[i][0]
        sumA[0][i] = sumA[0][i-1] + a[0][i]

    # Filling upper triangle
    for i in np.arange(1, m, 1):
        for j in np.arange(1, i, 1):
             sumA[i-j][j] =  sumA[i-j-1][j]+sumA[i-j][j -1]+a[i-j][j]-sumA[i-j-1][j-1]

    # Filling lower triangle
    for j in np.arange(1, m, 1):
        for i in np.arange(0, m - j, 1):
             sumA[m-1-i][j+i] =  sumA[m-2-i][j+i]+sumA[m-1-i][j-1+i]+a[m-1-i][j+i]-sumA[m-2-i][j-1+i]
             
    return sumA

# Smart sum array precalculating for 3-dimentional array
def sumAlg3(a, m):
    sumA = np.zeros((m, m, m))
    sumA = np.asarray(sumA, dtype = np.int32)
    sumA[0][0][0] = a[0][0][0]

    # Filling first lines of each axis
    for i in np.arange(1, m, 1):
        sumA[i][0][0] = sumA[i-1][0][0]+a[i][0][0] 
        sumA[0][i][0] = sumA[0][i-1][0]+a[0][i][0] 
        sumA[0][0][i] = sumA[0][0][i-1]+a[0][0][i]

    # Filling upper triangles of the first 3 sides 
    for i in np.arange(1, m, 1):
        for j in np.arange(1, i, 1):
            sumA[i-j][j][0] = sumA[i-1-j][j][0]+sumA[i-j][j-1][0]+a[i-j][j][0]-sumA[i-1-j][j-1][0]
            sumA[i-j][0][j] = sumA[i-1-j][0][j]+sumA[i-j][0][j-1]+a[i-j][0][j]-sumA[i-1-j][0][j-1]
            sumA[0][i-j][j] = sumA[0][i-1-j][j]+sumA[0][i-j][j-1]+a[0][i-j][j]-sumA[0][i-1-j][j-1]

    # Filling lower triangles of the first 3 sides 
    for j in np.arange(1, m, 1):
        for i in np.arange(0, m - j, 1):
            sumA[m-1-i][j+i][0] = sumA[m-2-i][j+i][0]+sumA[m-1-i][j-1+i][0]+a[m-1-i][j+i][0]-sumA[m-2-i][j-1+i][0]
            sumA[m-1-i][0][j+i] = sumA[m-2-i][0][j+i]+sumA[m-1-i][0][j-1+i]+a[m-1-i][0][j+i]-sumA[m-2-i][0][j-1+i]
            sumA[0][m-1-i][j+i] = sumA[0][m-2-i][j+i]+sumA[0][m-1-i][j-1+i]+a[0][m-1-i][j+i]-sumA[0][m-2-i][j-1+i]

    # Filling first half of the cube
    for i in np.arange(1, m, 1):
        for j in np.arange(1, i + 1, 1):
            for k in np.arange(1, i - j + 2, 1):
                sumA[j][i-j-k+2][k] = a[j][i-j-k+2][k]+sumA[j-1][i-j-k+2][k]+sumA[j][i-j-k+1][k]+sumA[j][i-j-k+2][k-1]
                sumA[j][i-j-k+2][k] -= sumA[j-1][i-j-k+1][k]+sumA[j-1][i-j-k+2][k-1]+sumA[j][i-j-k+1][k-1]
                sumA[j][i-j-k+2][k] += sumA[j-1][i-j-k+1][k-1]

    # Filling second half of the cube
    for i in np.arange(m, 3 * m, 1):
        for j in np.arange(1, m, 1):
            for k in np.arange(1, i - j + 2, 1):
                if (k < m) and (i - j - k + 2 < m):
                    sumA[j][i-j-k+2][k] = a[j][i-j-k+2][k]+sumA[j-1][i-j-k+2][k]+sumA[j][i-j-k+1][k]+sumA[j][i-j-k+2][k-1]
                    sumA[j][i-j-k+2][k] -= sumA[j-1][i-j-k+1][k]+sumA[j-1][i-j-k+2][k-1]+sumA[j][i-j-k+1][k-1]
                    sumA[j][i-j-k+2][k] += sumA[j-1][i-j-k+1][k-1]

    return sumA

amountOfTests = 5
repeatSum = 1000
timeConsumed = np.zeros((3, 2, amountOfTests))
timeConsumed = np.asarray(timeConsumed, dtype = np.float64)
amount = np.zeros((3, amountOfTests))
amount = np.asarray(amount, dtype = np.int32)

for i in range(amountOfTests):
    
    # For 1-d
    print("1-D")
    # Amount of elements
    m = 100000 * (i + 1)
    amount[0][i] = m
    print("m = {}".format(m))

    # Filling array with random integers
    arr = np.random.randint(0, 25, m)

    l = 10 * (i + 1)
    r = 90000 * (i + 1)

    timeEasy = time.perf_counter()
    for j in range(repeatSum):
        sumEasy = sum1(arr, l, r)
    fullTimeEasy = time.perf_counter() - timeEasy
    timeConsumed[0][0][i] = fullTimeEasy

    # Calculating array of sums with algorith and then calculating sum
    timeAlgorithm = time.perf_counter()
    sumAlgArray = sumAlg1(arr, m)
    fullTimeAlgorithm = time.perf_counter() - timeAlgorithm
    timeConsumed[0][1][i] = fullTimeAlgorithm
    sumAlg = sumAlgArray[r] - sumAlgArray[l - 1]

    print("Easy sum =      {}".format(sumEasy))
    print("Time consumed = {}".format(fullTimeEasy))
    print("Algorithm sum = {}".format(sumAlg))
    print("Time consumed = {}".format(fullTimeAlgorithm))
    
    # For 2-d
    print("2-D")
    # Amount of elements
    m = 50 * (i + 1)
    amount[1][i] = m
    print("m = {}".format(m))

    # Filling matrix with random integers
    arr = np.random.randint(0, 25, (m, m))

    l = [1 * (i + 1), 1 * (i + 1)]
    r = [40 * (i + 1), 40 * (i + 1)]

    timeEasy = time.perf_counter()
    for j in range(repeatSum):
        sumEasy = sum2(arr, l, r)
    fullTimeEasy = time.perf_counter() - timeEasy
    timeConsumed[1][0][i] = fullTimeEasy

    # Calculating array of sums with algorith and then calculating sum
    timeAlgorithm = time.perf_counter()
    sumAlgArray = sumAlg2(arr, m)
    fullTimeAlgorithm = time.perf_counter() - timeAlgorithm
    timeConsumed[1][1][i] = fullTimeAlgorithm
    sumAlg = sumAlgArray[r[0]][r[1]]
    sumAlg -= (0 if (l[0]==0) else sumAlgArray[l[0]-1][r[1]])
    sumAlg -= (0 if (l[1]==0) else sumAlgArray[r[0]][l[1]-1])
    sumAlg += (0 if (l[0]==0) else (0 if (l[1]==0) else sumAlgArray[l[0]-1][l[1]-1]))

    print("Easy sum =      {}".format(sumEasy))
    print("Time consumed = {}".format(fullTimeEasy))
    print("Algorithm sum = {}".format(sumAlg))
    print("Time consumed = {}".format(fullTimeAlgorithm))
    
    # For 3-d
    print("3-D")
    # Amount of elements
    m = 10 * (i + 1)
    amount[2][i] = m
    print("m = {}".format(m))

    # Filling cube with random integers
    arr = np.random.randint(0, 25, (m, m, m))

    l = [1 * (i + 1), 1 * (i + 1), 1 * (i + 1)]
    r = [7 * (i + 1), 7 * (i + 1), 7 * (i + 1)]

    timeEasy = time.perf_counter()
    for j in range(repeatSum):
        sumEasy = sum3(arr, l, r)
    fullTimeEasy = time.perf_counter() - timeEasy
    timeConsumed[2][0][i] = fullTimeEasy

    # Calculating array of sums with algorith and then calculating sum
    timeAlgorithm = time.perf_counter()
    sumAlgArray = sumAlg3(arr, m)
    fullTimeAlgorithm = time.perf_counter() - timeAlgorithm
    timeConsumed[2][1][i] = fullTimeAlgorithm
    sumAlg = sumAlgArray[r[0]][r[1]][r[2]]
    sumAlg -= (0 if (l[0]==0) else sumAlgArray[l[0]-1][r[1]][r[2]])
    sumAlg -= (0 if (l[1]==0) else sumAlgArray[r[0]][l[1]-1][r[2]])
    sumAlg -= (0 if (l[2]==0) else sumAlgArray[r[0]][r[1]][l[2]-1])
    sumAlg += (0 if (l[0]==0) else (0 if (l[1]==0) else sumAlgArray[l[0]-1][l[1]-1][r[2]]))
    sumAlg += (0 if (l[0]==0) else (0 if (l[2]==0) else sumAlgArray[l[0]-1][r[1]][l[2]-1]))
    sumAlg += (0 if (l[1]==0) else (0 if (l[2]==0) else sumAlgArray[r[0]][l[1]-1][l[2]-1]))
    sumAlg -= (0 if (l[0]==0) else (0 if (l[1]==0) else ( 0 if (l[2]==0) else sumAlgArray[l[0]-1][l[1]-1][l[2]-1])))

    print("Easy sum =      {}".format(sumEasy))
    print("Time consumed = {}".format(fullTimeEasy))
    print("Algorithm sum = {}".format(sumAlg))
    print("Time consumed = {}".format(fullTimeAlgorithm))

for i in range(3):
    plt.plot(amount[i], timeConsumed[i][0])
    plt.plot(amount[i], timeConsumed[i][1])
    plt.show()








