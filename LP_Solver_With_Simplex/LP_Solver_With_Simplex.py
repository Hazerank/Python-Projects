#!/usr/bin/env python

"""
Interchanges matrix's i'th and j'th rows.
i and j is the ids of rows.
Returns new matrix.
"""
def interChange(i, j, matrix):
    rowTemp = matrix[i]
    matrix[i] = matrix[j]
    matrix[j] = rowTemp
    return matrix

"""
Multiplies matrix's i'th row with scalar j.
i is the id of the row and j is the scalar
Returns new matrix.
"""
def multiplyScale(i, j, matrix):
    for t in range(len(matrix[0])) :
        matrix[i][t] *= j
    return matrix

"""
Multiplies matrix's i'th row with scalar j and adds to j'th row.
i is the id of the base row, 
j is the scalar and,
k is the id of the target row.
Returns new matrix.
"""
def interRow(i, j, k, matrix):
    for t in range(len(matrix[0])) :
        matrix[k][t] += j * matrix[i][t]
    return matrix

"""
Adds Identity matrix at the end of the given matrix.
Returns new matrix.
"""
def identify(matrix):
    newMatrix = []
    k = 0
    for line in matrix:
        newLine = line

        for i in range(len(matrix)):
            if i == k:
                newLine.append(float(1))
            else:
                newLine.append(float(0))
        newMatrix.append(newLine)
        
        k += 1
            
    return newMatrix


"""
Multiplies two rows and returns a float value
"""
def rowMult(r1,r2):
    result = 0
    for i in range(len(r1)):
        result += r1[i]*r2[i]
    return float(result)

"""
Returns the transpose of n'th column of matrix
"""
def getColT(matrix,n):
    col = []
    for line in matrix:
        col.append(line[n])
    return col


"""
Returns the n'th column of matrix
"""
def getCol(matrix,n):
    col = []
    for line in matrix:
        col.append([line[n]])
    return col


"""
Applies matrix multiplication
"""
def matrixMult(m1,m2):
    resultMatrix = []
    for row in m1:
        tempRow = []
        for colNum in range(len(m2[0])):
            col = getColT(m2,colNum)
            tempRow.append(rowMult(row,col))
        resultMatrix.append(tempRow)

    if len(resultMatrix) == 1 and len(resultMatrix[0]) == 1:
        return resultMatrix[0][0]
    return resultMatrix

"""
Retuns wanted columns of given matrix as a new matrix.
"matrix" is the input matrix that will be extracted from.
"colList" is list of numbers of columns of matrix that will be extracted and fused together.
"""
def getMatrix(matrix,colList):
    newMatrix = []
    
    for row in matrix:
        newRow = []
        for colNum in colList:
            newRow.append(row[colNum])
        newMatrix.append(newRow)
    return newMatrix


"""
Extracts the inverse matrix from the matrix our functions processed.
matrix is the matrix to extract values.
size is the length of the inverse matrix.
Returns the inverse matrix as list of lists of float numbers.
"""
def getInverse(matrix, size):
    newMatrix = []
    for line in matrix:
        newLine = []
        for i in range(size,len(line)):
            newLine.append(line[i])
        newMatrix.append(newLine)
            
    return newMatrix

"""
Reads matrix from the input file, adds new columns as the Identity Matrix to add slack variables.
input is a string that identifies input file.
Returns corresponding data.
"""
def readFile(input):
    matrixA = []
    with open("Data"+ str(input) + ".txt", "r") as f:
        line = f.readline().split()
        m = int(line[0])
        n = int(line[1])
        cRow = []
        bCol = []
        data = f.readlines()
        i = 0
        first = True
        for line in data:
            row = []
            rowTemp = line.split()
            if first:
                cRow = [ int(x) for x in rowTemp ]
                for k in range(m):
                    cRow.append(float(0))
                first = False
                continue
                
            for j in range(n + m + 1):
                if j < n :
                    row.append(float(rowTemp[j]))
                elif j < n + m :
                    if j - n  == i:
                        row.append(float(1))
                    else:
                        row.append(float(0))
                else:
                    bCol.append([float(rowTemp[-1])])

            matrixA.append(row)
            i += 1

        return(matrixA, cRow, bCol, m, n)

"""
Takes the inverse of the given matrix and returns it.
"""
def inverse(matrix):
    size = len(matrix)
    matrix = identify(matrix)
    
    for pivot in range(size):
        i = pivot
        while abs(matrix[i][pivot]) < 0.000001:
            i += 1
        
        matrix = interChange(pivot,i,matrix)
        matrix = multiplyScale(pivot, 1/matrix[pivot][pivot], matrix)

        for i in range(0,len(matrix)):
            if i == pivot: continue
            matrix = interRow(pivot, -1 * matrix[i][pivot],i,matrix)
      
    return getInverse(matrix,size)    
    # inverse = getInverse(matrix,size)
    # print("Inverted A: ", *inverse[0])
    # for i in range(1,len(inverse)):
    #     print("            ", *inverse[i])
        

"""
The Revised Simplex Algorithm
"""
def solve(matrixA, cRow, bCol,m, n):
    
    basicV = [int(i) for i in range(n,n+m)]
    nonBasicV = [int(i) for i in range(n)]

    while True:
        
        cB = getMatrix([cRow],basicV)
        matrixB = getMatrix(matrixA,basicV)
        bInverse = inverse(matrixB)
        
        # price out
        cBBinverse = matrixMult(cB,bInverse)
        
        valid = 1 

        inVal = [0,0]
        for i in range(len(nonBasicV)):
            value = cRow[nonBasicV[i]] - matrixMult(cBBinverse,getCol(matrixA,nonBasicV[i]))
            if value == 0: 
                valid = 0
            if value < inVal[0]:
                inVal[0] = value
                inVal[1] = i

        # Break Control
        if inVal[0] == 0:
            rhs = matrixMult(bInverse, bCol)
            
            resultSet = []
            
            for i in range(n+m):
                resultSet.append(float(0))
            for i in range(len(basicV)):
                if rhs[i][0] < 0:
                    valid = -1
                    break
                resultSet[basicV[i]] = rhs[i][0]
            

            resultVal = matrixMult(cBBinverse,bCol)

            if valid == -1:
                print("Problem is infeasible!")
                break
            elif valid == 0:
                print("Problem has multiple optima, let us write one of the results:")
            print("Result set is: ", resultSet)
            print("Optimum value is: ", resultVal)
            break

        # ratio test
        colEnter = matrixMult(bInverse, getCol(matrixA, nonBasicV[inVal[1]]) )
        rhs = matrixMult(bInverse, bCol)

        valid = False
        outVal = [float('inf'),0]
        for i in range(len(colEnter)):
            if colEnter[i][0] <= 0:
                continue
            valid = True
            ratio = rhs[i][0]/colEnter[i][0]
            if ratio < outVal[0]:
                outVal[0] = ratio
                outVal[1] = i
        if not valid:
            print("Problem is unbounded below.")
            break

        # update basic and nonBasic set

        temp = nonBasicV[inVal[1]]
        nonBasicV[inVal[1]] = basicV[outVal[1]]
        basicV[outVal[1]] = temp

    


"""
Main of the code, calls 3 input txt files.
"""

#print(mult([[0,-10,-10]],[[48],[20],[8]]))
for input in range(1,6):
    matrixA, cRow, bCol, m, n = readFile(input)

    print("Dataset ",input)
    # print(matrixA,cRow,bCol)
    solve( matrixA, cRow, bCol, m, n)

    
    print("--------------")
    matrixP = []
