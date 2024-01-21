
#
# --- Build Stage ---
#
FROM python:3.11-alpine as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY iq/ iq/
COPY templates/ templates/
COPY static/ static/


#
# --- Run Stage ---
#
FROM python:3.11-alpine

WORKDIR /app

RUN adduser -D iq
USER iq

COPY --from=builder /root/.local /home/iq/.local
COPY --from=builder /app /app

ENV PATH="/home/iq/.local/bin:${PATH}"

EXPOSE 8000
CMD ["uvicorn", "iq.server:app", "--host", "0.0.0.0", "--port", "8000"]
