def lineal_inverted(x, min_x, max_x):
    m = 1.0 / (max_x - min_x)
    return 1.0 -  (m * x)

def lineal(x, min_x, max_x):
    m = 1.0 / (max_x - min_x)
    return (m * x) + min_x


def identity(x):
    return x
