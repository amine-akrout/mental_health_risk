FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000

# Run the web service on container startup using gunicorn

CMD exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 8 --timeout 0 app:app