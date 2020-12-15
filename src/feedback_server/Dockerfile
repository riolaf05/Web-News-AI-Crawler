FROM arm32v7/ubuntu:18.04

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /home/scripts
WORKDIR /home/scripts

COPY ./telegram_feedback.py /home/scripts/

CMD ["python3", "telegram_feedback.py"]