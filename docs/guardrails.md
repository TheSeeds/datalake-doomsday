# Guardrails do projeto

## Objetivo

As guardrails definem os limites e regras do projeto datalake-doomsday para manter segurança, estabilidade, clareza e evolução controlada.

Este projeto é 100% software livre e open source. Portanto, todo desenvolvimento, infraestrutura, documentação e padrão de uso devem seguir princípios de transparência, reutilização e interoperabilidade.

## Princípios centrais

- preservar o dado bruto
- catalogar antes de transformar
- limitar processamento, não coleta
- separar dados crus, metadados e consulta
- manter custo baixo e arquitetura simples
- isolar protótipos e experimentos em sandbox
- evitar dependência de tecnologias fechadas quando houver alternativa livre

## Segurança

- nunca expor segredos em repositórios públicos
- usar variáveis de ambiente para dados sensíveis
- separar ambiente de desenvolvimento, teste e produção
- proteger acessos a redes internas, APIs e repositórios externos
- não misturar dados sensíveis com dados de prototipagem

## Isolamento e sandbox

Todo experimento novo deve iniciar em um ambiente isolado.

Regras:

- cada protótipo deve ter seu próprio escopo
- cada ambiente deve ter acesso mínimo necessário
- não deve haver acesso livre ao sistema completo
- leitura e escrita devem ser limitadas ao diretório do projeto ou sandbox configurado
- a IA e automações devem operar dentro do escopo autorizado

## Governança do dado

- todo dado deve ter origem, tipo e contexto
- o dado bruto deve permanecer preservado e imutável
- metadados precisam ser ricos e rastreáveis
- dados sensíveis devem ter classificação clara
- retained data deve estar alinhado com política de retenção e descarte

## Arquitetura e custos

- não montar cluster pesado antes da necessidade
- separar armazenamento, processamento e consulta
- preferir soluções simples e baratas para começar
- escalar somente quando houver demanda real
- manter o design modular

## Software livre e open source

- priorizar ferramentas com licença aberta
- evitar dependência de tecnologia proprietária como requisito principal
- manter documentação pública e revisável
- promover interoperabilidade e reuso
- garantir que o projeto possa ser reproduzido por terceiros

## IA e automação

- IA e automação só devem agir em área autorizada
- qualquer mudança relevante deve ser validada por humanos
- não automatizar operações críticas sem checkpoints
- não permitir que a IA acesse dados fora do sandbox definido
- separar experimentação de produção

## Qualidade e validação

- qualquer nova funcionalidade deve ter validação mínima
- protótipos precisam passar por testes de integridade básica
- mudanças em ingestão, metadados e consultas devem ser revisadas antes de escalar
- a documentação deve acompanhar a evolução do projeto

## Regras de contribuição

- toda mudança deve ser documentada
- toda decisão relevante deve ser explicada na documentação
- nomes, módulos e estruturas devem ser claros e consistentes
- mudanças grandes devem ser discutidas antes da implementação

## Regra final

O projeto deve crescer com clareza, segurança e disciplina, nunca com improviso.

Se a solução não tiver escopo definido, governança clara ou sandbox apropriado, ela não deve entrar em produção ou em uso amplo.
