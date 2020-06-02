from memory_profiler import profile
import numpy as np
import time

from investor import Lot, optimized_solve, solve, LOTS_TYPE

def generate_input(n, m):
    exporation_date = n + 30
    lots = []
    lots_values = np.array([], dtype=LOTS_TYPE)
    name = 'obligation'

    for i in range(n + 1):
        for j in range(m + 1):
            price = np.random.uniform(10, 200)
            amount = np.random.randint(1, 1000)
            lot = Lot(i, name, price, amount, exporation_date)
            lots.append(lot)
            lot_item = np.array([(lot.weight, lot.value)], dtype=LOTS_TYPE)
            lots_values = np.append(lots_values, lot_item)

    return lots_values, lots

@profile
def mem_profile(lots, solver, s):
    b, profit = solver(lots, s)

def time_profile(lots, solver, s, n, m):
    start_time = time.time()
    _, _ = solver(lots, s)
    el_time = time.time() - start_time
    print(n, m, s, el_time, sep=" ")

def run(lots, s, n, m, output_file, nonoptimized=False):
    solver = solve if nonoptimized else optimized_solve
    # sys.stdout = open(output_file, 'w+')
    mem_profile(lots, solver, s)
    time_profile(lots, solver, s, n, m)
