# ai-jail: boas práticas do projeto

## Objetivo

Este documento define a política padrão do projeto para uso da ferramenta ai-jail em ambientes de desenvolvimento e prototipagem.

A regra central é simples:

- a IA deve operar em sandbox
- o ambiente do usuário não deve ser exposto automaticamente
- o escopo do repositório deve ser o limite máximo de acesso
- a configuração do projeto deve ser padronizada e compartilhada

## Política padrão do projeto

A configuração do ai-jail deve ser compartilhada por todos os membros do projeto e versionada no repositório.

Isso garante:

- mesma política de segurança para todos
- ausência de variação entre máquinas
- clareza de comportamento
- facilidade de revisão e manutenção

## Regras obrigatórias

### 1. Sandbox por projeto

Toda execução da IA em código do projeto deve ocorrer em um sandbox isolado.

- não rodar a IA em ambiente host livre
- não deixar o agente operar fora do escopo do repositório ativo
- usar um projeto ou diretório de trabalho específico como base de execução

### 2. Acesso mínimo

O agente deve receber apenas o que for estritamente necessário.

- mapear apenas o diretório do projeto
- evitar montar diretórios pessoais
- evitar herdar o ambiente completo do shell
- manter a rede desligada por padrão
- manter display, GPU, Docker e outros recursos sensíveis desativados por padrão

### 3. Segredos protegidos

Segredos nunca devem estar acessíveis ao agente por padrão.

- não montar credenciais do usuário
- não herdar variáveis sensíveis do ambiente do host
- ocultar ou negar caminhos de secrets e arquivos críticos
- mascarar arquivos como `.env`, `.env.*`, `*.pem`, `secrets/` e outros padrões sensíveis

### 4. Escrita controlada

Escrita deve ser limitada ao escopo do projeto.

- permitir escrita apenas no diretório do projeto atual
- proibir gravação em diretórios externos ao sandbox
- evitar criação de arquivos fora do escopo
- exigir revisão humana antes de aceitar mudanças críticas

### 5. Ambiente de prototipagem

Todos os experimentos devem começar dentro de um sandbox claramente definido.

- não misturar ambiente de prototipagem com ambiente de produção
- não usar repositórios compartilhados sem escopo definido
- manter um único padrão para todos os membros

## Configuração compartilhada

A configuração do ai-jail deve ser versionada no repositório, de preferência em um arquivo padronizado, como `.ai-jail`.

A política do repositório deve ser a política mínima obrigatória e não deve ser tornada mais permissiva localmente sem justificativa e revisão.

Qualquer ajuste deve respeitar estas regras:

- deve ser documentado
- deve ser revisado por outra pessoa
- deve ser versionado junto com o código ou documentação relevante
- não deve relaxar o sandbox sem justificativa explícita

## Quando usar

O ai-jail deve ser usado em qualquer caso em que a IA:

- execute comandos dentro do projeto
- possa ler ou gravar arquivos do repositório
- manipule scripts ou protótipos
- processa dados do projeto
- acessa conteúdo sensível ou informações de infraestrutura

## Quando evitar uso indevido

Não use o ai-jail para:

- ignorar a política de segurança do projeto
- expandir permissões sem motivo
- rodar IA fora do escopo do repositório
- expor host home, credenciais do usuário ou secrets locais
- transformar o sandbox em um ambiente sem limites

## Regras de operação para a equipe

Antes de iniciar qualquer execução da IA, o membro deve verificar:

- qual é o projeto em execução
- qual é o diretório mapeado
- se a rede está desligada
- se há arquivos sensíveis fora do escopo
- se o ambiente está de acordo com a política compartilhada

## Política de revisão

Toda mudança na configuração do ai-jail deve seguir o mesmo padrão de documentação e revisão do projeto.

A configuração compartilhada é parte da governança do projeto e não um ajuste pessoal do ambiente.

## Regra final

O objetivo do ai-jail no projeto não é permitir liberdade da IA, e sim garantir contenção, previsibilidade e segurança.

A IA deve ser útil, mas sempre dentro do mesmo conjunto de guardrails para todos os membros.
