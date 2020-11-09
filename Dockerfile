FROM docker:stable-dind
RUN apk update &\
apk add python3 &\
apk add py3-pip
RUN unset DOCKER_HOST
RUN pip3.8 install ciscodnacapphosting
COPY docker_start.sh /
ENTRYPOINT ["sh", "/docker_start.sh"]