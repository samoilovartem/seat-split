# Indicating what image of Python it will be using (it will download it if doesn't have locally)
FROM python:3.11

#ENV APPDIR=/home/src
#ENV PYTHONPATH=$PYTHONPATH:$APPDIR
#
#RUN mkdir -p $APPDIR
#
#RUN apt-get update && \
#    apt-get install gcc g++ make libffi-dev libssl-dev postgresql-client iputils-ping -y && mkdir -p $APPDIR

#WORKDIR $APPDIR



# Indicating working directory
WORKDIR /usr/src/app

#COPY ./em $APPDIR/em
#COPY ./manage.py $APPDIR/
#COPY ./requirements.txt $APPDIR/
COPY requirements.txt requirements.txt

# Running commands that we might need. Example:
RUN pip3 install -r requirements.txt

# Copying everything from current directory to current directory in docker container
COPY . .

# Access to our env (if ever we need to get some data from there)
#ENV TZ Europe/Moscow



# RUN #pip install -r $APPDIR/requirements.txt --upgrade && rm $APPDIR/requirements.txt

#EXPOSE 8000

#CMD /usr/local/bin/gunicorn -b 0.0.0.0:8000 -w 3 --reload --access-logfile - em.wsgi:application --timeout 600

# Indicates what to run in container
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]



