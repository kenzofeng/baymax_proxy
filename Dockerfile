FROM node:10 as BuildNode
COPY . /tmp/
RUN cd /tmp/baymaxfront \
    && npm install \
    && npm run build

FROM python:3.6 as Runtime
WORKDIR /usr/local/application/
COPY . /usr/local/application/
COPY --from=BuildNode /tmp/baymaxfront /usr/local/application/baymaxfront
RUN mkdir -p /usr/local/data/
RUN mkdir -p project/log
RUN mkdir -p project/report
RUN mkdir -p project/test_automation
RUN mkdir -p project/tmp
RUN pip install pipenv
RUN pipenv install --skip-lock
RUN pipenv run python manage.py makemigrations
RUN pipenv run python manage.py migrate
CMD ["pipenv", "run", "python", "manage.py" ,"runserver" ,"0.0.0.0:8000", "--insecure"]