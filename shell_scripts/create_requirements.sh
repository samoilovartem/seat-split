#! /bin/sh

NC='\033[0m'
GREEN='\033[0;32m'

echo "Type only number:
1. Create dev-requirements.txt
2. Create prod-requirements.txt
3. Update both
"

# shellcheck disable=SC2162
read number

cd ..

if [ "$number" -eq 1 ]
  then
    pip-compile --extra dev -o dev-requirements.txt pyproject.toml
elif [ "$number" -eq 2 ]
  then
    pip-compile -o prod-requirements.txt pyproject.toml
elif [ "$number" -eq 3 ]
  then
    pip-compile -o prod-requirements.txt pyproject.toml
    pip-compile --extra dev -o dev-requirements.txt pyproject.toml
else
    echo "${GREEN}Wrong input. Please try again${NC}"
fi
