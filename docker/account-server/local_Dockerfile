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

ENV newuser="admin"
RUN useradd -ms /bin/bash $newuser \
    && usermod -aG sudo $newuser \
    && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $newuser

WORKDIR /home/$newuser

# x86
# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# RUN unzip awscliv2.zip
# RUN sudo ./aws/install

# ARM64
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" \
    unzip awscliv2.zip \
    sudo ./aws/install

COPY docker/account-server/requirements.txt .
RUN pip3 install -r requirements.txt

COPY configuration/credentials ./.aws/credentials
RUN sudo chown -R $newuser:$newuser .aws 

RUN mkdir -p persistence/ \
    touch persistence/neverquest.db

COPY main_account_server.py  .
COPY configuration/secrets.json configuration/secrets.json
#COPY persistence/ persistence
COPY resources/ resources
COPY services/account_service.py services/account_service.py
COPY services/token_service.py services/token_service.py

RUN sudo chown -R ${newuser}:${newuser} .

CMD ["python3", "-u", "main_account_server.py"]
