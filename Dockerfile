FROM python:3.6
LABEL maintainer="wilddeej@gmail.com"

ARG GIT_REPO=https://github.com/wilddeej/dockurl.git
ARG GIT_REPO_REV=master
ENV DATA_DIR /data
RUN \
  mkdir $DATA_DIR \
  && git clone $GIT_REPO \
  && cd dockurl \
  && git checkout $GIT_REPO_REV \
  && pip install -r requirements.txt \
  && python setup.py install

VOLUME $DATA_DIR
WORKDIR $DATA_DIR
CMD ["python", "-m", "dockurl"]

