#! /bin/sh

NC='\033[0m'
GREEN='\033[0;32m'

echo "Type only number:
1. Create dev-requirements.txt
2. Create prod-requirements.txt
3. Update dependencies
"

# shellcheck disable=SC2162
read number

cd .. && cd django-backend || exit

if test "$number" -eq 1
  then
    poetry export -f requirements.txt --output dev-requirements.txt --without-hashes --with dev
elif test "$number" -eq 2
  then
    poetry export -f requirements.txt --output prod-requirements.txt
elif test "$number" -eq 3
  then
    poetry update
else
    echo "${GREEN}Wrong input. Please try again${NC}"
fi
