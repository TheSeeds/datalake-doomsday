# Infraestrutura local (laboratório)

Este diretório concentra a infraestrutura como código para o ambiente local de teste do datalake-doomsday.

Importante:
- este ambiente é de laboratório e validação
- não é produção
- os serviços aqui usados devem ser simples, reprodutíveis e fáceis de destruir

## Estrutura

- `provision/`: scripts de bootstrap do sistema base
- `docker/`: arquivos Docker Compose por VM

## Ordem recomendada

1. Criar as VMs com Vagrant
2. rodar `install-docker.sh` dentro de cada VM Debian
3. iniciar os serviços com Docker Compose em cada VM
4. validar fluxo de ingestão e consulta
5. aplicar segurança e sandbox

## Script base

O script `provision/install-docker.sh` instala o Docker Engine e o plugin Compose no Debian.

## Observações

- use contas locais e segredos de teste
- não versionar dados reais
- manter tudo em ambiente controlado
- usar o `ai-jail` na VM-03 para qualquer operação de IA
