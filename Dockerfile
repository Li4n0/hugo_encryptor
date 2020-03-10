FROM jfloff/alpine-python:latest-slim
WORKDIR /blog
ADD requirements.txt /
ADD hugo-encryptor.py /
RUN /entrypoint.sh -a libxslt -b libxslt-dev -b libxml2-dev -b g++ \
    && rm -f /requirements.txt
CMD ["python", "/hugo-encryptor.py"]
