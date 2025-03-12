FROM python:3.12

WORKDIR /usr/local/app

COPY src ./src
RUN pip install -r ./src/requirements.txt

RUN apt-get update && apt-get install -y \
    wget unzip curl \
    chromium-driver \
    chromium


CMD [ "python", "-u", "./src/crawler.py" ]