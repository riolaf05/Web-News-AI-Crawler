FROM arm32v7/ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common curl
RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt install -y python3.8

RUN mkdir /home/scripts
WORKDIR /home/scripts

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY ./telegram_feedback.py /home/scripts/

CMD ["python3", "telegram_feedback.py"]