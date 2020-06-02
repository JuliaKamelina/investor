import numpy as np
import numba as nb
from numba import njit, types, jit
from numba.typed import Dict, List

LOTS_TYPE = np.dtype([('weight', np.int64), ('value', np.int64)])

class Lot(object):

    def __init__(self, day, name, price, amount, exporation_date):
        self.name = name
        self.price = float(price)*10
        self.day = int(day)
        self.amount = int(amount)

        self.weight = int(self.price * self.amount)
        self.value = int((exporation_date - self.day + 1000 - self.price) * self.amount)

@jit(nb.int64[:](nb.from_dtype(LOTS_TYPE)[:], nb.int64))
def optimized_solve(lots, S):
    m = np.zeros((len(lots) + 1, S + 1), dtype=np.int32)
    backtrack = np.zeros(m.shape, dtype=np.int32)

    for i in range(1, len(lots) + 1):
        for j in range(0, S + 1):
            w = lots[i - 1].weight
            v = lots[i - 1].value
            if j >= w:
                m[i][j] = max(m[i - 1, j], m[i - 1, j - w] + v)
            else:
                m[i][j] = m[i - 1][j]

            if m[i][j] == m[i - 1][j]:
                backtrack[i][j] = j
            else:
                backtrack[i][j] = j - w

    out_indexes = []
    for i in range(len(lots), 0, -1):
        if j != backtrack[i][j]:
            out_indexes.append(i - 1)
            j = backtrack[i][j]
    out_indexes.reverse()

    return np.array([[m[len(lots)][S]] + out_indexes], dtype=np.int64)

def solve(lots, S):
    m = np.zeros((len(lots) + 1, S + 1), dtype=np.int32)
    backtrack = np.zeros(m.shape, dtype=np.int32)

    for i in range(1, len(lots) + 1):
        for j in range(0, S + 1):
            w = lots[i - 1].weight
            v = lots[i - 1].value
            if w > j:
                m[i][j] = m[i - 1][j]
            else:
                m[i][j] = max(m[i - 1, j], m[i - 1, j - w] + v)

            if m[i][j] == m[i - 1][j]:
                backtrack[i][j] = j
            else:
                backtrack[i][j] = j - w
    return backtrack, m[len(lots)][S]
