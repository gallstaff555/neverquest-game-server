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

COPY docker/account-server/requirements.txt . 
COPY main_account_server.py  .
COPY configuration/secrets.json configuration/secrets.json
COPY persistence/ persistence
COPY resources/ resources
COPY services/account_service.py services/account_service.py
COPY services/token_service.py services/token_service.py

RUN pip3 install -r requirements.txt

CMD ["python3", "main_account_server.py"]
