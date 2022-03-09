from numpy import float32
import matplotlib.pyplot as plt
import time

#v = 0.53125
v = 0.1
N = 10 ** 7
tab = [float32(v) for _ in range(N)]
step = 25000


def count_sum(T, step):
    relative_error_in_steps = [0.0]
    result = float32(0.0)
    for i in range(len(T)):
        result += T[i]
        if (i + 1) % step == 0:
            tmp_error = abs(v * (i + 1) - result) / (v * (i + 1))
            relative_error_in_steps.append(tmp_error)

    return result, relative_error_in_steps


def merge_sum(T):
    if len(T) > 2:
        return merge_sum(T[:len(T) // 2]) + merge_sum(T[len(T) // 2:])
    else:
        return T[0] if len(T) == 1 else T[0] + T[1]


# bezwzględny
def absolute_error(counted, precise):
    return abs(precise - counted)


# względny
def relative_error(counted, precise):
    return absolute_error(counted, precise) / precise


start_algo = time.time()
algorithm_sum, step_errors = count_sum(tab, step)
algo_time = time.time() - start_algo
precise_sum = v * N

print(f'algo: {algorithm_sum}, precise: {precise_sum}')

absolute_algo_error = abs(precise_sum - algorithm_sum)
relative_algo_error = absolute_algo_error / precise_sum

print(f'absolute: {absolute_algo_error}, relative: {relative_algo_error}')

# getting plot for step_errors
steps = [x * step for x in range(0, N // step + 1)]

plt.plot(steps, step_errors)
plt.xlabel('STEPS')
plt.ylabel('ERROR')
plt.show()

start_merge = time.time()
merge_sum_result = merge_sum(tab)
merge_time = time.time() - start_merge

print(f'algo_merge: {merge_sum_result}, precise: {precise_sum}')

absolute_merge_error = absolute_error(merge_sum_result, precise_sum)
relative_merge_error = relative_error(merge_sum_result, precise_sum)

print(f'absolute: {absolute_merge_error}, relative: {relative_merge_error}')

print(f'algo time: {algo_time}, merge time: {merge_time}')
