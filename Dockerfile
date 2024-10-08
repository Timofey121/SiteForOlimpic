FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/req.txt

# XVFB
RUN apt-get update && apt-get install -y xvfb

# CHROME + POSTQRESQL + ngnix
RUN apt-get update && apt-get install -y wget gnupg2 unzip netcat-traditional nginx -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN LATEST=`wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/

RUN pip install --upgrade pip
RUN pip install -r /usr/src/requirements.txt

COPY . .


# docker rmi siteforolimpic_worker siteforolimpic_beat siteforolimpic_webapp siteforolimpic_nginx siteforolimpic_web