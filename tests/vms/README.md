# VM local com Vagrant + libvirt

Este diretório contém a configuração de máquinas virtuais do projeto para laboratório local, testes e validação arquitetural.

Importante: este ambiente é de teste, não de produção.

Ele serve para validar arquitetura local, isolamento, provisionamento e fluxo do MVP sem comprometer dados reais ou operação crítica.

## Objetivo

Criar um ambiente simples, reproduzível e isolado para:

- VM-01: data-core
- VM-02: app-query
- VM-03: ai-sandbox

## Requisitos do host

No Fedora Linux, o ambiente precisa ter:

- Vagrant
- libvirt
- qemu-kvm
- virt-install
- o plugin `vagrant-libvirt`

Verifique rapidamente:

```bash
vagrant --version
virsh --version
libvirtd --help
vagrant plugin list | grep libvirt
```

## Instalação das dependências

```bash
sudo dnf install -y @virtualization
sudo systemctl enable --now libvirtd
sudo usermod -aG libvirt,kvm "$USER"
newgrp libvirt
newgrp kvm
vagrant plugin install vagrant-libvirt
```

Se o `vagrant-libvirt` não estiver instalado, a VM não sobe corretamente.

## Ajuste de permissões do storage do libvirt

A falha mais comum no Fedora é a permissão de escrita para o diretório de imagens do libvirt.

Use estes comandos:

```bash
sudo mkdir -p /var/lib/libvirt/images
sudo chown root:kvm /var/lib/libvirt/images
sudo chmod 0770 /var/lib/libvirt/images

sudo semanage fcontext -a -t virt_image_t "/var/lib/libvirt/images(/.*)?" 2>/dev/null || true
sudo restorecon -Rv /var/lib/libvirt/images

sudo setfacl -m u:107:rwx /var/lib/libvirt/images
```

Se necessário, também ajuste o diretório padrão do libvirt:

```bash
sudo semanage fcontext -a -t virt_image_t "/root/.local/share/libvirt/images(/.*)?" 2>/dev/null || true
sudo restorecon -Rv /root/.local/share/libvirt/images 2>/dev/null || true
sudo setfacl -m u:107:rwx /root/.local/share/libvirt/images 2>/dev/null || true
```

## Definir o pool do libvirt

O pool padrão do libvirt deve apontar para `/var/lib/libvirt/images`:

```bash
sudo virsh pool-destroy default 2>/dev/null || true
sudo virsh pool-undefine default 2>/dev/null || true
sudo virsh pool-define-as --name default --type dir --target /var/lib/libvirt/images
sudo virsh pool-start default
sudo virsh pool-autostart default
```

Confirme:

```bash
sudo virsh pool-list --all
sudo virsh pool-dumpxml default | grep -A8 target
```

## Como subir a VM

A partir deste diretório:

```bash
cd /home/cflb/Projetos/TheSeed/datalake-doomsday/tests/vms
vagrant validate
vagrant up vm-01-data-core --provider=libvirt
```

Para subir todas as VMs:

```bash
vagrant up --provider=libvirt
```

## Acesso SSH

Após a VM subir:

```bash
vagrant ssh vm-01-data-core
```

## Parar e remover

```bash
vagrant halt
vagrant destroy -f
```

## Observações importantes

- O Vagrantfile usa Debian como base inicial por ser mais compatível no Fedora host.
- A VM é pensada para desenvolvimento local e não para produção.
- Os discos e arquivos temporários não devem entrar no git.
- Os volumes de libvirt e caches do Vagrant devem permanecer fora do repositório do projeto.

## Problemas conhecidos

O erro mais comum é:

```text
Cannot access storage file ... Permissão negada
```

Normalmente isso significa que:

- o usuário não está no grupo `libvirt`/`kvm`
- o diretório de imagens não tem permissões corretas
- o SELinux está bloqueando o acesso ao diretório do libvirt

A correção mais comum é:

```bash
sudo usermod -aG libvirt,kvm "$USER"
newgrp libvirt
newgrp kvm
sudo systemctl restart libvirtd
```

Depois tente novamente.
