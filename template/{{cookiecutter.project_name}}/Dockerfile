FROM python:{{ cookiecutter.python_version }}
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip3 install -U pip && pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
