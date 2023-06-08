#! /bin/sh

NC='\033[0m'
GREEN='\033[0;32m'

if test "$1" = "precommit"; then
  number=4
  docker_flags=""
else
  echo "Type only number:
  1. Run coverage tests, provide report
  2. Run coverage tests, provide report and save it as HTML
  3. Run standard Django tests
  4. Run standard Django tests in parallel"

  # shellcheck disable=SC2162
  read number
  docker_flags="-it"
fi

if test "$number" -eq 1
  then
    docker exec $docker_flags django bash -c "coverage run manage.py test -v 2 && coverage report"
elif test "$number" -eq 2
  then
    docker exec $docker_flags django bash -c "coverage run manage.py test -v 2 && coverage report && coverage html"
elif test "$number" -eq 3
  then
    docker exec $docker_flags django bash -c "python manage.py test"
elif test "$number" -eq 4
  then
    docker exec $docker_flags django bash -c "python manage.py test --parallel"
else
    echo "${GREEN}Wrong input. Please try again${NC}"
fi
