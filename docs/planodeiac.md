# Plano de IaC do datalake-doomsday

## Status geral

- [x] Definição da arquitetura em VMs
- [x] Separação entre isolamento e serviços
- [x] Definição da estratégia Docker + Compose
- [x] Documentação da abordagem local
- [x] Criação dos arquivos de infraestrutura (Vagrantfile, provision, compose por VM)
- [x] Provisionamento base das VMs (scripts install-docker.sh e bootstrap-vm.sh)
- [x] Implementação dos serviços MinIO / PostgreSQL / app de consulta (query-service e fallback vLLM)
- [ ] Implementação da VM de IA segura (ai-jail ainda é container "dummy"; falta integração real)
- [x] Testes automatizados de infraestrutura (CI estático + testes de unidade do query-service)

> Nota (2026-09-07): o MVP de ingestão, schema de PostgreSQL e DuckDB ainda não estão
> implementados de fato. O que existe é a camada de infra (VMs, Docker, MinIO, PostgreSQL)
> e a camada de consulta/IA (query-service + fallback vLLM), validada por testes de unidade.

## Objetivo do plano

Este plano deve evoluir com o projeto e registrar o que já foi definido, o que falta fazer e o que é prioridade.

## Prioridade imediata

1. Finalizar a infraestrutura local com Vagrant + libvirt
2. Garantir que as VMs consigam subir corretamente
3. Instalar Docker em cada VM
4. Provisionar a VM-01 com MinIO e PostgreSQL
5. Provisionar a VM-02 com ingestão e dashboard
6. Provisionar a VM-03 com ai-jail e IA leve
7. Validar fluxo de ingestão e consulta

## Entregáveis esperados

### Entregável 1: infraestrutura básica

- 3 VMs definidas
- rede privada local
- Docker instalado
- acesso SSH funcional

### Entregável 2: dados

- MinIO operacional
- PostgreSQL operacional
- persistência de metadados e dados brutos

### Entregável 3: aplicação

- app de ingestão funcional
- consultas por metadados
- dashboard simples

### Entregável 4: segurança

- ai-jail instalado e ativo
- regras de comando bloqueadas
- política de scripts e execução documentada

### Entregável 5: validação

- testes de smoke
- testes de integração
- Playwright para UI e fluxo do usuário

## Observações finais

A IaC do projeto precisa permanecer simples.

A arquitetura não deve ser convertida em um sistema grande antes da validação do MVP. O foco é manter o ambiente reproduzível e seguro, sem perder velocidade de desenvolvimento.
