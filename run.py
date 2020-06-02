import argparse
import numpy as np
import sys

from investor import Lot, optimized_solve, solve, LOTS_TYPE
from profiler import run, generate_input

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',  '-i', help="Path to input file")
    parser.add_argument('--output_file', '-o', help="Path to output file", default='output.txt')
    parser.add_argument('--algorithm',   '-a', choices=['app', 'profile_optimized', 'profile'],
                        default='app', help="Witch algorithm to run")
    parser.add_argument('-S', default=50000, type=int, help="Money amount (used for profiling only)")
    parser.add_argument('-N', default=250,   type=int, help="Number of days (used for profiling only)")
    parser.add_argument('-M', default=40,    type=int, help="Number of obligations (used for profiling only)")

    return parser.parse_args()

def format_output(indexes, profit, lots, S, output_file):
    j = S
    out_file = open(output_file, 'w+')
    out_file.write('%d\n' % profit)
    # outs = []
    # for i in range(len(lots), 0, -1):
    #     if j != backtrack[i][j]:
    #         outs.append((lots[i - 1].day, lots[i - 1].name, lots[i - 1].price/10, lots[i - 1].amount))
    #         j = backtrack[i][j]
    # outs.reverse()
    # for out in outs:
    #     out_file.write('%d %s %f %d\n' % out)
    for i in indexes:
        out = (lots[i].day, lots[i].name, lots[i].price/10, lots[i].amount)
        out_file.write('%d %s %f %d\n' % out)
    out_file.close()

def read_lots_from_file(file_path):
    input_file = open(file_path, 'r')
    input_lines = input_file.readlines()

    N, M, S = [int(x) for x in input_lines[0].split()]
    exporation_date = N + 30
    lots = np.array([])
    lots_values = np.array([], dtype=LOTS_TYPE)

    for input_string in input_lines[1:]:
        try:
            lot = Lot(*(input_string.split()), exporation_date)
            lots = np.append(lots, lot)
            lot_item = np.array([(lot.weight, lot.value)], dtype=LOTS_TYPE)
            lots_values = np.append(lots_values, lot_item)
        except Exception as exc:
            print(exc)
            sys.exit('Error reading file')

    return lots_values, lots, S, N, M

def main():
    args = parse_args()
    if args.algorithm == 'app':
        if args.input_file is None:
            sys.exit('Input file expected')
        lots_values, lots, S, _, _ = read_lots_from_file(args.input_file)
        out = optimized_solve(lots_values, S)
        profit, indexes = out[0, 0], out[0, 1:]
        format_output(indexes, profit, lots, S, args.output_file)
    else:
        if args.input_file:
            lots_values, lots, S, N, M = read_lots_from_file(args.input_file)
            if args.algorithm == 'profile_optimized':
                out = optimized_solve(lots_values, S)
                profit, indexes = out[0, 0], out[0, 1:]
                format_output(indexes, profit, lots, S, args.output_file)
                run(lots_values, S, N, M, args.output_file)
            else:
                out = solve(lots, S)
                profit, indexes = out[0, 0], out[0, 1:]
                format_output(indexes, profit, lots, S, args.output_file)
                run(lots, S, N, M, args.output_file, nonoptimized=True)
        else:
            lots_values, lots = generate_input(args.N, args.M)
            if args.algorithm == 'profile_optimized':
                out = optimized_solve(lots_values, args.S)
                profit, indexes = out[0, 0], out[0, 1:]
                format_output(indexes, profit, lots, args.S, args.output_file)
                run(lots_values, args.S, args.N, args.M, args.output_file)
            else:
                out = solve(lots, args.S)
                profit, indexes = out[0, 0], out[0, 1:]
                format_output(indexes, profit, lots, args.S, args.output_file)
                run(lots, args.S, args.N, args.M, args.output_file, nonoptimized=True)

if __name__ == '__main__':
    main()
