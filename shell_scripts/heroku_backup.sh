#! /bin/sh

NC='\033[0m'
GREEN='\033[0;32m'

echo "Choose what you want to do:
1. Check Backup Status and Info
2. Get more details about a given backup
3. Download all available backups
4. Download a backup via URL
5. Create a Manual Backup
6. Cancel Manual Backup Creation
7. Set Up a Backup Schedule (07:00 Manila)
8. Stop Scheduled Backups
9. View Backup Schedules
10. Restore a backup
11. Delete a Backup
"

# shellcheck disable=SC2162
read number

cd ..

if test "$number" -eq 1
  then
    heroku pg:backups --app django-docker
elif test "$number" -eq 2
  then
    echo "${GREEN}Please send a correct backup ID${NC}"
    read -r backup_id
    heroku pg:backups:info "$backup_id" --app django-docker
elif test "$number" -eq 3
  then
    heroku pg:backups:download --app django-docker
elif test "$number" -eq 4
  then
    echo "${GREEN}Please send a correct backup ID${NC}"
    read -r backup_id
    heroku pg:backups:url "$backup_id" --app django-docker
elif test "$number" -eq 5
  then
    heroku pg:backups:capture --app django-docker
elif test "$number" -eq 6
  then
    heroku pg:backups:cancel
elif test "$number" -eq 7
  then
    heroku pg:backups:schedule DATABASE_URL --at '07:00 Asia/Manila' --app django-docker
elif test "$number" -eq 8
  then
    heroku pg:backups:unschedule DATABASE_URL --app django-docker
elif test "$number" -eq 9
  then
    heroku pg:backups:schedules --app django-docker
elif test "$number" -eq 10
  then
    echo "${GREEN}Please send a correct backup ID${NC}"
    read -r backup_id
    echo "${GREEN}Are you sure you want to proceed? (yes/no)${NC}"
    read -r answer
    if test "$answer" = "yes"
      then
        heroku pg:backups:restore "$backup_id" DATABASE_URL --app django-docker
    else
        echo "${GREEN}The transaction is cancelled${NC}"
    fi
elif test "$number" -eq 11
  then
    echo "${GREEN}Please send a correct backup ID${NC}"
    read -r backup_id
    echo "${GREEN}Are you sure you want to delete backup ${backup_id}? (yes/no)${NC}"
    read -r answer
    if test "$answer" = "yes"
      then
        heroku pg:backups:delete "$backup_id" --app django-docker
    else
        echo "${GREEN}The transaction is cancelled${NC}"
    fi
else
    echo "${GREEN}Wrong input. Please try again${NC}"
fi
