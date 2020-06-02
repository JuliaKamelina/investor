# Optimization Lab

Realization of "Investor Task". `investor.py` contains implementation of optimized algorithm
and pure Python realization.

## How To Run

To run as an application:

```sh
python run.py -a app -i path/to/input_file.txt -o path/to/output_file.txt
```

To run profiling of optimized version:

```sh
python run.py -a profile_optimized
```

To run profiling of pure Python version:

```sh
python run.py -a profile
```

You can pass your input data for profiling using `-i` key,
otherwise profiling data will be generated automatically.

`-S`, `-N`, `-M` keys are used to generate random input data for profiling.

Run the application with the `-h` option to see help message.
