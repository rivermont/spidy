# To run spidy in a container and write all files back to the host filesystem:
#   docker run --rm -it -v $PWD:/data spidy

FROM python:3.6
LABEL maintainer "Peter Benjamin <petermbenjamin@gmail.com>"
WORKDIR /src/app/
COPY . .
VOLUME [ "/data" ]

RUN apt-get update \
    && apt-get install -y \
    --no-install-recommends \
    python3 \
    python3-lxml \
    python3-requests \
    && rm -rf /var/cache/apt/* \
    && pip install -r requirements.txt

ENTRYPOINT [ "python", "spidy/crawler.py" ]
