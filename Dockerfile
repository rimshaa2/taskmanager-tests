FROM python:3.9-slim

# Set HOME environment variable
ENV HOME=/app
WORKDIR $HOME

# Install dependencies + Chrome
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Install Chromedriver (match Chrome version)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -q https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Fix Selenium cache permissions
RUN mkdir -p /.cache/selenium && \
    chmod 777 /.cache/selenium

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "tests/"]
