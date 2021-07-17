# base localdev

FROM ubuntu:focal AS base

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8
RUN apt update && \
    apt upgrade -y && \
    apt install -y curl wget git zip unzip zsh-autosuggestions build-essential ninja-build htop jq less locales man-db nano software-properties-common sudo time vim multitail lsof ssl-cert fish zsh && \
    locale-gen en_US.UTF-8 && \
    wget https://apt.puppet.com/puppet-tools-release-focal.deb && \
    wget https://apt.puppetlabs.com/puppet6-release-focal.deb && \
    dpkg -i puppet6-release-focal.deb && \
    dpkg -i puppet-tools-release-focal.deb && \
    apt update && \
    apt install -y pdk puppet-agent puppet-bolt && \
    rm -f puppet6-release-bionic.deb puppet-tools-release-bionic.deb && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
    useradd -l -u 33333 -G sudo -md /home/localdev -s /bin/bash -p localdev localdev && \
    # passwordless 'sudo' group
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers && \
    usermod -s $(which zsh) localdev && \
    /opt/puppetlabs/puppet/bin/gem install homesick puppet-debugger hub -N && \
    ln -s /opt/puppetlabs/puppet/bin/homesick /usr/local/bin/homesick

FROM base AS user

USER localdev
ENV HOME=/home/localdev
WORKDIR $HOME
RUN sudo echo 'source .zshrc' >> ~/.profile
COPY .zshrc /home/localdev/.zshrc

FROM user as project

ARG CHROME_VERSION="google-chrome-stable"

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list && \
    sudo apt update -qqy && \
    sudo apt upgrade -qqy && \
    sudo apt install -qqy ${CHROME_VERSION:-google-chrome-stable} python3 python3-pip libnss3-tools libnss3-dev && \
    pip install selenium bs4 html5lib datetime && \
    sudo apt clean && \
    sudo apt -qqy install  && \
    sudo rm /etc/apt/sources.list.d/google-chrome.list && \
    sudo rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ENTRYPOINT /usr/bin/zsh
