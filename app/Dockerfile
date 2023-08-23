FROM python:3.10

WORKDIR /app

COPY /app/requarment.txt .

RUN pip install -r /app/requarment.txt


COPY . .

CMD [ "python", "app.py" ]