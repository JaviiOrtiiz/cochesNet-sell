# Image: python:latest
FROM arm32v7/python:latest

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Copy main.py to the working directory
COPY main-no-pandas.py .

# Copiar el script de shell al contenedor
COPY run_script.sh .

# Install the required packages
RUN pip install -r requirements.txt

# Run the shell script to execute the python script periodically
CMD ["sh", "run_script.sh"]