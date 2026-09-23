# Laboratório VM-01 (data-core)

Servicios do laboratório local para a camada de dados e catálogo:

- MinIO: armazenamento bruto (console em :9001, API S3 em :9000)
- PostgreSQL: metadados e catálogo (:5432)

## Variáveis de ambiente

Todos os valores sensíveis são lidos a partir de variáveis de ambiente. O Docker
Compose interpola o `.env` do mesmo diretório, se existir, com estes valores por
default de laboratório (NÃO usar em ambientes não controlados):

| Variable | Default (laboratório) | Descrição |
|----------|----------------------|-----------|
| `MINIO_ROOT_USER` | `minioadmin` | Usuario root de MinIO |
| `MINIO_ROOT_PASSWORD` | `minioadmin` | Senha root de MinIO |
| `POSTGRES_DB` | `datalake` | Nome da base |
| `POSTGRES_USER` | `datalake` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | `change-me` | Senha de PostgreSQL |

## Configuração local (recomendada)

Para sobrescribir os defaults no laboratório, cree um arquivo `.env` neste
diretório (está em `.gitignore`, não se versiona):

```bash
cp .env.example .env
```

> Nota: por política de segurança, o repositório não versiona `.env.example`.
> Use a tabela acima como referência ou gere seu próprio `.env` com os mesmos
> nomes de variável.

## Uso

```bash
# Validar composición
docker compose config >/dev/null

# Subir serviços
docker compose up -d
```