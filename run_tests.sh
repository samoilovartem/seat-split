#! /bin/sh

echo "Type only number:
1. Run coverage tests, provide report
2. Run coverage tests, provide report and save it as HTML
3. Run standard Django tests
4. Run standard Django tests in parallel"

# shellcheck disable=SC2162
read number

if [ "$number" -eq 1 ]
  then
    coverage run manage.py test -v 2 && coverage report
elif [ "$number" -eq 2 ]
  then
    coverage run manage.py test -v 2 && coverage report && coverage html
elif [ "$number" -eq 3 ]
  then
    python manage.py test
elif [ "$number" -eq 4 ]
  then
    python manage.py test --parallel
else
    echo "Wrong input. Please try again"
fi

