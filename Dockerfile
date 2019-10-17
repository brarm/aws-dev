FROM python:3-slim

# RUN apt-get update && apt-get install -y git
RUN apt-get update
RUN apt-get install -y curl
# RUN git clone --single-branch --branch deploy https://github.com/brarm/aws-dev

EXPOSE 80
WORKDIR /app
ADD . /app
# WORKDIR ./aws-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "app.py" ]

