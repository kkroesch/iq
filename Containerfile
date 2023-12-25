
#
# --- Build Stage ---
#
FROM python:3.11-alpine AS builder

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

#
# --- Run Stage ---
#
FROM python:3.11-alpine

WORKDIR /usr/src/app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/src/app .

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
