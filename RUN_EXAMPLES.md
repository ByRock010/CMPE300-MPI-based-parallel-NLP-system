# How to Run solution.py - Command Examples

This document provides examples of how to run `solution.py` with different patterns and testcases.

## Prerequisites

Make sure you have:
1. MPI installed (OpenMPI or MS-MPI)
2. mpi4py installed in your conda environment
3. Activated your conda environment (if using one)

## General Command Format

```bash
mpiexec -n <num_processes> python3 solution.py --text <text_file> --vocab <vocab_file> --stopwords <stopwords_file> --pattern <1|2|3|4>
```

## Pattern Requirements

- **Pattern #1**: `-n >= 2` (1 manager + at least 1 worker)
- **Pattern #2**: `-n = 5` (exactly 5 processes)
- **Pattern #3**: `-n = 1 + 4i` where `i >= 1` (e.g., 5, 9, 13, 17, ...)
- **Pattern #4**: `-n = 1 + 2i` where `i >= 1` (e.g., 3, 5, 7, 9, ...)

---

## Examples with Small Testcase

### Pattern #1 (with 3 processes: 1 manager + 2 workers)

```bash
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 1
```

### Pattern #2 (requires exactly 5 processes)

```bash
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2
```

### Pattern #3 (with 5 processes: 1 manager + 4 workers = 1 pipeline)

```bash
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3
```

### Pattern #3 (with 9 processes: 1 manager + 8 workers = 2 pipelines)

```bash
mpiexec -n 9 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3
```

### Pattern #4 (with 3 processes: 1 manager + 2 workers = 1 pair)

```bash
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
```

### Pattern #4 (with 5 processes: 1 manager + 4 workers = 2 pairs)

```bash
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
```

---

## Examples with Testcase 1

### Pattern #1 (with 3 processes)

```bash
mpiexec -n 3 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 1
```

### Pattern #1 (with 5 processes for better parallelization)

```bash
mpiexec -n 5 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 1
```

### Pattern #2 (exactly 5 processes)

```bash
mpiexec -n 5 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 2
```

### Pattern #3 (with 9 processes = 2 pipelines)

```bash
mpiexec -n 9 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 3
```

### Pattern #4 (with 5 processes = 2 pairs)

```bash
mpiexec -n 5 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 4
```

---

## Examples with Testcase 2

### Pattern #1 (with 4 processes)

```bash
mpiexec -n 4 python3 solution.py --text testcases/text_2.txt --vocab testcases/vocab_2.txt --stopwords testcases/stopwords_2.txt --pattern 1
```

### Pattern #2

```bash
mpiexec -n 5 python3 solution.py --text testcases/text_2.txt --vocab testcases/vocab_2.txt --stopwords testcases/stopwords_2.txt --pattern 2
```

### Pattern #3 (with 13 processes = 3 pipelines)

```bash
mpiexec -n 13 python3 solution.py --text testcases/text_2.txt --vocab testcases/vocab_2.txt --stopwords testcases/stopwords_2.txt --pattern 3
```

### Pattern #4 (with 7 processes = 3 pairs)

```bash
mpiexec -n 7 python3 solution.py --text testcases/text_2.txt --vocab testcases/vocab_2.txt --stopwords testcases/stopwords_2.txt --pattern 4
```

---

## Examples with Testcase 3

```bash
# Pattern #1
mpiexec -n 3 python3 solution.py --text testcases/text_3.txt --vocab testcases/vocab_3.txt --stopwords testcases/stopwords_3.txt --pattern 1

# Pattern #2
mpiexec -n 5 python3 solution.py --text testcases/text_3.txt --vocab testcases/vocab_3.txt --stopwords testcases/stopwords_3.txt --pattern 2

# Pattern #3 (with 9 processes)
mpiexec -n 9 python3 solution.py --text testcases/text_3.txt --vocab testcases/vocab_3.txt --stopwords testcases/stopwords_3.txt --pattern 3

# Pattern #4 (with 5 processes)
mpiexec -n 5 python3 solution.py --text testcases/text_3.txt --vocab testcases/vocab_3.txt --stopwords testcases/stopwords_3.txt --pattern 4
```

---

## Examples with Testcase 4

```bash
# Pattern #1
mpiexec -n 4 python3 solution.py --text testcases/text_4.txt --vocab testcases/vocab_4.txt --stopwords testcases/stopwords_4.txt --pattern 1

# Pattern #2
mpiexec -n 5 python3 solution.py --text testcases/text_4.txt --vocab testcases/vocab_4.txt --stopwords testcases/stopwords_4.txt --pattern 2

# Pattern #3 (with 13 processes)
mpiexec -n 13 python3 solution.py --text testcases/text_4.txt --vocab testcases/vocab_4.txt --stopwords testcases/stopwords_4.txt --pattern 3

# Pattern #4 (with 7 processes)
mpiexec -n 7 python3 solution.py --text testcases/text_4.txt --vocab testcases/vocab_4.txt --stopwords testcases/stopwords_4.txt --pattern 4
```

