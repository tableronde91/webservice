FROM debian:latest

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install curl -y
RUN apt-get install apache2 -y

RUN apt-get install libapache2-mod-wsgi-py3 -y
RUN a2enmod wsgi

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install default-libmysqlclient-dev -y

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY app.conf /etc/apache2/sites-available/
COPY ./FlaskApp /var/www/FlaskApp

RUN a2ensite app

RUN service apache2 start

EXPOSE 80 443

RUN apt-get clean

ENTRYPOINT ["/bin/bash", "/usr/sbin/apache2ctl", "-D", "FOREGROUND"]