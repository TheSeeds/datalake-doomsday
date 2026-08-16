SHELL := /bin/bash
VAGRANT_DIR := tests/vms

.PHONY: up down destroy status provision ci ssh-vm-01 ssh-vm-02 ssh-vm-03 shell

up:
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant up --provision vm-01-data-core --provider=libvirt
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant up --provision vm-02-app-query --provider=libvirt
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant up --provision vm-03-ai-sandbox --provider=libvirt
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant ssh vm-01-data-core -c 'sudo docker compose -f /vagrant/infra/docker/vm-01/docker-compose.yml up -d'
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant ssh vm-02-app-query -c 'sudo docker compose -f /vagrant/infra/docker/vm-02/docker-compose.yml up -d'
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant ssh vm-03-ai-sandbox -c 'sudo docker compose -f /vagrant/infra/docker/vm-03/docker-compose.yml up -d'
	@echo "Ambiente do laboratório subiu com sucesso."

provision:
	@cd $(VAGRANT_DIR) && VAGRANT_DISABLE_NFS=1 vagrant provision

status:
	@cd $(VAGRANT_DIR) && vagrant status

down:
	@cd $(VAGRANT_DIR) && vagrant halt || true
	@echo "VMs pausadas com sucesso."

destroy:
	@cd $(VAGRANT_DIR) && vagrant destroy -f || true
	@echo "Ambiente destruído com sucesso."

ssh-vm-01:
	@cd $(VAGRANT_DIR) && vagrant ssh vm-01-data-core

ssh-vm-02:
	@cd $(VAGRANT_DIR) && vagrant ssh vm-02-app-query

ssh-vm-03:
	@cd $(VAGRANT_DIR) && vagrant ssh vm-03-ai-sandbox

ci:
	@ruby -c tests/vms/Vagrantfile
	@bash -n infra/provision/install-docker.sh
	@bash -n infra/provision/bootstrap-vm.sh
	@docker compose -f infra/docker/vm-01/docker-compose.yml config >/dev/null
	@docker compose -f infra/docker/vm-02/docker-compose.yml config >/dev/null
	@docker compose -f infra/docker/vm-03/docker-compose.yml config >/dev/null
	@echo "Validação do laboratório concluída com sucesso."
