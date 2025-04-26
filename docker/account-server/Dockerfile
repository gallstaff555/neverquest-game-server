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
# make sure server is using id 1005 for neverquest user
ENV user_id="1005"

RUN groupadd -g $user_id $newuser \
    && useradd -u $user_id -g $newuser -m $newuser \
    && usermod -aG sudo $newuser \
    && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $newuser

WORKDIR /home/$newuser

# x86
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    unzip awscliv2.zip \
    sudo ./aws/install \
    rm awscliv2.zip

# ARM64
# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" \
#     unzip awscliv2.zip \
#     sudo ./aws/install \
#     rm awscliv2.zip

COPY docker/account-server/requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt

COPY main_account_server.py  .
COPY configuration/secrets.json configuration/secrets.json
COPY resources/account_resource.py resources/account_resource.py
COPY persistence/account_repository.py persistence/account_repository.py
COPY persistence/scripts/ persistence/scripts/
COPY services/account_service.py services/account_service.py
COPY services/token_service.py services/token_service.py

RUN sudo chown -R ${newuser}:${newuser} .

RUN touch persistence/neverquest.db

CMD ["python3", "-u", "main_account_server.py"]