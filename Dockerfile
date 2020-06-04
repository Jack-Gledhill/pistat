FROM python:latest

COPY . /opt/site

WORKDIR /opt/site

RUN python3.8 -m pip install -r requirements.txt

WORKDIR /opt/site/website

CMD ["python3.8", "site.py"]