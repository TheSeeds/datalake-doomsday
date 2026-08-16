# Arquitetura do projeto

## Visão geral

A arquitetura do datalake-doomsday deve seguir um modelo em camadas, separando armazenamento, catálogo, consulta e conhecimento.

## Compromisso de arquitetura aberta

A arquitetura deste projeto deve ser 100% compatível com software livre e open source.

Isso significa:

- evitar dependências proprietárias onde não for necessário
- priorizar ferramentas com licença aberta
- manter módulos reutilizáveis e auditáveis
- garantir que a solução possa ser reproduzida em ambientes livres
- favorecer interoperabilidade e transparência técnica

## Camadas propostas

### 1. Ingestão

Responsável por receber dados de diferentes fontes e formatos.

Inclui:

- arquivos locais
- documentos
- logs
- mídia
- dados estruturados e semiestruturados
- dados de sensores e ambientes locais

### 2. Armazenamento bruto

Responsável por preservar o dado original com integridade e rastreabilidade.

Objetivos:

- preservar tudo que puder ser capturado
- manter integridade por hash e metadados
- separar dados crus de dados processados
- permitir retenção por categoria e valor

### 3. Metadados e catalogação

Responsável por organizar o contexto do dado.

Deve registrar:

- origem
- tipo
- data de coleta
- formato
- hash
- categoria
- tags
- status de processamento
- política de retenção

### 4. Consulta e acesso

Responsável por permitir leitura analítica e contextualizada.

Pode incluir:

- consultas leves
- leitura estruturada
- indexação por texto
- filtros por categoria e origem
- acesso por tema e contexto

### 5. Visualização e dashboards

Responsável por transformar os dados em visão útil.

Inclui:

- métricas
- indicadores
- exploração por contexto
- painéis operacionais
- análise de tendências

### 6. IA e base de conhecimento

Responsável por preparar o lake para uso por IA e busca semântica.

Inclui:

- extração de texto
- indexação de conteúdo
- busca contextualizada
- resumos e análise de conhecimento
- apoio à decisão e exploração

## Princípio arquitetural

O projeto deve ter uma arquitetura que separe claramente:

- dado bruto
- metadados
- consulta
- análise
- conhecimento

Isso reduz acoplamento, custo e riscos operacionais.

## Direção arquitetural

A arquitetura deve priorizar:

- simplicidade inicial
- baixo custo
- resiliência
- escalabilidade modular
- compatibilidade com uso futuro por IA
