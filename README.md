# Precomputed-Dominant-Resource-Fairness

The files in this repository implement Precomputated Dominant Resource Fairness(PDRF), which is an algorithm to approximate Dominant Resource Fairness (DRF) allocation in fewer steps, by precomputing the DRF iterations and assigning the resulting allocations.

There are two implementations, one uses the maximum dominant share variable, and the other, by the virtue of a simplification step, does not use it. Presumably for numerical reasons, and surprisingly, the one that uses maximum dominant share returns more accurate allocations and performs better in terms of return times.

The Jupyter-Notebooks for numerical analysis create random data, process it wiht DRF and PDRF, and compare the differences. Python scripts are basicly same, but simplified for printing out raw data to be used in the analyses. Scripts are run 1000 times with different parameters and the data is analysed with Statistics.ipynb, which can be found under the Results folder, along with both the raw data and the tables created with them.
