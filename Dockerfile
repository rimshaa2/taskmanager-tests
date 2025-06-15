FROM python:3.9-slim 

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y wget unzip
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip && mv chromedriver /usr/bin/ && chmod +x /usr/bin/chromedriver

RUN pip install -r requirements.txt  

CMD ["pytest", "tests/"] 
