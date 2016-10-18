#
# Python Dockerfile
#

# Pull base image.
FROM fedora

# Install Python.
# RUN dnf -y update
RUN dnf -y install p7zip lrzip openssh-clients procps-ng
RUN dnf -y install python3 python3-devel python3-pip python3-virtualenv python3-numpy python3-lxml
RUN pip3 install mwparserfromhell

# Copy scripts
WORKDIR /root
COPY wikidiff_fast.py .
COPY wikidiff.sh .

# Environment
ENV PYTHONIOENCODING utf_8
