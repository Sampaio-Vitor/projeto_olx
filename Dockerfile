# Start with a Python base image
FROM python:3.9

# Set the working directory in docker
WORKDIR /app

# Install necessary packages
RUN apt-get update -q && apt-get install -y -q --fix-missing \
    wget \
    unzip

# Add Google Chrome's official repository and install the specific version
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable=116.0.5845.110-1

# Download and unzip the provided Chromium file
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip -d /usr/bin

# Set ChromeDriver as the WebDriver (if using Selenium with Chrome)
ENV SELENIUM_DRIVER_EXECUTABLE_PATH /usr/bin/chromedriver
ENV DISPLAY=:99

# Copy requirements and install dependencies from the root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying necessary csv files from data folder
COPY data/dados_detalhados_olx.csv /app/data/dados_detalhados_olx.csv
COPY data/new_links_olx.csv /app/data/new_links_olx.csv
COPY data/processed_data.csv /app/data/processed_data.csv
COPY data/scored_data.csv /app/data/scored_data.csv
COPY data/train_data/final_dataframe.csv /app/data/train_data/final_dataframe.csv

# Copy source code and other utilities
COPY src /app/src

# Copy the best_model.pkl file
COPY models/best_model.pkl /app/models/best_model.pkl

# Add the root directory of your project to the Python path
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Copy the root level important files
COPY .gitignore /app/.gitignore
COPY config.yaml /app/config.yaml
COPY README.md /app/README.md

# Expose the port the app runs on (assuming it's 5000 for Flask)
EXPOSE 5000

# Clean up the package lists
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Default command to run on container start (starting the web interface)
CMD ["python", "/app/src/webapp/app.py"]
