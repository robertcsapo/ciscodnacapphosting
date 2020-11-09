FROM docker:stable-dind
RUN apk update &\
apk add python3 &\
apk add py3-pip
RUN unset DOCKER_HOST
RUN sed 's/exec "$@"/exec "$@" \&/g' -i /usr/local/bin/dockerd-entrypoint.sh
RUN pip3.8 install ciscodnacapphosting
#ENTRYPOINT ["python3.8", "ciscodnacapphosting/cli.py"]
#CMD ["python3.8", "ciscodnacapphosting/cli.py"]
CMD /usr/local/bin/dockerd-entrypoint.sh