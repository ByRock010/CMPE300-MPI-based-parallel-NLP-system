#!/bin/bash
# Comprehensive test script for all patterns with all testcases

TESTCASES_DIR="testcases"
SOLUTION="solution.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track test results
PASSED=0
FAILED=0

run_test() {
    local pattern=$1
    local processes=$2
    local testcase=$3
    local text_file="${TESTCASES_DIR}/text_${testcase}.txt"
    local vocab_file="${TESTCASES_DIR}/vocab_${testcase}.txt"
    local stopwords_file="${TESTCASES_DIR}/stopwords_${testcase}.txt"

    echo -e "${YELLOW}Testing Pattern #${pattern} with testcase ${testcase} (${processes} processes)${NC}"

    if mpiexec -n ${processes} python3 ${SOLUTION} \
        --text ${text_file} \
        --vocab ${vocab_file} \
        --stopwords ${stopwords_file} \
        --pattern ${pattern} 2>&1; then
        echo -e "${GREEN}[PASSED]${NC} Pattern #${pattern} - Testcase ${testcase}"
        ((PASSED++))
    else
        echo -e "${RED}[FAILED]${NC} Pattern #${pattern} - Testcase ${testcase}"
        ((FAILED++))
    fi
    echo ""
}

echo "=========================================="
echo "  MPI NLP System - Full Test Suite"
echo "=========================================="
echo ""

# Test all 5 testcases with all 4 patterns
for testcase in 1 2 3 4 5; do
    echo "=========================================="
    echo "  Testcase ${testcase}"
    echo "=========================================="
    echo ""

    # Pattern 1: Requires at least 2 processes (1 manager + workers)
    # Using 4 workers for good parallelism
    run_test 1 5 ${testcase}

    # Pattern 2: Requires exactly 5 processes
    run_test 2 5 ${testcase}

    # Pattern 3: Requires 1 + 4*k processes (k >= 1)
    # Using 5 processes (1 manager + 1 pipeline of 4 workers)
    run_test 3 5 ${testcase}

    # Pattern 4: Requires 1 + 2*k processes (k >= 1)
    # Using 5 processes (1 manager + 2 pairs of workers)
    run_test 4 5 ${testcase}
done

# Also run with small testcase
echo "=========================================="
echo "  Small Testcase (quick validation)"
echo "=========================================="
echo ""

for pattern in 1 2 3 4; do
    if [ ${pattern} -eq 2 ]; then
        processes=5
    elif [ ${pattern} -eq 3 ]; then
        processes=5
    else
        processes=3
    fi

    echo -e "${YELLOW}Testing Pattern #${pattern} with small testcase (${processes} processes)${NC}"

    if mpiexec -n ${processes} python3 ${SOLUTION} \
        --text ${TESTCASES_DIR}/small_text.txt \
        --vocab ${TESTCASES_DIR}/small_vocab.txt \
        --stopwords ${TESTCASES_DIR}/small_stopwords.txt \
        --pattern ${pattern} 2>&1; then
        echo -e "${GREEN}[PASSED]${NC} Pattern #${pattern} - Small testcase"
        ((PASSED++))
    else
        echo -e "${RED}[FAILED]${NC} Pattern #${pattern} - Small testcase"
        ((FAILED++))
    fi
    echo ""
done

# Summary
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
TOTAL=$((PASSED + FAILED))
echo "Total:  ${TOTAL}"
echo ""

if [ ${FAILED} -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
