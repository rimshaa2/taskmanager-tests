FROM python:3.10

RUN apt-get update && \
    apt-get install -y wget unzip curl chromium chromium-driver

WORKDIR /tests

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest"]
