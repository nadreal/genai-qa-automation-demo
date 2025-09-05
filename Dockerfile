FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for Playwright, Selenium, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    git \
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
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir playwright && \
    playwright install

# Copy application code
COPY . .

# Default command: run tests
CMD ["pytest", "--maxfail=2", "--disable-warnings", "-v"]
