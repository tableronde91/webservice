FROM debian:latest

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./client.py /var/www/client.py
COPY ./serv.py /var/www/serv.py

ENTRYPOINT ["/bin/python3", "/var/www/serv.py", "-D", "FOREGROUND"]