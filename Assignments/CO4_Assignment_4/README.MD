ITA06 — MACHINE LEARNING
ASSIGNMENT 4 — CO4 | COMPLETE PROJECT SUBMISSION
================================================

OVERVIEW
--------
This project answers Q1 through Q7 of the supplied 50-mark assignment.
It includes an editable 17-page Word report, seven individually executable
experiments, a run-all script, datasets, program execution logs, raw CSV/JSON
results, charts, Voronoi cells, RBF boundaries, and workflow diagrams.

FILES AND FOLDERS
-----------------
Final_Assignment.docx         Editable assignment with calculations, results,
                              analysis, tables, program references and visuals
Programs/common.py           Shared deterministic data and evaluation functions
Programs/q1_knn.py           Scratch k-NN, distance tables and Voronoi cells
Programs/q2_scaling.py       k selection, feature scaling, weights, dimensions
Programs/q3_lwr.py           Manual calculation and scratch local regression
Programs/q4_rbf.py           XOR least-squares and crescent RBF network
Programs/q5_cbr.py           Case retrieval, weight sensitivity and retention
Programs/q6_cost_noise.py    Learning costs, noise, and tree index experiments
Programs/q7_redesign.py      Training-only feature-selection redesign
Programs/run_all.py          Execute all questions sequentially
Datasets/                    CSV inputs, labels and partition indicators
Results/                     Full numeric results and configurations (CSV/JSON)
Graphs/                      Figures produced by the executed experiments
Diagrams/                    Explanatory algorithm/process schematics
Outputs/                     Actual console outputs for each executed program
requirements.txt             Python package dependencies

HOW TO RUN
----------
1. Use Python 3.10 or higher.
2. In this project root, install dependencies with:
       python -m pip install -r requirements.txt
3. Change to the Programs folder:
       cd Programs
4. Run all seven questions:
       python run_all.py
5. Or run an individual program:
       python q1_knn.py
       python q2_scaling.py
       python q3_lwr.py
       python q4_rbf.py
       python q5_cbr.py
       python q6_cost_noise.py
       python q7_redesign.py
6. The current CSV/JSON figures and logs were produced by actual program
   execution and are supplied in the package.

REPRODUCIBILITY
---------------
* Q1: eight original machine observations; full distance rankings for both
  Euclidean and Manhattan distances; nearest-neighbour predictions checked
  against scikit-learn.
* Q2: independent 1,000-row datasets for seeds 17, 29 and 41. Seed 17 is
  saved as Datasets/q2_1000.csv. Splits are stratified 600 train / 200
  validation / 200 test. Fixed k candidates: 1, 3, 5, 7, 9, 15, 25.
* Q2 final configuration: standardisation fitted on training data, k=15,
  inverse-square distance voting (1/max(distance,1e-12)^2); final test
  accuracy 0.905. No tuning on test rows.
* Q3: 100 nonlinear points, random seed 73; 75 train / 25 validation.
  Manual weighted least-squares solution saved as Results/q3_manual.json.
* Q4: 1,000 two-crescent points, seed 71; stratified 600/200/200 partition;
  k-means trains on the training split only. 2/5/10/20/50 centres and
  0.35/0.75/1.5 nearest-centre-distance width multipliers.
* Q5: exact six provided cases; C7 is a conditional example of how a case
  could be retained following technician confirmation, not evidence that
  any physical maintenance has occurred.
* Q6: seeds 17/29/41, train sizes 200/500/1000/2000/5000. The additional
  records come from the same Q2 generator; the original held-out Q2 records
  never enter training. All times are local wall-clock measurements and
  may differ on another machine.
* Q7: uses the same Q2 splits and seeds and holds the k-NN settings fixed.
  Baseline uses 22 inputs; redesigned model uses top two training-ranked
  mutual-information inputs, with no test leakage.

RESULT HIGHLIGHTS
-----------------
Q1: (3,3) classified Worn for Euclidean k=1,3,5 and Manhattan k=3.
Q2: scaled validation 0.925 at k=15 vs unscaled 0.745; held-out 0.905.
Q3: hand-worked LWR(3.5,tau=1) = 3.5953457208 vs global line 3.67.
Q4: XOR outputs 0,1,1,0; RBF test 0.94 vs reused k-NN recipe 0.935.
Q5: C3 best match (similarity 0.70), and weighting changes neighbour order.
Q6: low-dimensional tree index speeds k-NN; 52D tree search is slower.
Q7: mean validation 0.7383 -> 0.9383 using top-two feature filtering.

DEPENDENCIES
------------
See requirements.txt. The implemented experiments use numpy, pandas,
scipy, scikit-learn and matplotlib; the Word report was created with
python-docx. No specialised hardware or paid software is necessary.

AI / EXTERNAL ASSISTANCE ACKNOWLEDGMENT
--------------------------------------
AI assistance was used to prepare and review the explanations, code,
figures, and report. All reported numeric results were obtained by
executing the included programs. Sources and implementation choices are
noted in the Word report. Users should understand and be able to explain
all manual calculations, model choices and validation steps.
