# Base image
FROM python:3.6

# Use python -u/unbuffered setting
ENV PYTHONUNBUFFERED 1

# Install requirements
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app

CMD "scripts/startup.sh"
