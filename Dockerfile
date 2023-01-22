FROM python:3.11.1

COPY app/requirements.txt .

RUN pip3 install --upgrade pip setuptools && \
    pip3 install --upgrade flake8 autopep8 pytest refurb && \
    pip3 install --no-cache-dir -r requirements.txt