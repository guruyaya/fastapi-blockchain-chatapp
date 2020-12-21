FROM rackspacedot/python37

MAINTAINER Yair Eshel Cahansky (admin@pace2pace.net)

RUN apt-get update

ADD ./* /src/

RUN cd /src/ && pip install -r requirements.txt
CMD cd /src/ && python main_fast.py