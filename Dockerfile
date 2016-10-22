#
# Python Dockerfile
#

# Pull base image.
FROM fedora

# Environment
WORKDIR /root
ENV PYTHONIOENCODING utf_8

# Install Python.
# RUN dnf -y update
RUN dnf -y install tar bzip2 lrzip openssh-clients procps-ng
RUN dnf -y install gcc libxml2-devel libxslt-devel
# RUN dnf -y install python3 python3-devel python3-pip python3-virtualenv python3-lxml

# Install pypy
COPY progs/pypy-5.4.1-linux_x86_64-portable.tar.bz2 .
RUN tar -xjf pypy-5.4.1-linux_x86_64-portable.tar.bz2
RUN ln -s pypy-5.4.1-linux_x86_64-portable/bin .
RUN bin/pypy -m ensurepip
RUN bin/pip install lxml

# Copy scripts
COPY wikidiff_py2.py .
COPY wikidiff.sh .
