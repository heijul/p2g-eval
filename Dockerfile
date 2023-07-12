FROM ubuntu:latest
LABEL maintainer="Julius Heinzinger <julius.heinzinger@gmail.com>"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip ghostscript git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR p2g-eval
RUN git clone --recurse-submodules https://github.com/heijul/p2g-eval
RUN pip3 install p2g-eval/custom_conf
RUN pip3 install p2g-eval/pdf2gtfs
RUN pip3 install ./p2g-eval

WORKDIR /p2g-eval/p2g-eval
RUN useradd -u 1234 -mU john && chown -R john:john .
USER john
CMD python3 -m unittest discover test
