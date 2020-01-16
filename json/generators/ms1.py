def ms1(delta, num, cacheline=64, elem=8, veclen=8, offset=0):
    # delta     -> distance from last cacheline to next
    # num       -> number of cachelines accessed
    # cacheline -> size of cacheline in bytes
    # elem      -> size of element in bytes (must evenly divide cacheline)
    # veclen    -> size of vector in elements
    # offset    -> offset each access by this many elements

    if num < 1 or num > veclen:
        raise ValueError('num must be between 1 and veclen. A gather cannot access fewer than 1 cacheline and it cannot access more cachelines than it has elements')

    
    a = [[i*(delta)*(cacheline//elem)]*(veclen//num + int(i<veclen%num)) for i in range(num)]
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][0]+j+offset
    #flatten
    b = [item for sublist in a for item in sublist]
    # recommended delta
    d = num*delta*(cacheline//elem)
    return {'pattern':tuple(b), 'delta':d, 'name':'MS1_{}_{}'.format(num, delta)}



