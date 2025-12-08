# Multi-stage build to minimize the size of the final image
# Stage 1: Builder
FROM python:3.11 AS builder

# Installing UV for dependency management
RUN pip install uv

# Setting the working directory
WORKDIR /app

# Copying the project file
COPY pyproject.toml ./
COPY uv.lock ./

# Installing dependencies using UV
RUN uv sync --frozen

# Stage 2: Final image
FROM python:3.11-slim

# Setting the working directory
WORKDIR /app

# Copying installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copying the application source code
COPY . .

# Command to run the bot
CMD ["python", "src/bot/main.py"]