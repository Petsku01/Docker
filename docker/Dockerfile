# Stage 1 Builder stage for dependencies
# Toimiii 10h takana
FROM ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install build tools
RUN apt-get update && apt-get install -y 
    build-essential 
    curl 
    && apt-get clean 
    && rm -rf varlibaptlists

# Install code-server (VS Code in browser)
RUN curl -fsSL httpscode-server.devinstall.sh  sh

# Stage 2 Final image
FROM ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Copy build artifacts
COPY --from=builder usrbincode-server usrbincode-server
COPY --from=builder usrlibcode-server usrlibcode-server

# Install runtime dependencies
RUN apt-get update && apt-get install -y 
    bash 
    zsh 
    curl 
    wget 
    nano 
    vim 
    git 
    python3 
    python3-pip 
    jq 
    openssh-server 
    sudo 
    htop 
    net-tools 
    nodejs 
    npm 
    awscli 
    && apt-get clean 
    && rm -rf varlibaptlists

# Install oh-my-zsh for enhanced shell
RUN sh -c $(curl -fsSL httpsraw.githubusercontent.comohmyzshohmyzshmastertoolsinstall.sh)  --unattended

# Set up SSH
RUN mkdir varrunsshd
COPY configsshd_config etcsshsshd_config
RUN chmod 644 etcsshsshd_config

# Set up non-root user
COPY scriptssetup_user.sh setup_user.sh
RUN chmod +x setup_user.sh && setup_user.sh

# Set up working directory and permissions
WORKDIR homeuser
RUN chown -R useruser homeuser

# Copy configuration files
COPY configmotd etcmotd
COPY configzshrc homeuser.zshrc
RUN chown useruser homeuser.zshrc

# Copy scripts
COPY scripts homeuserscripts
RUN chmod +x homeuserscripts.sh && chown -R useruser homeuserscripts

# Set up persistent volumes
VOLUME homeuserdata
VOLUME homeuser.ssh

# Expose ports (SSH 22, code-server 8080, web 80)
EXPOSE 22 8080 80

# Copy and set entrypoint
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Entrypoint
ENTRYPOINT [entrypoint.sh]

# Default command
CMD [binzsh]
