# Usage:
# 1. Build this image:
#     docker build -t spidy:latest .
# 2. Run spidy container:
#     docker run --rm -it -v $PWD:/data spidy

FROM python:3.6
WORKDIR /src/app/
COPY . .
RUN pip install -r requirements.txt

VOLUME [ "/data" ]
WORKDIR /data

ENTRYPOINT [ "python", "/src/app/spidy/crawler.py" ]
