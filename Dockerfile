FROM python:3.11

ENV WORKDIR /opt
# prequisite --- install python requests module
COPY requirements.txt ${WORKDIR}/
RUN pip3 install -r /opt/requirements.txt

# install nodeJS
RUN curl -fsSL https://fnm.vercel.app/install | bash && \
	. ~/.bashrc && \
	fnm use --install-if-missing 22

# copy python and bash wrapper
COPY *py ${WORKDIR}/
COPY *sh ${WORKDIR}/

# copy batchCasesCreator.js
COPY *js ${WORKDIR}/

RUN apt-get update -y && \
    apt-get install -y emacs screen