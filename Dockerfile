FROM docker:stable-dind
RUN apk update &\
apk add python3 &\
apk add py3-pip
COPY ./ ./

#RUN pip3.8 install -r requirements.txt
RUN unset DOCKER_HOST
RUN /usr/local/bin/dockerd-entrypoint.sh &
RUN pip3.8 install ciscodnacapphosting
#ENTRYPOINT ["python3.8", "ciscodnacapphosting/cli.py"]
CMD ["python3.8", "ciscodnacapphosting/cli.py"]