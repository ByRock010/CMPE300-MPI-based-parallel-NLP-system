#!/bin/bash
# Quick test script for all patterns with small testcase

echo "=========================================="
echo "Testing Pattern #1 (3 processes)"
echo "=========================================="
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 1

echo ""
echo "=========================================="
echo "Testing Pattern #2 (5 processes)"
echo "=========================================="
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2

echo ""
echo "=========================================="
echo "Testing Pattern #3 (5 processes)"
echo "=========================================="
mpiexec -n 5 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3

echo ""
echo "=========================================="
echo "Testing Pattern #4 (3 processes)"
echo "=========================================="
mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4

echo ""
echo "=========================================="
echo "All tests completed!"
echo "=========================================="

