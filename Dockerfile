FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN apk update && apk add --no-cache \
    chromium \
    chromium-chromedriver \
    && rm -rf /var/cache/apk/*
    
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt


# Run the application
CMD ["python", "main.py"]


