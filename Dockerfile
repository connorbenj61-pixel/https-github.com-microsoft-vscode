# Use this Dockerfile to containerize your Python project for easy deployment anywhere
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Default command (can be changed as needed)
CMD ["python", "biochemical_mind_map.py"]
