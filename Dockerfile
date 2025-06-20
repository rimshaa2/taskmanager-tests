FROM markhobson/maven-chrome:latest

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

CMD ["pytest", "test/test_add_task.py"]
