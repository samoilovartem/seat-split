#! /bin/sh
cd .. && tree -a -L 2 -I 'venv|__pycache__|.git|.DS_Store|.idea|htmlcov|instruction_files|*.pyc|*.pyo|.pytest_cache' --filelimit=20
echo 'Done!'
