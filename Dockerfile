# Use the official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["python", "-m", "streamlit", "run", "src/main_stream.py", "--server.port=8501", "--server.address=0.0.0.0"]

