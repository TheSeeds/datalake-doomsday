# datalake-doomsday

## Status do ambiente

Este repositório representa um ambiente de validação local, protótipo e laboratório de arquitetura.

Ele não é um ambiente de produção.

Todos os serviços, VMs, parâmetros e fluxos aqui documentados devem ser entendidos como:

- ambiente de teste
- ambiente de validação de MVP
- ambiente controlado para desenvolvimento e experimentação
- infraestrutura local sem compromisso de disponibilidade, operação crítica ou segurança de produção

## Visão geral

O projeto datalake-doomsday é uma proposta de data lake resiliente, de baixo custo e modular, pensado para preservar e organizar tudo que puder ser capturado em ambientes com infraestrutura mínima, pouca sofisticação operacional e necessidade de continuidade.

A ideia central é construir uma base de memória digital que possa sobreviver a limitações técnicas, falhas locais e restrições de recursos, mantendo o valor do dado mesmo quando a infraestrutura é simples ou degradada.

## Compromisso de software livre

Este projeto é 100% software livre e open source em sua essência.

Todos os componentes, módulos, scripts, documentação e padrões de desenvolvimento devem priorizar:

- código aberto
- transparência
- reuso comunitário
- ausência de lock-in de fornecedor
- compatibilidade com infraestrutura livre e acessível

O objetivo é manter o ecossistema sustentável, auditável e reutilizável por qualquer pessoa que queira prototipar, adaptar ou evoluir a ideia.

## Objetivo

O projeto busca criar uma estrutura para:

- coletar dados heterogêneos
- preservar o dado bruto
- catalogar metadados e contexto
- separar armazenamento, consulta e análise
- permitir crescimento gradual sem depender de um cluster pesado desde o início
- servir como base de conhecimento para análise e IA

## Filosofia

A filosofia do projeto é simples:

- preservar o máximo possível
- processar somente quando houver necessidade
- separar o que é dado bruto do que é dado útil
- manter metadados ricos e rastreáveis
- utilizar infraestruturas leves e acessíveis
- evoluir por camadas, não por complexidade prematura

## O que o projeto deve permitir

O sistema deve ser capaz de receber e organizar:

- textos e documentos
- registros e logs
- imagens e arquivos multimídia
- dados tabulares
- arquivos binários e outras fontes legíveis
- informações provenientes de sensores, máquinas e ambientes locais

## O que o projeto não é

Este projeto não é:

- um cluster Hadoop completo desde o começo
- uma solução de alto custo e alta complexidade
- um banco de dados rígido com schema obrigatório
- um sistema que depende de grande infraestrutura para funcionar

## Visão técnica

Em termos técnicos, o datalake-doomsday deve seguir uma arquitetura modular com:

- camada de ingestão
- camada de armazenamento bruto
- camada de metadados e catalogação
- camada de consulta leve
- camada de dashboards e visualização
- camada de IA e busca contextualizada

A ideia é que o projeto cresça em camadas, mantendo resiliência e custo sob controle.

## Declaração resumida

O datalake-doomsday é um data lake de baixo custo, resiliente e modular para preservar e organizar dados heterogêneos em infraestruturas mínimas, com foco em armazenamento bruto, catalogação, consulta e uso como base de conhecimento para análise e IA.

## Estrutura do repositório

- docs/: documentação interna do projeto
- src/: código e módulos principais
- infra/: infraestrutura e provisionamento
- sandbox/: ambiente isolado para prototipagem
- examples/: exemplos e experimentos
- .github/workflows/: validações automáticas do laboratório e da infraestrutura

## Validação automatizada do laboratório

O projeto inclui uma pipeline no GitHub Actions para validar a integridade do ambiente local de teste.

A validação automatizada cobre:

- sintaxe do Vagrantfile
- sintaxe dos scripts bash de provisionamento
- validação dos arquivos Docker Compose
- consistência dos arquivos essenciais do laboratório
- checagem simples de guardrails e postura do projeto

O workflow principal está em [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Fluxo operacional do laboratório

Este ambiente foi pensado para subir e destruir com comandos simples, sem depender de dezenas de etapas manuais.

### Subir tudo

```bash
make up
```

Este comando:

1. sobe as VMs com Vagrant + libvirt
2. provisiona o ambiente base
3. inicia o stack da VM-01 com MinIO e PostgreSQL

### Validar infraestrutura

```bash
make ci
```

Este comando executa a validação simples da estrutura do laboratório.

### Verificar status

```bash
make status
```

### Pausar tudo

```bash
make down
```

### Destruir tudo

```bash
make destroy
```

### Entrar em uma VM específica

```bash
make ssh-vm-01
make ssh-vm-02
make ssh-vm-03
```

## Como testar localmente

No repositório, você pode usar os comandos do Makefile ou executar a validação manual:

```bash
cd /home/cflb/Projetos/TheSeed/datalake-doomsday
ruby -c tests/vms/Vagrantfile
bash -n infra/provision/install-docker.sh
bash -n infra/provision/bootstrap-vm.sh
docker compose -f infra/docker/vm-01/docker-compose.yml config >/dev/null
docker compose -f infra/docker/vm-02/docker-compose.yml config >/dev/null
docker compose -f infra/docker/vm-03/docker-compose.yml config >/dev/null
```

## Como funciona a pipeline

A pipeline segue uma lógica simples:

1. valida a estrutura do laboratório
2. valida sintaxe e composição do código de infra
3. garante que os arquivos essenciais existam
4. confirma que o projeto mantém o modelo de laboratório local
5. em execução manual em runner self-hosted, também sobe a VM-01 e valida o Docker dentro dela

Este modelo mantém o ambiente seguro, rápido e útil para evolução controlada do projeto, sem transformar o GitHub Actions em um ambiente de produção.

## Política de operação

- o ambiente é local e de teste
- o objetivo é acelerar validação, não operar produção
- qualquer destruição deve ser intencional e explícita
- os comandos de provisionamento e destruição devem ser reproduzíveis e simples
