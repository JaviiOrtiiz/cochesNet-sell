# Image: python:latest
FROM arm32v7/python:latest

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Copy main.py to the working directory
COPY main-no-pandas.py .

# Install the required packages
RUN pip install -r requirements.txt

# Run the main.py file
CMD ["python", "main.py"]