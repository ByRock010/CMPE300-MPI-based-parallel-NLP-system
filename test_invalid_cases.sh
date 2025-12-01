#!/bin/bash
# Test script for invalid cases - should exit cleanly without hanging

echo "=========================================="
echo "Testing Invalid Cases (Error Handling)"
echo "=========================================="
echo ""
echo "These should all print error messages and exit cleanly."
echo "If any command hangs, there's a deadlock issue!"
echo ""

echo "Test 1: Pattern #1 with -n 1 (too few processes)"
echo "Expected: Error message"
timeout 5 mpiexec -n 1 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 1 2>&1 || echo "Command completed or timed out"
echo ""

echo "Test 2: Pattern #2 with -n 3 (wrong number, should be 5)"
echo "Expected: Error message"
timeout 5 mpiexec -n 3 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 2 2>&1 || echo "Command completed or timed out"
echo ""

echo "Test 3: Pattern #3 with -n 6 (not in form 1+4i)"
echo "Expected: Error message"
timeout 5 mpiexec -n 6 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3 2>&1 || echo "Command completed or timed out"
echo ""

echo "Test 4: Pattern #4 with -n 4 (not in form 1+2i)"
echo "Expected: Error message"
timeout 5 mpiexec -n 4 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4 2>&1 || echo "Command completed or timed out"
echo ""

echo "Test 5: Pattern #3 with -n 2 (too few and wrong form)"
echo "Expected: Error message"
timeout 5 mpiexec -n 2 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 3 2>&1 || echo "Command completed or timed out"
echo ""

echo "Test 6: Pattern #4 with -n 2 (too few and wrong form)"
echo "Expected: Error message"
timeout 5 mpiexec -n 2 python3 solution.py --text testcases/small_text.txt --vocab testcases/small_vocab.txt --stopwords testcases/small_stopwords.txt --pattern 4 2>&1 || echo "Command completed or timed out"
echo ""

echo "=========================================="
echo "Invalid case tests completed!"
echo "=========================================="
echo ""
echo "If any test hung (didn't complete within 5 seconds),"
echo "there's a deadlock issue that needs to be fixed."

