# Estado validado do laboratório

## Visão geral

Este documento registra o estado funcional que foi validado no laboratório local do projeto. Ele representa a linha de base que ficou estável após ajustes de infraestrutura, provisionamento e compatibilidade de runtime.

O objetivo aqui não é a solução de produção, e sim o ambiente de prova de conceito local para validar:

- separação funcional por VM
- armazenamento bruto e metadados
- camada de consulta
- acesso a uma IA mínima e compatível com APIs OpenAI
- fluxo end-to-end entre dados, consulta e resposta da IA

## Arquitetura validada

A arquitetura final validada foi a seguinte:

- VM-01: camada de dados e catálogo
  - MinIO para armazenamento bruto
  - PostgreSQL para metadados e contexto

- VM-02: camada de aplicação e consulta
  - serviço Python para receber consultas
  - integração com a camada de IA local
  - endpoint HTTP para consulta

- VM-03: sandbox de IA local
  - serviço mínimo compatível com OpenAI
  - resposta em JSON para /v1/chat/completions
  - fallback local em Python para manter a cadeia funcionando

## Por que esta arquitetura foi escolhida

A abordagem inicial com um stack mais pesada de vLLM não se encaixou bem no ambiente local de validação: exigia mais recursos, mais complexidade operacional e falhava em compatibilidade com o runtime disponível no laboratório.

Foi então adotado um modelo mínimo e funcional, com foco em prova de conceito e integração real do fluxo de consulta, em vez de tentar reproduzir uma stack de IA pesada de produção.

## Fluxo funcional validado

1. A requisição entra no serviço da VM-02.
2. O query-service prepara a solicitação em formato JSON compatível.
3. A VM-03 responde em um endpoint OpenAI-like.
4. O resultado volta para o cliente com resposta textual.
5. A cadeia inteira foi testada em HTTP real.

## Endpoints validados

Os endpoints que estiveram ativos no laboratório e foram validados com sucesso incluem:

- VM-03: /v1/models
- VM-02: /health
- VM-02: /query

A validação real retornou uma resposta de modelo e uma resposta de consulta verdadeira, demonstrando que a integração entre os serviços está funcionando.

## Observações importantes

- O ambiente é local, controlado e experimental.
- Não é uma infraestrutura de produção.
- A rede utilizada é privada e local, com IPs de laboratório.
- Não devem ser armazenados segredos reais, tokens, chaves privadas ou dados sensíveis no repositório.
- Qualquer valor de senha ou token deve ser substituído por placeholders, variáveis de ambiente locais ou configuração fora do código.

## Política de segurança aplicada ao repositório

Antes de registrar qualquer mudança no código, foram observadas as seguintes regras:

- não incluir segredos reais
- não incluir tokens ou chaves pessoais
- não registrar dados sensíveis do host ou da VM
- manter arquivos de ambiente fora do código-fonte
- usar apenas exemplos ou valores locais de laboratório

## Regra de uso do laboratório

Este ambiente foi montado para:

- entender o desenho da arquitetura
- validar a separação entre dados, consulta e IA
- provar que a integração funciona sem complexidade excessiva
- servir como base para evolução posterior

Não deve ser usado como ambiente de produção, operação crítica ou armazenamento de dados reais sensíveis.

## Resumo do estado atual

O laboratório está em um estado funcional e documentado como:

- arquitetura mínima por VM
- serviços isolados por função
- integração com IA local compatível com OpenAI
- validação real de HTTP funcionando
- documentação e guardrails alinhadas ao objetivo de laboratório

Este conjunto representa a linha de base que foi preservada no repositório para continuar evoluindo com segurança e sem comprometer dados sensíveis.
