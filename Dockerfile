FROM python:3.7-alpine

# Set up environment
WORKDIR /app

RUN pip install --no-cache-dir gunicorn
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["gunicorn", "--reload", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
