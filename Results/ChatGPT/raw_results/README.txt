PDRF/DRF independent rerun — raw outputs
========================================

Run date: 2026-10-31
Experiment script: run_PDRF_experiments_corrected.py (from the user's Library bundle)
Seed: 20261031 (NumPy SeedSequence; separate child streams per configuration and method)
Users per trial: 1,000
Trials per configuration: 1,000

Each raw file is whitespace-separated, one trial per row.
PDRF files have 10 integer columns:
1 underallocated by 1 task
2 underallocated by 2 tasks
3 underallocated by >2 tasks
4 maximum underallocation (tasks/user)
5 total underallocated users
6 overallocated by 1 task
7 overallocated by 2 tasks
8 overallocated by >2 tasks
9 maximum overallocation (tasks/user)
10 total overallocated users

Heuristic raw files have an additional 11th column:
11 indicator (0/1) that heuristic's final resource consumption exceeded DRF's in every resource.

Configurations are encoded in filenames:
results_<users>_<resources>_<reserve-low>_<reserve-high>_<demand-low>_<demand-high>
The reserve and demand bounds are inclusive, matching the corrected rerun script.
