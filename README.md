# Precomputed-Dominant-Resource-Fairness

The two Jupyter-Notebooks in this repository is aimed to demonstrate calculations in the article Precomputed Dominant Resource Fairness (PDRF).

Note that PDRF_Core_Calculator is not a full implementation of PDRF, but an implementation of the core calculation of the algorithm for proof of concept purposes.

The third notebook, Numerical Analysis, demonstrates the accuracy of PDRF with respect to DRF. In the tests carried out with different number of users, demand intervals and resource capacity intervals, 45%-55% percent allocations deviate from the final DRF distribution, predominantly by 1 task. Overallocations constitute approximately 3% of those. If the overallocations are not tolerable, a more conservative allocation algorithm may be obtained by rounding cycle iterations down, before multiplying with the ratios. In this case, the underallocations may rise up to 100% and may be as much as 6-7 tasks, yet no overallocation is observed.

When the ratio between the demand interval and the resource capacities are high, PDRF performs better in terms of return latency.

Further data will be collected for more accurate statistical demonstration.
