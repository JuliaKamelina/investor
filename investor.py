from numba import njit
import numpy as np

LOTS_TYPE = np.dtype([('weight', 'i4'), ('value', 'i4')])

class Lot(object):

    def __init__(self, day, name, price, amount, exporation_date):
        self.name = name
        self.price = float(price)*10
        self.day = int(day)
        self.amount = int(amount)

        self.weight = int(self.price * self.amount)
        self.value = int((exporation_date - self.day + 1000 - self.price) * self.amount)

@njit
def optimized_solve(lots: np.ndarray, S: int):
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

    return backtrack, m[len(lots)][S]

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