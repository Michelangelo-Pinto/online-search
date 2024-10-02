FROM python:3.12-slim



# Definisci valori predefiniti per UID e GID che possono essere sovrascritti durante la build
ARG UID=1618
ARG GID=1618

# Aggiorna e installa openssl, git, zip, unzip, cowsay e crea l'utente con UID e GID specificati
RUN apt-get update && apt-get install -y \
    git zip unzip cowsay sudo && rm -rf /var/lib/apt/lists/* \
    && groupadd -g ${GID} onlineagent_group \
    && useradd -m -d /home/superuser -s /bin/bash -u ${UID} -g ${GID} -p $(openssl passwd -1 YourPasswordHere) onlineagent \
    && usermod -aG sudo onlineagent \
    && echo "onlineagent ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


COPY --chown=onlineagent:onlineagent code /home/onlineagent/code


# Install pip requirements
COPY code/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt \
    && apt-get update && apt-get install -y cowsay procps && rm -rf /var/lib/apt/lists/* \
    && chmod -R +x /home/onlineagent/code

# Imposta l'utente 'onlineagent' per eseguire i comandi
USER onlineagent


ENTRYPOINT ["/bin/bash", "-c", "sudo chown -R 1618:1618 /home/onlineagent && /home/onlineagent/code/entrypoint.sh \"$@\"", "--"]




# FROM python:3.12-slim

# # Create a non-root user
# ARG UID=1618
# ARG GID=1618

# # Aggiorna e installa openssl, crea il gruppo e l'utente con UID e GID specificati
# RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/* \
#     && groupadd -g ${GID} onlineagent_group \
#     && useradd -m -d /home/superuser -s /bin/bash -u ${UID} -g ${GID} -p $(openssl passwd -1 YourPasswordHere) onlineagent

# COPY --chown=onlineagent:onlineagent code /home/onlineagent/code


# # Install pip requirements
# COPY code/requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt \
#     && rm -rf /tmp/requirements.txt \
#     && apt-get update && apt-get install -y git zip unzip cowsay && rm -rf /var/lib/apt/lists/* \
#     && chmod -R +x /home/onlineagent/code


# # Set the user
# USER onlineagent

# WORKDIR /home/onlineagent

# ENTRYPOINT ["/bin/bash", "-c", "/home/onlineagent/code/entrypoint.sh \"$@\"", "--"]
