FROM python:3.6.5

COPY requirements /home/slogansvc/requirements
WORKDIR /home/slogansvc
RUN ls -la
RUN pip install -r ./requirements/requirements.txt
COPY . /home/slogansvc

EXPOSE 5000

ENTRYPOINT ["uwsgi", "--ini", "app.ini"]

