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
- tratar criptografia como requisito obrigatório, não como opcional

## Criptografia

A criptografia deve ser tratada como requisito de arquitetura e não como camada acessória.

### Regras mínimas

- todo tráfego entre serviços deve usar TLS 1.2 ou superior
- todo dado em repouso deve ser cifrado em disco ou em storage
- qualquer armazenamento de dados sensíveis deve usar criptografia forte, preferencialmente AES-256
- backups e snapshots também devem ser cifrados
- chaves e segredos devem ser gerenciados fora do código-fonte e fora de logs
- nenhum dado sensível deve ficar em texto puro em arquivos temporários, dumps ou logs
- qualquer integração com serviços externos deve exigir autenticação e cifragem no transporte

### Política do projeto

- dados sensíveis devem ter classificação clara e política de retenção
- acesso a dados cifrados deve exigir autorização explícita
- a rotação de chaves deve ser planejada e documentada
- a infraestrutura deve priorizar soluções com cifragem por padrão
- se uma funcionalidade exigir acesso a dados protegidos, a solução precisa documentar como a criptografia será preservada

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

## Sandbox de execução para IA: ai-jail

Para reforçar a proteção da execução de agentes de IA, este projeto usará a ferramenta ai-jail como camada de sandbox do sistema operacional.

A responsabilidade do ai-jail não é substituir a arquitetura de segurança do projeto, mas complementar a defesa do ambiente em que a IA opera.

### O que compete a esta ferramenta

O ai-jail é responsável por limitar o que o agente de IA pode acessar durante a execução. Em prática, ele cuida de:

- isolar o processo em um ambiente controlado
- limitar acesso ao sistema de arquivos do host
- impedir leitura ou escrita indiscriminada em diretórios fora do escopo
- não montar automaticamente o ambiente completo do usuário
- suprimir acesso a credenciais e secrets por padrão
- bloquear capacidades sensíveis como rede, GPU, display, SSH, Docker e IPC do host por padrão
- reduzir o risco de fuga de dados e execução não autorizada

Em outras palavras, o ai-jail cobre a parte de execução segura do agente de IA: sandbox, isolamento, perfil de acesso e contenção do ambiente.

### O que não compete a esta ferramenta

O ai-jail não substitui:

- governança do dado
- políticas de retenção e descarte
- separação entre ambiente de desenvolvimento e produção
- revisão humana de mudanças importantes
- catalogação e metadados do lake
- regras internas de acesso ao projeto

Essas responsabilidades continuam sendo do projeto e da arquitetura do datalake-doomsday.

### Como vamos usar

A ferramenta será usada em todos os cenários em que uma IA for autorizada a operar em código, arquivos ou protótipos do projeto.

Padrão recomendado:

- rodar a IA em sandbox por projeto
- mapear apenas o diretório do repositório ou do sandbox relevante
- manter a rede desligada por padrão
- manter credenciais e ambiente do sistema host fora do sandbox
- mascarar ou negar caminhos sensíveis e arquivos secretos
- usar acesso somente leitura para áreas de referência
- permitir escrita somente no escopo do projeto ativo
- validar manualmente qualquer alteração relevante antes de aceitar

### Política de uso no projeto

O uso do ai-jail será obrigatório para:

- qualquer agente de IA executando comandos dentro do repositório
- qualquer execução que manipule arquivos de projeto
- qualquer tarefa que possa criar, editar ou remover conteúdo sensível
- qualquer protótipo em sandbox ou ambiente de teste

O uso do ai-jail será opcional apenas para leitura passiva e análise documental em ambiente estritamente controlado, quando o escopo for conhecido e a segurança estiver explicitamente validada.

### Regra prática

A IA pode operar, mas só em um ambiente controlado e limitado. O ai-jail é a camada de contenção da execução; o projeto continua sendo responsável pela arquitetura, governança e decisões humanas.

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
