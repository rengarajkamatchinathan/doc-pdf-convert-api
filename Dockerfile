# Use an official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install pandoc
RUN apt-get update && apt-get install -y pandoc
RUN apt-get update && apt-get install -y texlive-full


# Expose port 8000
EXPOSE 8000

# Start the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
