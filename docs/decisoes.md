# Decisões de arquitetura (ADR)

Registro formal das decisões do datalake-doomsday. Cada entrada traz o contexto,
a decisão, a **alternativa rejeitada** e a consequência. Sem a alternativa
rejeitada, um ADR é só uma afirmação — quem ler em 2027 não sabe o que foi
considerado e descartado.

Formato: ADR curto, numerado, imutável. Mudança de rumo gera **novo** ADR que
substitui o anterior, nunca edição do texto antigo.

Este arquivo vive no repositório de **conceito**. O que é operacional
(`plano-atividades.md`, charts, código) vive em `datalake-doomsday-env`.

**Estado de execução** (o que já está pronto, onda por onda) não se registra
aqui — fica em
[`datalake-doomsday-env › docs/plano-atividades.md`](https://github.com/TheSeeds/datalake-doomsday-env/blob/main/docs/plano-atividades.md).
ADR registra **decisão**, com a alternativa rejeitada; o plano registra
**andamento**, com a prova executável. Misturar os dois faz um ADR virar
diário e perder a função.

| ADR | Título | Status |
|---|---|---|
| [001](#adr-001) | microk8s como orquestrador único | aceita |
| [002](#adr-002) | Ubuntu Server 24.04 como Tier 1 de homologação | aceita |
| [003](#adr-003) | Garage como object store, em DaemonSet | aceita |
| [004](#adr-004) | Três buckets com ciclos de vida distintos | aceita |
| [005](#adr-005) | `replication_factor` decidido antes de haver dado | aceita |
| [006](#adr-006) | Snap `classic`, nunca `strict` | aceita |
| [007](#adr-007) | Núcleo de domínio puro (`lakecore`) separado do encanamento | aceita |
| [008](#adr-008) | Dois repositórios: conceito e ambiente | aceita |
| [009](#adr-009) | Apache 2.0 | aceita |
| [010](#adr-010) | Piso de VRAM em vez de flag booleana de GPU | aceita |
| [011](#adr-011) | Três camadas de acesso independentes | aceita |
| [012](#adr-012) | Módulo `ingestion`, função `ingest()` — nunca o mesmo nome | aceita |

---

## ADR-001

**microk8s como orquestrador único**

**Contexto.** O modelo anterior era 3 VMs com Vagrant + libvirt + Docker Compose.
O objetivo mudou: o projeto passa a ser um **modelo conceitual implantável** em
hardware diverso, incluindo máquinas modestas e cenários sem internet.

**Decisão.** microk8s como único orquestrador, single-node na v1, com caminho de
crescimento por adição de nó. Snap oficial, canal `1.35/stable` pinado.

**Alternativas rejeitadas.**
- *k3d* — é o que já roda no geoflow, mas **flannel não impõe NetworkPolicy**
  (medido no M2.5 do geoflow). A camada de acesso da arquitetura deixaria de ser
  enforcement e viraria diagrama.
- *kind / kubeadm* — sem caminho de airgap oficial nem addons homologados.
- *Docker Compose puro* — satisfaria o hardware mínimo, mas não daria RBAC nem
  NetworkPolicy, que são requisito de "camadas de acesso".
- *HashiCorp Nomad* — binário único e elegante, mas o ecossistema de charts
  pronto é menor, e o custo de adaptar tudo seria maior que o ganho.

**Consequência.** microk8s já estava rodando nesta máquina (v1.31.14, 2 anos de
uptime): custo de adoção zero. Em troca, a homologação fica acoplada à matriz da
Canonical (ADR-002). `1.31` saiu da janela de suporte — o pin é obrigatório.

---

## ADR-002

**Ubuntu Server 24.04 como Tier 1 de homologação**

**Contexto.** O host de desenvolvimento é Fedora 42, com **SELinux Enforcing e
AppArmor inativo**. O snap do microk8s depende de AppArmor para confinamento.

**Decisão.** Quatro níveis explícitos: Tier 1 = Ubuntu Server 24.04 (único alvo de
release, `verify.sh` verde sem rede); Tier 2 = 26.04; Tier 3 = Fedora (dev, não
homologado); não suportado = arm64/Pi/macOS.

**Alternativas rejeitadas.**
- *Homologar no Fedora* — funciona, mas a confinação nunca é exercida nas mesmas
  condições, e a Canonical descreve suporte fora do Ubuntu como "best-effort".
- *Não declarar matriz* — é o estado atual do repositório: 13 fatos errados na
  doc, porque nada era medido contra um alvo definido.

**Consequência.** Regra operacional: **o que quebra no Fedora não é bug do
projeto, é desvio de matriz. Se quebrar no Ubuntu, é bug.** Isso evita meses
depurando idiossincrasia de distro.

---

## ADR-003

**Garage como object store, em DaemonSet**

**Contexto.** O desenho original usava MinIO. O repositório `minio/minio` foi
**arquivado**, sem binários pré-compilados para a community, e o console perdeu
as funções de administração. Um lake que promete preservação por décadas não pode
depender de um daemon sem manutenção.

**Decisão.** Garage (Deuxfleurs, AGPLv3), deployado como **DaemonSet com
`hostPath`**, separando `meta` (SSD, 5–10 GiB) de `data` (resto).

**Alternativas rejeitadas.**
- *`pgsty/silo`* (fork do MinIO) — drop-in e com console de volta, mas AGPL e
  mantido por um único grupo.
- *SeaweedFS* — Apache-2.0 e maduro, operação mais complexa do que o problema pede.
- *Filesystem + PVC puro* — o mais honesto em hardware mínimo, mas sem S3 não há
  como delegar acesso por prefixo (ADR-011 depende disso).

**Consequência.** DaemonSet é a tradução direta de "adicionar nó = adicionar
capacidade": todo nó novo já sobe com instância Garage, faltando apenas
`layout assign` + `apply`. Com StatefulSet seria preciso dimensionar réplicas e
afinidade a cada nó.

**Pegadinha registrada.** O chart Helm **não** configura o cluster layout. Sem
`garage layout assign` + `apply`, o cluster sobe todo verde e **não armazena
nada**. É falha silenciosa e precisa de teste próprio.

---

## ADR-004

**Três buckets com ciclos de vida distintos**

**Contexto.** "Guardar tudo para sempre" e "poder apagar para liberar espaço" são
requisitos contraditórios. Misturá-los num bucket só torna impossível saber o que
é seguro deletar.

**Decisão.** `raw/` (imutável, nunca apagar), `derived/` (Parquet, regenerável,
pode ser apagado inteiro), `backup/` (retenção definida por rotação).

**Alternativa rejeitada.** Um bucket único com prefixos — mais simples de operar,
mas qualquer política de retenção vira uma expressão frágil de prefixos, e um
erro apaga o ativo junto com o derivado.

**Consequência.** Layout determinístico no `raw`:
`{origem}/{tipo}/{YYYY}/{MM}/{DD}/{sha256}`. O hash como nome de objeto faz a
escrita ser idempotente por construção — duas ingestões do mesmo conteúdo
disputam a mesma chave.

---

## ADR-005

**`replication_factor` decidido antes de haver dado**

**Contexto.** O Garage **não permite** alterar o `replication_factor` com dado
dentro: exige apagar o cluster layout e rebalancear tudo, com indisponibilidade.

**Decisão.** A decisão é pré-requisito da Onda 4, está registrada no plano (§10) e
o dashboard expõe alerta enquanto `rf=1`.

**Alternativas rejeitadas.**
- *Decidir depois* — tecnicamente possível, operacionalmente é uma migração
  destrutiva disfarçada de configuração.
- *`rf=3` desde o início* — exige 3 nós; com 1 nó o cluster não forma layout válido.

**Consequência, e é a frase mais importante deste documento:**

> Um lake single-node com `rf=1` **não é um lake doomsday** — é um lake de
> preparação. Enquanto não houver 3 nós, `raw/` não deve conter nada
> insubstituível.

Aritmética que precisa aparecer na doc, não ser descoberta depois: `rf=3` em 3 nós
de 500 GB = **1,2 TB brutos, 400 GB úteis**. A redundância custa 2/3 do bruto.

---

## ADR-006

**Snap `classic`, nunca `strict`**

**Contexto.** O microk8s tem canal estritamente confinado (`1.3x-strict`).

**Decisão.** `install.sh` instala `--classic` e **recusa** rodar contra um snap
`*-strict`.

**Alternativa rejeitada.** Strict por segurança — mas bloqueia workloads que
exigem shared mount com o host, e os addons afetados incluem **`gpu`**, que é
justamente o eixo que precisa ficar disponível (ADR-010).

**Consequência.** O instalador valida a confinação antes de prosseguir e falha com
mensagem explícita. Confinamento mais fraco é o custo aceito por GPU funcional.

---

## ADR-007

**Núcleo de domínio puro (`lakecore`) separado do encanamento**

**Contexto.** A lição do geoflow: lógica de negócio enterrada dentro de um Job
de Kubernetes é testável só com cluster no ar, e a suíte demora minutos.

**Decisão.** `lakecore` recebe `path` e devolve `Record`. **Não conhece** HTTP,
S3, PostgreSQL ou Kubernetes. Nenhuma dependência externa — só stdlib.

**Alternativa rejeitada.** Implementar tudo no `ingest-api` — mais rápido no
primeiro dia, e depois cada bug exige ambiente completo para reproduzir.

**Consequência.** `make test` roda em milissegundos, sem container e sem rede. As
ondas 0–2 rodam com o cluster desligado. As portas (`Catalog`, `ObjectStore`,
`Clock`) são `Protocol`, não ABC: um adaptador não precisa importar o núcleo.

Detalhe de tipo que carrega uma decisão de segurança: `ObjectStore` exige `put` e
`exists`, mas **não** exige `get`. É a tradução em código do papel `ingest`
write-only.

---

## ADR-008

**Dois repositórios: conceito e ambiente**

**Contexto.** Visão e arquitetura mudam quando o pensamento muda. Charts e
scripts mudam quando o código muda e precisam de tag, digest e release.

**Decisão.** `datalake-doomsday` (conceito, este) e `datalake-doomsday-env`
(ambiente instalável).

**Alternativa rejeitada.** Repositório único com `docs/` e `charts/` — sem custo
inicial, mas o `verify.sh` precisa fixar um commit de si mesmo para o bundle
(`versions.yaml`), e isso fica ambíguo quando prosa e chart compartilham histórico.

**Consequência.** Um risco de divergência, mitigado com **ponteiro**: o
`plano-atividades.md` existe só no repo do ambiente; aqui fica um link de 3 linhas.
Dois arquivos idênticos divergem na primeira edição; um ponteiro não.

---

## ADR-009

**Apache 2.0**

**Contexto.** O projeto se declara "100% software livre" em quatro documentos e
**não tinha arquivo de licença**. Sem licença, o código é legalmente
*all rights reserved* — não é open source.

**Decisão.** Apache 2.0, mesmo precedente do Project NOMAD.

**Alternativa rejeitada.** AGPLv3 — mais alinhada com o Garage, mas impõe
obrigações de rede que encarecem adoção por quem só quer rodar o lake na própria
casa.

**Consequência.** O `LICENSE` atual contém apenas o **aviso**, não o texto
integral, e diz isso numa nota. O CI **bloqueia tag de release** enquanto o texto
completo não estiver presente. Anunciar "Apache 2.0" com licença incompleta é pior
que dizer "licenciado sob os termos de".

---

## ADR-010

**Piso de VRAM em vez de flag booleana de GPU**

**Contexto.** Medido em 2026-11-18: a máquina de desenvolvimento tem
**RTX 3050 Laptop, 4096 MiB de VRAM, com ~3666 MiB já em uso** por outro serviço
(um `VLLM::EngineCore`). O Ollama está ativo com `qwen2.5-coder:7b` (4,7 GB).
`nvidia-ctk` e `nvidia-container-runtime` estão presentes; o addon `nvidia` do
microk8s existe.

A arquitetura supunha "GPU provavelmente ausente". **Estava errada.**

**Decisão.** O eixo `gpu` (`none`/`nvidia`/`amd`) descreve fabricante; módulos
declaram **`requires.vram`**. Módulo que não satisfaz o piso **recusa instalação**
com mensagem clara.

**Alternativa rejeitada.** Manter a flag booleana e "degradar para CPU" — 4 GB e
24 GB de VRAM são o mesmo "nvidia" e viabilizam coisas diferentes. Degradar em
silêncio para CPU entrega 1 token/s sem avisar, que é a mesma classe de mentira do
`estado-validado.md` afirmando inferência de LLM onde há uma string formatada.

**Consequência.** IA continua **fora** do escopo até a Onda 7 (§9 do plano) — a
GPU hoje é recurso disputado, não disponível. Mas a capacidade deixa de ser
especulação e vira restrição medida:

- embed pequeno: piso 2 GB — viável **se** a GPU ceder espaço
- LLM 7B quantizado: piso 6 GB — **não cabe** nesta máquina
- LLM 13B+: 12 GB+ — fora do escopo v1

**Regra:** nenhuma medição de desempenho de IA é válida com a GPU compartilhada.
Medir sob contenção não mede o modelo — mede a disputa.

### Emenda (2026-11-18) — o degrau de 4 GB

Os pisos acima estavam **incompletos**: ignoravam que existe um degrau utilizável
abaixo de 7B. Fonte: o estudo em `vllm-doomsday/docs/resultados.md`, medido nesta
máquina em 2026-09-07.

| modelo | piso de VRAM | nesta máquina |
|---|---|---|
| embed pequeno | 2 GB | ✅ |
| **LLM 0.5–1.5B** | **4 GB**, com `--enforce-eager` | ✅ **se a GPU estiver livre** |
| LLM 7B quantizado | 6 GB | ❌ |
| LLM 13B+ | 12 GB+ | ❌ |

O estudo é explícito sobre o que **não** caberia: com `gpu-memory-utilization 0.90`
e `max-model-len 4096`, o consumo somado (pesos 1,45 + ativação 0,25 + KV cache
1,61 + CUDA graphs 0,41 ≈ 3,72 GiB) estourou os 3,68 GiB disponíveis. A
configuração que estabilizou foi `0.80` / `2048` / `--enforce-eager`.

**Consequência para o módulo de IA.** Se ele existir, roda **vLLM**, não Ollama,
e por dois motivos concretos, não por preferência:

1. **Teto de memória explícito.** `--gpu-memory-utilization` é configuração;
   no Ollama o consumo é decidido pelo processo. Num pod que divide a GPU com
   outro serviço preexistente, controle explícito não é conveniência — é o que
   evita OOM.
2. **Batching contínuo.** O lake pode receber requisição do `query-api`, do
   dashboard e de um agente ao mesmo tempo. PagedAttention serve vários clientes
   com uma fração da VRAM que o modo single-stream exigiria.

O módulo deve falar **API OpenAI**, com vLLM como implementação de referência.
Amarrar em vLLM transformaria o Ollama — que já roda nesta máquina — em dívida
em vez de alternativa.

**Continua valendo:** a IA não entra antes da Onda 7. O que muda é que a decisão
técnica deixou de ser especulação e passou a ter medição com data e fonte.

---

## ADR-011

**Três camadas de acesso independentes**

**Contexto.** "Camadas de acesso" pode significar muita coisa e virar teatro de
segurança se houver só um ponto de imposição.

**Decisão.** Três mecanismos independentes; um só vazando, a camada não existe:

1. **Rede** — NetworkPolicy (Calico, efetivo no microk8s ao contrário do flannel)
2. **Objeto** — chave S3 do Garage por bucket + prefixo
3. **Catálogo** — role do PostgreSQL

**Alternativa rejeitada.** Só RBAC do Kubernetes — governa *pods*, não governa
leitura de objeto. Um pod autorizado a existir pode ler o bucket inteiro.

**Consequência.** Detalhes que carregam a segurança:

- `ingest` **escreve sem ler** `raw/` — ingestor comprometido não exfiltra o acervo
- `ai-worker` com `egress: []` — modelo não precisa de rede
- uma `Secret` por papel, montada só no pod correspondente — nenhum pod enxerga a
  credencial de outro

**Fricção deliberada:** leitura na LAN é livre (sem conta, como no NOMAD);
escrita, ingestão e operação destrutiva exigem token. Dois níveis, não seis.

---

## ADR-012

**Módulo `ingestion`, função `ingest()` — nunca o mesmo nome**

**Contexto.** Durante a Onda 1, o módulo `lakecore/ingest.py` e a função
`ingest()` tinham o mesmo nome. O `__init__.py` reexportava a função, o que faz
o pacote expor o **nome** `lakecore.ingest`. Resultado: `import lakecore.ingest
as modulo` devolvia a **função**, não o módulo.

Isso não quebrava nada visível — e é exatamente o problema. Um teste de
integridade usava `monkeypatch` nesse módulo para simular arquivo modificado
durante a gravação. Como o "módulo" era a função, o patch alterava atributos de
um objeto de função e a ingestão continuava usando a implementação real: o teste
**passava sem nunca exercitar a proteção**, e falhava ao ser reescrito com
`monkeypatch`.

**Decisão.** Renomear o módulo para `lakecore/ingestion.py`. A função pública
continua `ingest()`. Regra geral: **nome de módulo e nome de função não podem
colidir quando a função é reexportada no `__init__`**.

**Alternativas rejeitadas.**
- *Renomear a função para `ingest_file()`* — resolveria, mas `ingest` é o nome
  do domínio e a assinatura de CLI `lakecore ingest` já é natural.
- *Não reexportar a função no `__init__`* — manteria o nome privado do pacote e
  obrigaria todo chamador a `from lakecore.ingestion import ingest`. Funciona,
  mas o pacote existe para ser ergonômico; o nome do módulo é o detalhe interno.
- *Importar o módulo por caminho* (`importlib`) no teste — contornaria o sintoma.
  Teste que precisa de `importlib` para alcançar código de produção aponta para
  defeito de API, não para limitação do teste.

**Consequência.** Dois aprendizados que valem além deste caso:

1. **Um teste que não pode falhar é pior que teste ausente**, porque produz
   confiança. A detecção veio de reescrever o teste com a ferramenta correta
   (`monkeypatch`), não de ler o código.
2. **Incidente de processo registrado:** o commit da Onda 1 foi enviado com CI
   vermelho porque `make ci 2>&1 | tail` fez o `&&` do shell enxergar o exit code
   do `tail`. Corrigido com o alvo `make ci-check`, que aplica `set -o pipefail`
   e aborta com mensagem explícita. Gate validado com falha proposital: exit 2.
