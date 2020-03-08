FROM python:3.8-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "app:app"]
