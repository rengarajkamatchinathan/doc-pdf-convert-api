# Use a Python base image
FROM python:3.9-slim

# Install system dependencies (Pandoc, LaTeX)
RUN apt-get update && apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    --no-install-recommends && \
    apt-get clean

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app into the container
COPY . /app

# Expose the necessary port (e.g., 8000 for FastAPI)
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
