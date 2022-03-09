import numpy as np

#xn+1=rxn(1−xn)
def next_interation(r, x_n):
    return r*x_n*(1-x_n)