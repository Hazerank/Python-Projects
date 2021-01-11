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
Checks if the given row has any nonzero (significantly larger or smaller than zero) values by iterating through the list.
row is the list to check its values.
Returns if there is any nonzero values.
"""
def notZero(row):
    for i in row:
        if abs(i) > 0.0000001 : return True
    return False

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
        for i in range(size,len(line) - 1):
            newLine.append(line[i])
        newMatrix.append(newLine)
            
    return newMatrix

"""
Extracts the A'|b' matrix from the matrix our functions processed.
matrix is the matrix to extract values.
size is the length of the A'|b' matrix.
Returns the A'|b' matrix as list of lists of float numbers.
"""
def normalize(matrix, size):
    newMatrix = []
    for line in matrix:
        newLine = []
        for i in range(size):
            newLine.append(line[i])
        newLine.append(line[-1])
        newMatrix.append(newLine)
            
    return newMatrix


"""
Reads A|b matrix from the input file, adds new columns for the Identity Matrix to create A|I|b.
matrixP is the list data structure to process.
input is a string that identifies input file.
Returns the A|I|b matrix as list of lists of float numbers.
"""
def readFile(matrixP , input):
    with open("data"+ str(input) + ".txt", "r") as f:
        size = int(f.read(1))
        f.read(1)
        data = f.readlines()
        i = 0
        for line in data:
            row = []
            rowTemp = line.split()
         
            wide = len(rowTemp)
            
            for j in range(wide + size ):
                if j < wide - 1:
                    row.append(float(rowTemp[j]))
                elif j < wide + size - 1:
                    if j - wide + 1 == i:
                        row.append(float(1))
                    else:
                        row.append(float(0))
                else:
                    row.append(float(rowTemp[-1]))

            matrixP.append(row)
            i += 1

        return(matrixP, size)

"""
Solves the problem for inconsistent and infinitely many case.
Does pivotting operation and prints the results.
"""
def irregular(matrix, row, size):
    noPiv = [row + 1]
    for pivot in range(row + 1, size):
        i = pivot - len(noPiv)
        pivotRow = pivot - len(noPiv)
        while abs(matrix[i][pivot]) < 0.000001:
            i += 1
            if i == size:
                noPiv.append(pivot + 1)
                break
        if i == size: continue
        
        matrix = interChange(pivotRow,i,matrix)
        matrix = multiplyScale(pivotRow, 1/matrix[pivotRow][pivot], matrix)

        for i in range(0,size):
            if i == pivotRow: continue
            matrix = interRow(pivotRow, -1 * matrix[i][pivot],i,matrix)
    rows = -1 * len(noPiv)
    while rows != 0:
        if notZero(matrix[rows]):
            print("Inconsistent problem")
            return
        rows += 1
    print("Arbitrary variables: " , *noPiv )
    solutionList = []
    for i in range(len(matrix) - len(noPiv) ):
        solutionList.append(round(matrix[i][-1],4))
    for x in noPiv:
        solutionList.insert(x-1, 0)
        
    print("Arbitrary solution:",*solutionList)
    return

"""
The function which solves the given matrix.
It calls Irregular() function in the cases where there is no unique solution.
Prints the results and A^-1 matrix.
"""
def solve(matrix,size):
    for pivot in range(size):
        i = pivot
        while abs(matrix[i][pivot]) < 0.000001:
            i += 1
            if(i == size):
                matrix = normalize(matrix,size)
                irregular(matrix,pivot,size)
                return
        
        matrix = interChange(pivot,i,matrix)
        matrix = multiplyScale(pivot, 1/matrix[pivot][pivot], matrix)

        for i in range(0,size):
            if i == pivot: continue
            matrix = interRow(pivot, -1 * matrix[i][pivot],i,matrix)
      
    
    solutionList = []
    for i in range(len(matrix)):
        solutionList.append(matrix[i][-1])
        
    print("Unique solution:", *solutionList)
    inverse = getInverse(matrix,size)
    print("Inverted A: ", *inverse[0])
    for i in range(1,len(inverse)):
        print("            ", *inverse[i])


"""
Main of the code, calls 4 input txt files.
"""
matrixP = []
global size
for input in range(1,5):
    matrixP, size = readFile(matrixP, input)

    print("Dataset ",input)
    solve(matrixP,size)
    print("--------------")
    matrixP = []
   



