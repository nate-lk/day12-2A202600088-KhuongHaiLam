# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build
COPY 05-scaling-reliability/production/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
# Since context is root, we copy the production folder contents to /app
COPY 05-scaling-reliability/production/ /app/

# Expose port
EXPOSE 8000

CMD ["python", "app.py"]
