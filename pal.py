def stringify(x):
    s = str(x)
    stringified = ''.join([ c for c in s if c != '.'])
    if '-' in s:
        stringified = stringified.strip('-')
    if '.' in s:
        stringified = stringified[:-1]
    return stringified

def pal(x):
    stringified = stringify(x)
    return pal_str(stringified)

def pal_str(s):
    return s == s[::-1]

def pal_dist(x):
    old = -1
    y = []
    xval = []
    for n in x:
        if pal(n):
            if old == -1:
                d = 0
            else:
                d = n - old
            old = n
            y.append(d)
            xval.append(n)
    return xval, y

def pal_len(x):
    y = []
    xval = []
    for n in x:
        s = stringify(n)
        if pal_str(s):
            y.append(len(s))
            xval.append(n)
    return xval, y

def augment_x(x, precision, scale, n):
    if n > precision:
        return x
    newx = []
    for el in x:
        for i in range(0,10):
            val = el+i/10**(n+scale)
            val = round(val, n+scale)
            newx.append(val)
    return augment_x(newx, precision, scale, n+1)
