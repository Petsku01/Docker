FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install all dependencies in one layer
RUN apt-get update && apt-get install -y \
    bash \
    zsh \
    curl \
    wget \
    nano \
    vim \
    git \
    python3 \
    python3-pip \
    jq \
    openssh-server \
    sudo \
    htop \
    net-tools \
    nodejs \
    npm \
    awscli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Set up SSH
RUN mkdir -p /var/run/sshd

# Create non-root user
RUN useradd -m -s /bin/zsh user && \
    usermod -aG sudo user && \
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/user

# Set up working directory
WORKDIR /home/user

# Copy configuration files
COPY config/sshd_config /etc/ssh/sshd_config
COPY config/motd /etc/motd
COPY config/zshrc /home/user/.zshrc

# Copy scripts
COPY scripts /home/user/scripts

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh

# Set permissions
RUN chmod 644 /etc/ssh/sshd_config && \
    chmod 644 /etc/motd && \
    chmod +x /entrypoint.sh && \
    chmod +x /home/user/scripts/*.sh && \
    chown -R user:user /home/user

# Set up persistent volumes
VOLUME ["/home/user/data", "/home/user/.ssh"]

# Expose ports (SSH 22, code-server 8080, web 80)
EXPOSE 22 8080 80

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["/bin/zsh"]
