FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    sudo \
    python3 \
    python3-pip \
    vim \
    net-tools \
    lsof

ENV newuser="admin"
RUN useradd -ms /bin/bash $newuser \
    && usermod -aG sudo $newuser \
    && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $newuser

WORKDIR /home/$newuser

COPY requirements.txt . 
COPY main_game_server.py  .
COPY services/connection_service.py services/

RUN pip3 install -r requirements.txt

CMD ["python3", "main_game_server.py"]
