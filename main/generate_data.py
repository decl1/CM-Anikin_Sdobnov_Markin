import random
def generate(batches_, stages_, sugarMin_, sugarMax_, degMin_, degMax_, concentrate_ = False, ripening_ = 0, inoInf_ = False):
    sugarMatrix = [[ 0 for i in range(stages_)] for j in range(batches_)]
    lossMatrix = [[ 0 for i in range(stages_)] for j in range(batches_)]
    for i in range(batches_):
        sugarMatrix[i][0] = random.uniform(sugarMin_, sugarMax_)
    if ripening_ == 0:
        degMatrix = [[ 0 for i in range(stages_ - 1)] for j in range(batches_)]
        if concentrate_:
            for i in range(batches_):
                const = random.uniform(0.00000001,(degMax_ - degMin_) / 4.0)
                constMin = random.uniform(degMin_, degMax_ - const)
                constMax = constMin + const
                for j in range(stages_ - 1):
                    degMatrix[i][j] = random.uniform(constMin, constMax)
        else:
            degMatrix = [[random.uniform(degMin_,degMax_) for i in range(stages_ - 1)] for j in range(batches_)]
    else:
        ripeningMax = (batches_ - 1)/(batches_ - 2)
        degMatrix = [[0 for i in range(stages_ - 1)] for j in range(batches_)]
        if concentrate_:
            for i in range(batches_):
                const = random.uniform(0.00000001, (ripeningMax - 1.0)/4)
                constMin = random.uniform(1.0, ripeningMax - const)
                constMax = constMin + const
                for j in range(ripening_):
                    degMatrix[i][j] = random.uniform(constMin, constMax)
            for i in range(batches_):
                const = random.uniform(0.00000001, (degMax_ - degMin_) / 4.0)
                constMin = random.uniform(degMin_, degMax_ - const)
                constMax = constMin + const
                for j in range(ripening_, stages_ - 1):
                    degMatrix[i][j] = random.uniform(constMin, constMax)
        else:
            for i in range(batches_):
                for j in range(ripening_):
                    degMatrix[i][j] = random.uniform(1.0, ripeningMax)
            for i in range(batches_):
                for j in range(ripening_, stages_ - 1):
                    degMatrix[i][j] = random.uniform(degMin_, degMax_)
    for i in range(batches_):
        for j in range(1,stages_):
            sugarMatrix[i][j] = sugarMatrix[i][j-1] * degMatrix[i][j-1]
    if inoInf_:
        KVector = [random.uniform(4.8, 7.05) for i in range(batches_)]
        NaVector = [random.uniform(0.21, 0.82) for i in range(batches_)]
        NVector = [random.uniform(1.58, 2.8) for i in range(batches_)]
        IMatrix = [[ 0 for i in range(stages_)] for j in range(batches_)]
        for i in range(batches_):
            IMatrix[i][0] = random.uniform(0.62,0.64)
        for i in range(batches_):
            for j in range(1,stages_):
                IMatrix[i][j] = IMatrix[i][j-1] * 1.22153980475
        lossMatrix = [[0.01*(1.2967+0.1514*(KVector[i]+NaVector[i])+0.2159*NVector[i]+0.9989*IMatrix[i][j]) for j in range(stages_)] for i in range(batches_)]
    else:
        lossMatrix = [[0 for i in range(stages_)] for j in range(batches_)]
    CMatrix = sugarMatrix
    LMatrix = lossMatrix
    SMatrix = [[CMatrix[i][j] * (1 - LMatrix[i][j]) for j in range(stages_)] for i in range(batches_)]
    return (CMatrix,LMatrix,SMatrix)