FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for Playwright and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    git \
    python3 \
    python3-pip \
    python3-venv \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libxkbcommon0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*


# Install Playwright and its dependencies
RUN pip install --no-cache-dir playwright
RUN playwright install
RUN pip install --upgrade pip


# Install other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command to run the tests
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v"]
