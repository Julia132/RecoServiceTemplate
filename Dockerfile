FROM python:3.8-buster as build

COPY . .

FROM python:3.8-slim-buster as runtime

WORKDIR /usr/src/app
COPY --from=build data ./

ENV PYTHONOPTIMIZE true
ENV DEBIAN_FRONTEND noninteractive

# setup timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir service
COPY --from=build service ./service
COPY --from=build requirements.txt main.py gunicorn.config.py ./

RUN apt update
RUN apt install gcc -y
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
