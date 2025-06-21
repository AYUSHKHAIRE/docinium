FROM python:3.10

# Set working directory
WORKDIR /container

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY script.py .
COPY logger_config.py .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Mozilla GPG key
RUN mkdir -p /etc/apt/keyrings && \
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O - | gpg --dearmor > /etc/apt/keyrings/packages.mozilla.org.gpg

# Add Firefox repo
RUN echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.gpg] https://packages.mozilla.org/apt mozilla main" \
    > /etc/apt/sources.list.d/mozilla.list

# Set APT pin priority (no sudo)
RUN printf "Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n" \
    > /etc/apt/preferences.d/mozilla

# Install Firefox
RUN apt-get update && apt-get install -y firefox

# install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.34.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.34.0-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v0.34.0-linux64.tar.gz

# Set the default command
CMD ["python", "script.py"]
