FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependencies from requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project to working directory
COPY . .

# Expose the port
EXPOSE 8000

# Command to run app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]