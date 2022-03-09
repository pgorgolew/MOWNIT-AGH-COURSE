from numpy import float32
import time

v = 0.53125
v_marta = 0.84359234
#v = 0.8591295
N = 10 ** 7
tab = [float32(v_marta) for _ in range(N)]
step = 25000
precise_sum = N * v_marta


def kahan(T):
    sum = float32(0)
    err = float32(0)
    for i in range(len(T)):
        y = float32(T[i] - err)
        temp = float32(sum + y)
        err = (temp - sum) - y
        sum = temp

    sum = float32(sum - err)
    return sum


# bezwzględny
def absolute_error(counted, precise):
    return abs(precise - counted)


# względny
def relative_error(counted, precise):
    return absolute_error(counted, precise) / precise


start = time.time()
kahan_sum = kahan(tab)
kahan_time = time.time() - start
relative_kahan_err = relative_error(kahan_sum, precise_sum)
absolute_kahan_err = absolute_error(kahan_sum, precise_sum)

print(f'algo_sum: {kahan_sum}, precise: {precise_sum}')
print(f'absolute: {absolute_kahan_err}, relative: {relative_kahan_err}')

print(f'kahan time: {kahan_time}')
