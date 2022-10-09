FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "===> Installing system dependencies.." && \
apt-get update && apt-get install --no-install-recommends -y python3 python3-pip wget libxtst6 fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 $BUILD_DEPS xvfb curl vim && \
\
echo "===> Installing geckodriver.." && \
wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz && \
tar -zxf geckodriver-v0.31.0-linux64.tar.gz -C /usr/local/bin && \
chmod +x /usr/local/bin/geckodriver && \
rm geckodriver-v0.31.0-linux64.tar.gz &&\
\
echo "===> Installing firefox.." && \
apt-get purge firefox && \
wget "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
tar -xjf $(ls | grep firefox*) -C /opt/ && \
ln -s /opt/firefox/firefox /usr/bin/firefox
#RUN rm firefox*.tar

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/

RUN pip3 install -r requirements.txt && \
rm -rf /var/lib/apt/lists/*
CMD tail -f /dev/null && \
["bash"]
#CMD python3 example.py
