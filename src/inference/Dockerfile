FROM derekmerck/keras-tf:py3-tf190-k222-arm32v7

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 uninstall conda -y
RUN pip3 uninstall Pillow -y
RUN pip3 uninstall Werkzeug -y 

RUN mkdir /home/scripts
RUN mkdir /home/scripts/models
WORKDIR /home/scripts

COPY ./models/rss_model.h5 /home/scripts/models
COPY ./feed_list.txt /home/scripts/
COPY ./stateful_news_ai.py /home/scripts
COPY ./config.ini /home/scripts

CMD ["python3", "stateful_news_ai.py"]