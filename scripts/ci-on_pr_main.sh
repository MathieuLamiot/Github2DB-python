echo "Starting CI on-pr-main (ci-on_pr_main.sh)..."

echo "ci-on_pr_main: starting linting..."
chmod +x ./scripts/lint.sh
LINT_ERROR_LIST=$(./scripts/lint.sh)
if [[ $? -eq 0 ]]; then
    echo "ci-on_pr_main: Linting OK"
else 
    echo "ci-on_pr_main: Linting failed. See the results:"
    echo "$LINT_ERROR_LIST"
    exit 1
fi

echo "ci-on_pr_main: starting testing..."
chmod +x ./scripts/tests.sh
TESTS_ERRORS=$(./scripts/tests.sh)
if [[ $? -eq 0 ]]; then
    echo "ci-on_pr_main: Tests OK"
else 
    echo "ci-on_pr_main: Tests failed. See the results:"
    echo "$TESTS_ERRORS"
    exit 1
fi

echo "ci-on_pr_main: Done."
exit 0