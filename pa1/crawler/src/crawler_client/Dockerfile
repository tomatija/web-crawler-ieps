FROM python:3.12

WORKDIR /usr/local/app

COPY src ./src
RUN pip install -r requirements.txt

CMD [ "python", "./src/dummy.py" ]