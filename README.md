# Precomputed-Dominant-Resource-Fairness

The files in this repository implement **Precomputed Dominant Resource Fairness (PDRF)**, an algorithm that approximates Dominant Resource Fairness (DRF) allocation in fewer steps by precomputing the DRF iterations and assigning the resulting allocations.

There are two implementations. One uses the maximum dominant share variable; the other, by virtue of a simplification step, does not. In the original experiments, we observed, to our surprise, that the unsimplified version returns more accurate results and shorter execution times. However, the tests carried out by ChatGPT did not replicate this result. We leave both implementations in the repository.

The Jupyter notebooks for numerical analysis generate random data, process it using DRF and PDRF, and compare the resulting allocations. The Python scripts perform essentially the same computations but are simplified to print raw data for subsequent analysis. The scripts are run 1,000 times with different parameters.

## Experiments and Results

The repository contains two sets of experiments:

- **Original:** Experiments conducted by the author. Their results and raw data are available in the `Results/Original` directory.
- **ChatGPT:** A separate set of experiments conducted by ChatGPT. Their results and raw data are available in the `Results/ChatGPT` directory.

The `Results` directory also contains the `Statistics.ipynb` notebook and the tables generated from the experimental data.
