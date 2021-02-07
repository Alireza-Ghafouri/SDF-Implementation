def read_file():
    file= open ("topology_matrix.txt","rt")
    matrix= [[int(num) for num in line.split(",")] for line in file.readlines()]
    #return matrix
    


