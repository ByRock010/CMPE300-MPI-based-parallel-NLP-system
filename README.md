# CMPE 300 Project 2: MPI-Based Parallel NLP System

This project implements four MPI communication patterns for parallel natural language processing.

## Setup

### Using Conda Environment

1. Create a conda environment:
```bash
conda create -n mpi_nlp python=3.9
conda activate mpi_nlp
```

2. Install mpi4py:
```bash
conda install -c conda-forge mpi4py
```

Alternatively, if you have MPI installed separately:
```bash
pip install mpi4py
```

3. Verify installation:
```bash
mpiexec -n 2 python -c "from mpi4py import MPI; print('MPI works!')"
```

## Project Structure

- `solution.py` - Main implementation with all 4 patterns
- `test_operations.py` - Test script to verify NLP operations work correctly
- `resources/` - Sample input files
- `testcases/` - Test case files for the project

## NLP Operations

The following operations are implemented:

1. **Lowercasing**: Converts all characters to lowercase
2. **Punctuation Removal**: Removes all punctuation symbols
3. **Stopword Removal**: Eliminates common stopwords
4. **Term-Frequency (TF) Counting**: Counts word occurrences across all sentences
5. **Document-Frequency (DF) Counting**: Counts in how many distinct sentences each word appears

## Patterns

### Pattern #1: Parallel End-to-End Processing in Worker Processes
- Manager divides text into balanced chunks
- Each worker performs preprocessing and TF counting
- Workers return partial TF results to manager
- **Process requirement**: `-n >= 2` (1 manager + at least 1 worker)

### Pattern #2: Linear Pipeline
- Each worker performs exactly one stage of the pipeline
- Data flows sequentially through stages
- **Process requirement**: `-n = 5` (1 manager + 4 workers)

### Pattern #3: Parallel Pipelines (Multiple Independent Pipelines)
- Multiple independent linear pipelines operate simultaneously
- Each pipeline has 4 stages
- **Process requirement**: `-n = 1 + 4i` where `i >= 1` (e.g., 5, 9, 13, ...)

### Pattern #4: End-to-End Processing with Task Parallelism
- Workers perform preprocessing, then exchange data in pairs
- Even-ranked workers compute DF, odd-ranked workers compute TF
- **Process requirement**: `-n = 1 + 2i` where `i >= 1` (e.g., 3, 5, 7, ...)

## Usage

### Testing Operations

First, test that the NLP operations work correctly:

```bash
python3 test_operations.py
```

### Running the Solution

Run the solution with MPI:

```bash
mpiexec -n <num_processes> python3 solution.py --text <text_file> --vocab <vocab_file> --stopwords <stopwords_file> --pattern <1|2|3|4>
```

### Example Commands

**Pattern #1** (with 3 processes):
```bash
mpiexec -n 3 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 1
```

**Pattern #2** (requires exactly 5 processes):
```bash
mpiexec -n 5 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 2
```

**Pattern #3** (with 9 processes = 1 + 4*2):
```bash
mpiexec -n 9 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 3
```

**Pattern #4** (with 5 processes = 1 + 2*2):
```bash
mpiexec -n 5 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 4
```

## Implementation Details

- Uses only `MPI_Send` and `MPI_Recv` for point-to-point communication
- No collective operations or non-blocking communication
- Rank 0 is always the manager process
- All patterns handle chunking appropriately to enable parallel processing

## Notes

- The program validates process counts for each pattern
- Sentences are never split across chunks
- Chunk sizes are balanced to distribute work evenly
- Pattern #4 uses asymmetric communication to avoid deadlocks (even ranks send first, odd ranks receive first)

