# Escopo do projeto

## Contexto

O projeto datalake-doomsday nasce da necessidade de criar uma base de memória digital resiliente, capaz de preservar e consultar informação em condições de infraestrutura mínima, custo controlado e crescimento contínuo.

## Objetivo principal

Construir um data lake de baixo custo e alta resiliência para receber, guardar e consultar dados heterogêneos, mantendo contexto e metadados ricos.

## Escopo funcional

O projeto deve entregar:

- ingestão de dados diversos
- armazenamento bruto e preservado
- catálogo de arquivos e metadados
- organização por fontes, tipos e contexto
- consultas leves e acessíveis
- suporte a dashboards e visualização
- base para pesquisa e uso por IA

## Escopo operacional

O projeto deve operar com foco em:

- baixa complexidade inicial
- custos moderados ou baixos
- resiliência em ambientes limitados
- escalabilidade gradual
- manutenção simples

## Limites iniciais

O projeto não deve assumir, desde o início:

- cluster massivo
- infraestrutura de alta disponibilidade complexa
- processamento distribuído pesado
- schema rígido obrigatório para toda entrada

## Direção de evolução

O projeto deve crescer por camadas e módulos, começando com a parte mais importante: preservação do dado e catalogação de contexto.

A partir daí, será possível evoluir para:

- consultas analíticas
- dashboards
- extração de texto e metadados
- buscas contextualizadas
- uso de IA sobre o conhecimento do lake
