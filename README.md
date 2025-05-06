Build the Docker Image

    Create the project directory and files:
    bash

mkdir -p super-ubuntu-docker/config super-ubuntu-docker/scripts super-ubuntu-docker/data
cd super-ubuntu-docker
Use a text editor to create the files with the contents above.
Build the image:
bash

    docker build -t super-ubuntu .
    
Run the Docker Container
Option 1: Interactive Shell

Run with persistent volumes:
bash
docker run -it -v $(pwd)/data:/home/user/data -v $(pwd)/ssh:/home/user/.ssh super-ubuntu

    See the MOTD, run example.sh, and get a zsh prompt as user.
    Try commands:
    bash

whoami  # Outputs: user
node --version  # Check Node.js
aws --version  # Check AWS CLI
ll  # Alias for ls -la
/home/user/scripts/help.sh  # Show help
cat /home/user/data/output.txt  # View persisted output


Option 2: SSH Access

    Generate an SSH key pair on the host (if not already done):
    bash

ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ""
mkdir -p ssh
cp ~/.ssh/id_rsa.pub ssh/authorized_keys
Run with SSH enabled:
bash
docker run -d --name ubuntu-ssh -p 2222:22 -v $(pwd)/data:/home/user/data -v $(pwd)/ssh:/home/user/.ssh -e ENABLE_SSH=true super-ubuntu
Connect:
bash
ssh user@localhost -p 2222


Verify Persistence

Check the host’s data directory:
bash
ls data/
cat data/output.txt

See output.txt with content like:
text
Hello from Wed May 07 12:34:56 UTC 2025
