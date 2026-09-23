# Plano de execução do escopo inicial

## Visão geral

Este documento registra o plano inicial de execução do projeto datalake-doomsday e funciona como uma linha do tempo viva de decisões, objetivos e entregas.

Ele deve ser versionado e atualizado de forma contínua conforme o projeto evolui.

## Objetivo do plano

O plano tem como objetivo manter clareza sobre:

- o que o projeto está tentando construir
- quais módulos fazem parte do escopo inicial
- quais decisões foram tomadas
- o que já foi validado
- o que vem em seguida
- o que precisa ser revisado antes de avançar

## Regra de evolução

Este documento não é estático.

Sempre que uma decisão, mudança de arquitetura ou nova prioridade surgirem, o plano deve ser atualizado com:

- data da mudança
- descrição da mudança
- motivo
- impacto no escopo
- next steps

## Estado geral do projeto

Use o checklist abaixo para marcar o que já foi concluído e o que ainda está pendente.

## Checklist do escopo inicial

- [x] definição da visão do projeto
- [x] definição do nome e conceito do projeto
- [x] documentação central do guarda-chuva TheSeed
- [x] criação do repositório datalake-doomsday
- [x] criação da documentação interna do projeto
- [x] definição do escopo inicial do projeto
- [x] definição da arquitetura em camadas
- [x] definição das guardrails do projeto
- [x] documentação da política de software livre e open source
- [x] criação da política de uso do ai-jail
- [x] criação do plano de execução versionado
- [x] decisão do modelo de infraestrutura em 3 VMs
- [x] definição da arquitetura técnica do lake em camadas
- [x] definição da stack inicial recomendada
- [ ] protótipo de ingestão mínima
- [ ] protótipo de armazenamento bruto em MinIO (infra montada; falta ingestor e schema)
- [ ] protótipo de metadados e catálogo em PostgreSQL
- [ ] protótipo de consulta leve em DuckDB
- [ ] dashboard mínimo de métricas
- [ ] integração segura de IA com sandbox (query-service validado; ai-jail real pendente)
- [x] camada de consulta e fallback local (query-service + fallback vLLM), validada por testes de unidade
- [ ] revisão do MVP e documentação de operação

## Escopo inicial

O escopo inicial do projeto inclui:

1. preservação do dado bruto
2. organização por metadados e contexto
3. separação entre armazenamento, catálogo e consulta
4. uso de infraestrutura leve e escalável por camadas
5. suporte para consulta analítica simples
6. uso futuro como base de conhecimento para IA

## Fase 1: definição da base do projeto

### Objetivos

- consolidar a visão do projeto
- estabelecer documentação central e interna
- fixar as regras de software livre e segurança
- definir o escopo do primeiro protótipo

### Entregáveis

- visão do projeto
- escopo inicial
- arquitetura em camadas
- guardrails do projeto
- política de uso do ai-jail

### Status

Concluído.

## Fase 2: arquitetura do lake

### Objetivos

- definir a separação entre armazenamento bruto, metadados e consulta
- decidir como a ingestão deve acontecer
- estabelecer regras para organização por categoria e origem
- decidir a estratégia inicial de custo e armazenamento
- fixar o padrão de 3 VMs como referência operacional

### Entregáveis esperados

- diagrama de camadas
- política de ingestão
- regras de catalogação
- níveis de armazenamento: bruto, quente, frio e archive
- desenho da distribuição de responsabilidades por VM

### Status

Concluído em parte, com modelo de infraestrutura definido.

## Fase 3: protótipo funcional mínimo

### Objetivos

- montar um protótipo funcional com ingestão mínima
- validar a organização de arquivos e metadados
- testar consulta leve e indexação simples
- validar a lógica em sandbox

### Entregáveis esperados

- protótipo funcional de ingestão
- estrutura mínima de armazenamento
- metadados básicos por arquivo
- consulta simples por categoria e origem

### Status

Pendente.

## Fase 4: dashboards e visualização

### Objetivos

- transformar dados em indicadores úteis
- permitir percepção de contexto e uso do conteúdo
- validar visualização de conhecimento mínimo

### Entregáveis esperados

- painéis simples
- visualização de métricas básicas
- exploração por fontes e categorias

### Status

Pendente.

## Fase 5: IA e base de conhecimento

### Objetivos

- extrair texto e metadados
- preparar o lake para ser consultado por IA
- criar uma camada de busca contextualizada
- validar uso de IA como apoio de descoberta e análise

### Entregáveis esperados

- mecanismo de extração textual
- índice de busca por contexto
- política de acesso para IA
- integração segura com o sandbox e guardrails

### Status

Pendente.

## Decisões estratégicas já assumidas

- o projeto é 100% software livre e open source
- o foco inicial é arquitetura em camadas, não cluster pesado
- todo dado bruto deve ser preservado
- metadados e catálogo são prioritários
- protótipos devem operar em sandbox
- o ai-jail deve ser usado como camada de contenção para execução de IA

## Riscos principais

- crescimento descontrolado de dados sem metadados
- excesso de complexidade antes da necessidade
- ignorar a separação entre dados crus e processados
- permitir acesso amplo demais à execução da IA
- misturar protótipo com produção

## Práticas de evolução do plano

Cada nova mudança deve ser adicionada ao plano em formato de registro, com:

- data
- objetivo
- decisão
- impacto no escopo
- próximos passos
- responsável, quando aplicável

## Registro de mudanças

### 2026-09-07

- revisão geral do projeto
- testes de unidade do query-service e fallback vLLM (10 testes, pytest)
- credenciais de MinIO/PostgreSQL movidas a variáveis de ambiente (fora do código-fonte)
- modelo de IA configurável via `MODEL_NAME` (padrão: Qwen2.5-0.5B-Instruct)
- fallback real no query-service quando o endpoint principal falha
- adição de `requirements-dev.txt`, `pytest.ini` e job de testes no CI
- atualização dos checklists de plano e IaC ao estado real do repositório

### 2026-08-15

- criação do plano de execução inicial
- definição do escopo do projeto
- consolidação da documentação base
- definição das guardrails e sandbox para IA
- criação do checklist de execução e definição de status
- definição do modelo de infraestrutura em 3 VMs
- definição da arquitetura técnica do lake em camadas
- escolha da stack inicial recomendada
- atualização do plano para refletir a fase de implementação do MVP

## Próximas ações prioritárias

A sequência imediata do projeto é esta:

1. criar a estrutura inicial do repositório para o MVP
2. preparar o ambiente de infraestrutura em 3 VMs
3. instalar e configurar MinIO na VM 1
4. preparar o banco PostgreSQL na VM 1 com schema de metadados
5. criar a ingestão mínima em Python na VM 2
6. integrar leitura básica com DuckDB na VM 2
7. criar dashboard simples de métricas na VM 2
8. validar a execução da IA e processamento em sandbox na VM 3
9. aplicar checklist de segurança da IA antes de qualquer operação de automação
10. bloquear qualquer comando destrutivo sem autorização explícita e declaração de risco
11. revisar o MVP e documentar o fluxo operacional
12. registrar tudo em documentação versionada e manter o plano atualizado

## Memória operacional imediata

- prioridade atual: transformar a arquitetura em implementação prática
- objetivo do próximo ciclo: montar o MVP funcional de ingestão, armazenamento e catálogo
- padrão adotado: 3 VMs separadas por função
- regra: não avançar para IA antes da base funcional do lake estar validada

## Convenção de status

- [x] concluído
- [ ] pendente
- [ ] em revisão

Sempre que uma etapa for concluída, basta marcar o item no checklist e registrar a atualização no histórico de mudanças.
