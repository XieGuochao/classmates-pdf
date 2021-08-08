FROM python:3.8

ADD ttf /ttf
ADD src /src
ADD run.sh /run.sh

RUN ["python3", "-m", "pip", "install", "-r", "/src/requirements.txt"]

ENTRYPOINT [ "/run.sh" ]