FROM python:3.12-slim

# Build arguments to select the runtime mode:
#   web  → run the Streamlit web demo  (default)
#   api  → run the FastAPI REST backend
ARG MODE=web

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose ports
#   8501 → Streamlit
#   8000 → FastAPI / uvicorn
EXPOSE 8501 8000

ENV MODE=${MODE}

CMD ["sh", "-c", "\
  if [ \"$MODE\" = 'api' ]; then \
    uvicorn api:app --host 0.0.0.0 --port 8000; \
  else \
    streamlit run web_demo.py --server.port 8501 --server.address 0.0.0.0; \
  fi"]
