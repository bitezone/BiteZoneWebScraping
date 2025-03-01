FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && apt-get clean

CMD ["python", "main.py"]