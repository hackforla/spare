# Base image
FROM python:3.6

# Use python -u/unbuffered setting
ENV PYTHONUNBUFFERED 1

# Install requirements
COPY requirements /app/requirements/

WORKDIR /app
RUN pip install -r requirements/local.txt

COPY . /app

CMD "scripts/startup.sh"
