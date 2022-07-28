FROM python:slim-buster

#Debug tools
RUN apt update && apt install jq vim -y

RUN pip install boto3 requests pyyaml
ADD update.py /opt