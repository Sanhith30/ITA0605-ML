ITA06 – MACHINE LEARNING | ASSIGNMENT 5 – CO5
================================================

PACKAGE CONTENTS
----------------
Final_Assignment_5_CO5.docx    Full editable academic report (Q1–Q7),
                               complete source-code appendix, executed data
                               and performance results, 26 tables and 10 figures.
Programs/                      Seven complete Python question programs,
                               plus shared module common.py.
Datasets/                      NumPy arrays, CSV, JSON, reference machine
                               information, changed-input experiment, and
                               March/April partitions.
Outputs/                       Actual program console logs, JSON results,
                               raw calculation and tabulation outputs.
Graphs/                        Seven Q5 plots, Q6 pipeline plots, Q7 analysis.
Diagrams/                      The Q7 redesign workflow diagram.
Original_Assignment_Questions.txt   Full uploaded question text.
requirements.txt               Third-party Python packages.
run_all.py                     One-command experiment runner.
verify_results.py              Cross-file and reproducibility assertions.

HOW TO RUN ON WINDOWS OR LINUX
------------------------------
1. Extract the ZIP into a normal folder.
2. Open a terminal in the extracted Assignment_5_Submission folder.
3. Ensure Python 3.10+ is installed.
4. Optional: create a virtual environment:
   Windows:  py -m venv .venv && .venv\Scripts\activate
   Linux/Mac: python3 -m venv .venv && source .venv/bin/activate
5. Install the dependencies: python -m pip install -r requirements.txt
6. Execute ALL questions: python run_all.py
7. Check the deliverables: python verify_results.py
8. Open Final_Assignment_5_CO5.docx in Microsoft Word.

DEPENDENCY ORDER / INDIVIDUAL PROGRAMS
--------------------------------------
python Programs/Q1_numpy_sensor_arrays.py
python Programs/Q2_numpy_statistics_io.py
python Programs/Q3_pandas_cleaning.py
python Programs/Q4_pandas_combine_group.py
python Programs/Q5_pandas_plots.py
python Programs/Q6_reproducible_pipeline.py
python Programs/Q7_redesign_validation.py

Q3 must precede Q4–Q7 because it creates the 1,000-record production
file; Q4 must precede Q6 because it creates Machine_Info.csv.

SEEDS, DATA AND EXPERIMENTAL RULES
---------------------------------
Q1: Generator seed 20260501; 4 machines x 5 days; Gaussian error SD=0.5.
Q2: Generator seed 20260502; 50 machines x 30 days; seven injected extremes
    at fixed zero-based coordinates; global |z| > 3; per-machine median fill.
Q3: Generator seed 20260503; 1,000 distinct machine/date/shift readings,
    12 exact duplicates appended, 30 missing production outputs, 24 missing
    defect counts, and 35 lowercase line entries before appending duplicates.
    After duplicate removal and imputation exactly 1,000 records remain.
Q4: Machine metadata seed 20260504. Production machine M13 is missing from
    the metadata table; metadata-only M14 has no production rows.
Q5–Q7: Consume the cleaned Q3 production file. Q6/Q7 use 100,000 repeated
    production rows for paired computation and memory benchmarks.

The Q3 full raw CSV and JSON round-trips are asserted bit-for-bit, including
parsed dates and dtypes. Q2 binary and 17-digit CSV floating-point round-trips
are tested for exact array equality and dtype preservation.

PRACTICAL LIMITATIONS
---------------------
All timing values in the Word report were measured from actual execution in
one environment. Rerunning on another computer will produce different runtimes
while preserving the intended numerical results. The large production records
are reproducibly generated for these experimental questions; they are not
claimed to be live operational records from any organisation.

The cover page does not invent a student name, register number or faculty name.

ACKNOWLEDGMENT
--------------
OpenAI ChatGPT assisted with preparing code and report prose. Executed
outputs, assertions and plots were produced by the included Python programs.
