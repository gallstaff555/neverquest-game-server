FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    sudo \
    python3 \
    python3-pip \
    vim \
    net-tools \
    lsof \
    curl \
    unzip

ENV newuser="neverquest"
RUN useradd -ms /bin/bash $newuser \
    && usermod -aG sudo $newuser \
    && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $newuser

WORKDIR /home/$newuser

COPY requirements.txt . 
RUN pip3 install -r requirements.txt --break-system-packages

COPY npc/ npc/
COPY main_world_server.py  .
COPY configuration/config.py configuration/config.py

CMD ["python3", "-u" ,"main_world_server.py"]