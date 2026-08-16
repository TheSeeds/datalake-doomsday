#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

# Base do laboratório local
apt-get update
apt-get install -y \
  curl \
  git \
  jq \
  net-tools \
  nano \
  ca-certificates \
  gnupg \
  lsb-release

# Ajusta hostname por convenção
hostnamectl set-hostname "$(hostname)"

# Garante que o Docker esteja disponível
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Run install-docker.sh first."
  exit 1
fi

# Deixa o ambiente pronto para serviços locais
mkdir -p /opt/the-seed /var/lib/the-seed
chmod 755 /opt/the-seed /var/lib/the-seed

echo "VM pronta para laboratório local."