---

## Examples with Testcase 5

```bash
# Pattern #1
mpiexec -n 5 python3 solution.py --text testcases/text_5.txt --vocab testcases/vocab_5.txt --stopwords testcases/stopwords_5.txt --pattern 1

# Pattern #2
mpiexec -n 5 python3 solution.py --text testcases/text_5.txt --vocab testcases/vocab_5.txt --stopwords testcases/stopwords_5.txt --pattern 2

# Pattern #3 (with 17 processes = 4 pipelines)
mpiexec -n 17 python3 solution.py --text testcases/text_5.txt --vocab testcases/vocab_5.txt --stopwords testcases/stopwords_5.txt --pattern 3

# Pattern #4 (with 9 processes = 4 pairs)
mpiexec -n 9 python3 solution.py --text testcases/text_5.txt --vocab testcases/vocab_5.txt --stopwords testcases/stopwords_5.txt --pattern 4
```

---

## Quick Test Commands

### Test all patterns with small testcase:

```bash
# Pattern 1
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 1

# Pattern 2
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2

# Pattern 3
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3

# Pattern 4
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
```

---

## Invalid Cases (Error Handling Examples)

These examples demonstrate error handling when invalid `-n` values are used. The program should print an error message and exit cleanly without hanging.

### Pattern #1 - Invalid: Too Few Processes

```bash
# Pattern #1 requires at least 2 processes, but using only 1
mpiexec -n 1 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 1
# Expected: "Error: Pattern #1 requires at least 2 processes (1 manager + 1 worker)"
```

### Pattern #2 - Invalid: Wrong Number of Processes

```bash
# Pattern #2 requires exactly 5 processes, but using 3
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2
# Expected: "Error: Pattern #2 requires exactly 5 processes, got 3"

# Pattern #2 with 7 processes (also invalid)
mpiexec -n 7 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2
# Expected: "Error: Pattern #2 requires exactly 5 processes, got 7"
```

### Pattern #3 - Invalid: Not in Form 1+4i

```bash
# Pattern #3 requires size = 1 + 4i (5, 9, 13, 17, ...), but using 6
mpiexec -n 6 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3
# Expected: "Error: Pattern #3 requires size = 1 + 4i (i >= 1), got 6"

# Pattern #3 with 2 processes (too few and wrong form)
mpiexec -n 2 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3
# Expected: "Error: Pattern #3 requires size = 1 + 4i (i >= 1), got 2"

# Pattern #3 with 10 processes (not in form 1+4i)
mpiexec -n 10 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3
# Expected: "Error: Pattern #3 requires size = 1 + 4i (i >= 1), got 10"
```

### Pattern #4 - Invalid: Not in Form 1+2i

```bash
# Pattern #4 requires size = 1 + 2i (3, 5, 7, 9, ...), but using 4
mpiexec -n 4 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
# Expected: "Error: Pattern #4 requires size = 1 + 2i (i >= 1), got 4"

# Pattern #4 with 2 processes (too few and wrong form)
mpiexec -n 2 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
# Expected: "Error: Pattern #4 requires size = 1 + 2i (i >= 1), got 2"

# Pattern #4 with 6 processes (not in form 1+2i)
mpiexec -n 6 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4
# Expected: "Error: Pattern #4 requires size = 1 + 2i (i >= 1), got 6"
```

### Testing Error Handling with Larger Testcases

```bash
# Pattern #2 with wrong process count using testcase 1
mpiexec -n 3 python3 solution.py --text testcases/text_1.txt --vocab testcases/vocab_1.txt --stopwords testcases/stopwords_1.txt --pattern 2
# Expected: Error message and clean exit

# Pattern #3 with invalid process count using testcase 2
mpiexec -n 7 python3 solution.py --text testcases/text_2.txt --vocab testcases/vocab_2.txt --stopwords testcases/stopwords_2.txt --pattern 3
# Expected: Error message and clean exit
```

**Note**: All invalid cases should exit cleanly without hanging. If the program hangs, it indicates a deadlock issue that needs to be fixed.

---

## Notes

- Make sure you're in the project directory when running these commands
- If using a conda environment, activate it first: `conda activate mpi_nlp`
- On macOS, you might need to use `python3` instead of `python`
- The output will show the Term-Frequency (TF) results, and for Pattern #4, also Document-Frequency (DF) results
- If you get an error about process count, check that you're using the correct `-n` value for the pattern
- **Invalid cases should exit cleanly** - if they hang, there's a deadlock issue that needs to be fixed

