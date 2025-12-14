FROM python:3.10

WORKDIR /container

# copy the files 
COPY requirements.txt .
COPY script.py .
COPY logger_config.py .
COPY socket_client.py .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install system dependencies for Firefox and Geckodriver
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libx11-xcb1 \
    libnss3 \
    libdbus-glib-1-2 \
    libxss1 \
    libasound2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxrender1 \
    libxtst6 \
    libxshmfence1 \
    fonts-liberation \
    xdg-utils \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Mozilla repo for latest Firefox
RUN mkdir -p /etc/apt/keyrings && \
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O - | gpg --dearmor > /etc/apt/keyrings/packages.mozilla.org.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.gpg] https://packages.mozilla.org/apt mozilla main" > /etc/apt/sources.list.d/mozilla.list && \
    printf "Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n" > /etc/apt/preferences.d/mozilla && \
    apt-get update && apt-get install -y firefox && \
    rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.36.0-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v0.36.0-linux64.tar.gz

# run the script
CMD ["python", "script.py"]
