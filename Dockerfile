FROM kageurufu/debian-python

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD . /home/docker/

EXPOSE 80

CMD ["/home/docker/.config/docker-run"]

# Some basic usage:
#   $ docker build -t pkgname .
#   $ docker run \
#       -p 5000:80 \
#       --rm \
#       pkgname:latest
