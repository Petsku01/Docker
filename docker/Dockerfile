# Stage 1: Builder (fetch secure tools)
FROM ubuntu:24.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install oh-my-zsh manually
RUN git clone https://github.com/ohmyzsh/ohmyzsh.git /tmp/ohmyzsh --depth=1 && \
    cp -r /tmp/ohmyzsh/tools/install.sh /tmp/install-ohmyzsh.sh && \
    chmod +x /tmp/install-ohmyzsh.sh && \
    /tmp/install-ohmyzsh.sh --unattended && \
    rm -rf /tmp/ohmyzsh /tmp/install-ohmyzsh.sh

# Install code-server via DEB (latest version)
ARG CODE_SERVER_VERSION=4.107.1
RUN curl -fsSL -o /tmp/code-server.deb https://github.com/coder/code-server/releases/download/v${CODE_SERVER_VERSION}/code-server_${CODE_SERVER_VERSION}_amd64.deb

# Stage 2: Runtime
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

LABEL maintainer="Petsku01" \
      description="Secure Ubuntu dev container with tools" \
      version="1.2"

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    zsh=5.9-5ubuntu1 \
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
    nodejs=20.11.0-1nodesource1 \
    npm \
    awscli=2.15.0-1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /root/.oh-my-zsh /root/.oh-my-zsh
COPY --from=builder /tmp/code-server.deb /tmp/code-server.deb
RUN dpkg -i /tmp/code-server.deb && rm /tmp/code-server.deb

# SSH hardening (require key-based auth for security)
RUN mkdir -p /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Non-root user with sudo (require password for safety - NO NOPASSWD)
RUN useradd -m -s /bin/zsh user -G sudo && \
    echo "user ALL=(ALL) ALL" > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user

WORKDIR /home/user

# Copy configs/scripts (assume originals; update as needed)
COPY config/sshd_config /etc/ssh/sshd_config
COPY config/motd /etc/motd
COPY config/zshrc /home/user/.zshrc
COPY scripts /home/user/scripts

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh

RUN chown -R user:user /home/user && \
    chmod +x /entrypoint.sh /home/user/scripts/*.sh && \
    chmod 750 /home/user/data /home/user/.ssh

VOLUME ["/home/user/data", "/home/user/.ssh"]

EXPOSE 22 8080

HEALTHCHECK --interval=30s --timeout=10s CMD pgrep sshd || exit 1

ENTRYPOINT ["/entrypoint.sh"]
