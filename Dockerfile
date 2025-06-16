FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver - simplified version
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F. '{print $1}') && \
    echo "Chrome version: $CHROME_VERSION" && \
    CHROME_DRIVER_VERSION=$(wget -q -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    echo "Installing ChromeDriver version: $CHROME_DRIVER_VERSION" && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

WORKDIR /app
COPY . .

RUN pip install selenium pytest pytest-html

CMD ["pytest", "tests/", "--verbose", "--html=report.html"]
