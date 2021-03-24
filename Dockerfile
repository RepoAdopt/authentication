FROM python:3

WORKDIR /opt/GraphQL

COPY main.py ./
COPY requirements.txt ./
#TODO ENABLE WHEN THE FOLDER EXISTS
#COPY lib ./lib/

RUN pip install -r ./requirements.txt

CMD ["python", "./main.py"]