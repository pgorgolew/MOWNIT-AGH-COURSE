from numpy import float64


def dzeta_forward(n, s):
    result = float64(0.0)
    for k in range(1, n):
        result += 1 / (k ** s)
    return result


def dzeta_backward(n, s):
    result = float64(0.0)
    for k in range(n, 0, -1):
        result += 1 / (k ** s)
    return result


def eta_forward(n, s):
    result = float64(0.0)
    for k in range(1, n):
        result += ((-1) ** (k - 1)) / (k ** s)
    return result


def eta_backward(n, s):
    result = float64(0.0)
    for k in range(n, 0, -1):
        result += ((-1) ** (k - 1)) / (k ** s)

    return result


N = [50, 100, 200, 500, 1000]
S = [2, 3.6667, 5, 7.2, 10]

for i in range(len(N)):
    n = N[i]
    s = float64(S[i])

    print('######################')
    print(f"n = {n}, s = {s}")
    print(f"dzeta forward: {dzeta_forward(n,s)}, dzeta backward: {dzeta_backward(n,s)}")
    print(f"eta forward: {eta_forward(n,s)}, eta backward {eta_backward(n,s)}")
    print("######################")
