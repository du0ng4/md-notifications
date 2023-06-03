FROM python:slim-buster

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH="$PYTHONPATH:/app"

RUN apt-get -qq update \
    && apt-get -qq -y install \
        python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv $VIRTUAL_ENV \
    && pip3 install -q --upgrade pip \
    && pip3 install -q requests pytz

WORKDIR /app
ADD src /app/src

CMD ["python3", "src/main.py"]