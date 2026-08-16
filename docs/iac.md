# IaC do datalake-doomsday

## Visão geral

Este documento define a estratégia de infraestrutura como código (IaC) para o projeto.

Importante: esta infraestrutura é um ambiente de teste e laboratório local. Ela não representa produção.

O objetivo é validar arquitetura, fluxo, segurança e comportamento do MVP em um ambiente controlado, simples e reprodutível.

A filosofia do projeto é simples:

- VMs para isolamento e fronteira de segurança
- Docker para execução dos serviços dentro das VMs
- regras e políticas em código
- ambiente reproduzível e versionado
- testes automatizados como parte do processo

A infraestrutura precisa ser tratada como parte do produto, e não como uma etapa manual separada.

## Objetivo da estratégia IaC

A IaC deve permitir que qualquer membro do projeto consiga:

- criar as VMs de forma reprodutível
- instalar o mínimo necessário em cada VM
- provisionar os serviços com consistência
- repetir o ambiente localmente sem depender de configurações manuais dispersas
- evitar drift de infraestrutura
- reduzir possibilidade de erro humano

## Princípios

### 1. Isolamento por VM

Cada VM deve ter um papel bem definido:

- VM-01: data-core
- VM-02: app-query
- VM-03: ai-sandbox

A separação de responsabilidades é parte da segurança e da clareza do desenho.

### 2. Docker dentro das VMs

As VMs não precisam rodar todos os serviços “na máquina host”. O ideal é que cada VM tenha Docker e rodar os serviços necessários como containers.

Isso traz:

- menor acoplamento entre serviços
- implantação mais simples
- rollback mais fácil
- reutilização de definições de serviço

### 3. Código como fonte de verdade

Toda mudança de infraestrutura deve ser rastreada por versionamento Git.

Isso inclui:

- Vagrantfile
- scripts de provisionamento
- arquivos de ambiente
- compose files
- regras de segurança
- policies de AI e operação

### 4. Segurança integrada

A IaC deve refletir as regras do projeto.

Isso inclui:

- rede privada entre VMs
- acesso mínimo por serviço
- uso de TLS
- segredos fora do código
- sandbox para IA
- aprovação humana antes de ações destrutivas

## Estrutura proposta

```text
infra/
  vms/
    Vagrantfile
    scripts/
  docker/
    vm-01/
      docker-compose.yml
    vm-02/
      docker-compose.yml
    vm-03/
      docker-compose.yml
  ansible/
    inventory/
    playbooks/
    roles/
  security/
    policies/
    ai-jail/
```

## Arquitetura de aplicação e infraestrutura

### VM-01: data-core

Função:

- MinIO
- PostgreSQL
- backups
- criptografia
- persistência de dados brutos e metadados

Tecnologia:

- Debian
- Docker + Compose
- MinIO
- PostgreSQL
- backup automatizado

### VM-02: app-query

Função:

- ingestão
- processamento leve
- consulta
- dashboard
- APIs internas

Tecnologia:

- Debian
- Docker + Compose
- Python app
- DuckDB
- dashboard

### VM-03: ai-sandbox

Função:

- execução segura de IA
- extração de contexto
- processamento isolado
- acesso controlado

Tecnologia:

- Debian
- Docker + Compose
- ai-jail
- modelo leve
- serviços exclusivos de processamento

## Estratégia de rede

As VMs devem comunicar-se em rede privada, de forma controlada.

Padrão recomendado:

- VM-01: 192.168.56.10
- VM-02: 192.168.56.11
- VM-03: 192.168.56.12

A comunicação deve ser:

- VM-02 -> VM-01 para leitura e ingestão
- VM-03 -> VM-01 somente quando estritamente necessário
- isolamento da VM-03 por padrão
- regras de firewall e portas limitadas

## Provisionamento base

Cada VM deve ser provisionada com o mínimo necessário:

- usuário operacional do projeto
- Docker instalado
- usermod para acesso ao docker
- SSH habilitado
- cron/backup mínimos
- ferramenta de monitoramento leve
- firewall básico

## Provisionamento com IaC

A forma recomendada é:

- Vagrant para criar as VMs
- Ansible para provisionar cada VM
- Docker Compose para orquestrar serviços em cada VM

Isso separa responsabilidades:

- Vagrant: cria máquina
- Ansible: configura sistema
- Compose: executa serviços

## Segurança na IaC

As regras de segurança devem fazer parte do provisionamento.

Regras mínimas:

- TLS para comunicação entre serviços
- chaves fora do código-fonte
- permissões mínimas por serviço
- log sem segredos
- rede privada entre VMs
- ai-jail obrigatório para qualquer processamento IA
- nenhuma ação destrutiva sem explicitação de risco e aprovação humana

## Testes de infraestrutura

A infraestrutura também precisa de testes.

Exemplos:

- verificar se a VM inicializa corretamente
- verificar se o serviço Docker está ativo
- verificar se o container MinIO responde na porta esperada
- verificar se o PostgreSQL aceita conexão
- verificar se a IA sandbox bloqueia comandos proibidos
- verificar fluxo de ingestão

O uso de Playwright pode ser integrado para validação de fluxo de usuário e frontend, mas a infraestrutura mínima também precisa de testes automatizados simples.

## Regras do projeto para IaC

- não usar configurações manuais persistentes em sessão local
- não versionar volumes, discos, imagens geradas por VMs
- não versionar arquivos temporários, logs e snapshots locais
- sempre documentar mudanças na infra em commit separado
- manter a documentação alinhada com o código

## Conclusão

A infraestrutura do datalake-doomsday deve ser tratada como software.

O desenho esperado é:

- VM isolada por função
- Docker como execução dos serviços
- IaC como padrão da operação
- segurança e testes como requisito de projeto, não como item extra

Assim, a plataforma fica simples, reprodutível e coerente com a visão do projeto.
