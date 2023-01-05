#! /bin/sh
set -e

NC='\033[0m'
GREEN='\033[0;32m'

docker build -t registry.heroku.com/django-docker/web .
echo -e "${GREEN}Docker image has been successfully built${NC}"

docker push registry.heroku.com/django-docker/web
echo -e "${GREEN}Docker image has been successfully pushed to registry.heroku.com${NC}"

heroku container:release -a django-docker web
echo -e "${GREEN}Docker container has been successfully launched${NC}"