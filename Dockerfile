FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# Install wget and unzip
RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Download the zip file
RUN wget --no-check-certificate 'https://aizakonik-data.fra1.cdn.digitaloceanspaces.com/data.zip' -O /code/app/data.zip

# Unzip the file
RUN unzip /code/app/data.zip -d /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
