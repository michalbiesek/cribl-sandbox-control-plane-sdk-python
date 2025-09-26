# Use the official Python 3.11 image as base
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create workspace directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Note: Dependencies will be installed via postCreateCommand
# This ensures they're installed in the correct user context

# Set the default command
CMD ["python", "main.py"]
