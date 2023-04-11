

def lower_duplicate(x):
    y = (x & 0x0f)
    y |= (y << 2)
    y &= 0x33
    y |= (y << 1)
    y &= 0x55
    y |= (y << 1)
    return y

def lower_quadruplicate(x):
    y = (x & 0x03)
    y |= (y << 3)
    y &= 0x11
    y |= (y << 2)
    y &= 0x55
    y |= (y << 1)
    return y


a = 121
print("{:08b}: {:08b}, {:08b}".format(a, lower_duplicate(a), lower_quadruplicate(a)))


