import random
def generate(matrix_size, base_min, base_max, hi_min, hi_max):
    CMatrix = [[ random.uniform(base_min,base_max) for i in range(matrix_size)] for j in range(matrix_size)]
    XVector = [ random.uniform(hi_min,hi_max) for i in range(matrix_size)]
    GMatrix = [[ 0 for i in range(matrix_size)] for j in range(matrix_size)]
    for i in range(matrix_size):
        for j in range(matrix_size):
            for s in range(j,matrix_size):
                GMatrix[i][j] += ((1 - XVector[i]) * CMatrix[i][s])
    return (CMatrix,XVector,GMatrix)
def GenerateDMatrix(CMatrix,XVector,UpdateOrder):
    matrix_size = len(CMatrix)
    DMatrix = [[ 0 for i in range(matrix_size)] for j in range(matrix_size)]
    for i in range(matrix_size):
        for j in range(matrix_size):
            sum1 = 0
            sum2 = 0
            for s in UpdateOrder[0:j]:
                sum1 += ((1 - XVector[s]) * CMatrix[s][j])
            for c in UpdateOrder[0:matrix_size]:
                sum2 += (XVector[c] * CMatrix[c][j])
            DMatrix[i][j] = sum1 + sum2 + (1 - XVector[i]) * CMatrix[i][j]
    return DMatrix
