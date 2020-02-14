FROM python:alpine
ADD . /src
RUN pip install /src && \
    rm -rf /src
CMD ["sh"]
