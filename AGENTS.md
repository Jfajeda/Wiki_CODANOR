# AGENTS.md — Wiki CODANOR

## What this is

A local AI-powered knowledge base (RAG system) for CODANOR consulting projects. Uses Open WebUI + Ollama + ChromaDB to provide intelligent search over 10 thematic collections of documents (regulations, client data, OSINT feeds). Documents are stored on a Synology NAS; only vector indices live on the Mac.

## Architecture

```
NAS Synology (documents)          Mac (inference + vectors)
┌─────────────────────┐           ┌──────────────────────┐
│ Wiki_Knowledge/     │  mounted  │ Ollama (LLM + embed) │
│   PRIVADO/          │ ───────►  │ ChromaDB (vectordb/) │
│   PUBLICO/          │           │ Open WebUI (:3000)   │
└─────────────────────┘           └──────────────────────┘
```

## Quick start

```bash
# 1. Start Ollama (if not running)
open /Applications/Ollama.app

# 2. Ensure embedding model is available
ollama pull nomic-embed-text

# 3. Mount NAS (replace IP)
open smb://192.168.1.XXX/Wiki_Knowledge

# 4. Start Open WebUI
cd "/Users/jaimefajeda/Proyectos/Wiki_CODANOR"
docker compose up -d

# 5. Open browser
open http://localhost:3000
```

## Key constraints

- **RGPD**: Documents in `PRIVADO/` contain real client data. They must NEVER leave the local network (NAS + Mac). No cloud upload.
- **PUBLICO/**: Contains only publicly available regulations (INCIBE, AEPD, CCN-CERT, BOE, Magerit). Can be backed up to Google Drive.
- **Vectors are local**: ChromaDB stores in `./vectordb/`. Although embeddings don't contain reconstructible text, keep them local for precaution.
- **Ollama is native**: NOT in Docker. The container connects via `host.docker.internal:11434`.
- **No internet required for queries**: Once documents are ingested, the system works 100% offline.

## 10 Knowledge Collections

| Collection | Content | Source |
|---|---|---|
| ENS | Esquema Nacional de Seguridad | NAS/PUBLICO/ENS + Gestion_Riesgos_ENS |
| ISO27001 | Information Security Management | NAS/PUBLICO/ISO27001 + Gestion_Riesgos_ISO27001 |
| LOPD-RGPD | Data Protection | NAS/PUBLICO/LOPD-RGPD + Gestion_Riesgos_LOPD-RGPD |
| NIS2 | EU Cybersecurity Directive | NAS/PUBLICO/NIS2 |
| Legislacion | Spanish/Catalan law updates | NAS/PUBLICO/Legislacion + legislacion_monitor |
| Licitaciones | Public tenders | NAS/PRIVADO/Licitaciones |
| Logs-SIEM | Cybersecurity log analysis | NAS/PUBLICO/Logs-SIEM + ANALISIS_LOGs_PreSIEM |
| Actas | Client meeting minutes | NAS/PRIVADO/Actas (per client/project) |
| Plantillas | Document templates ENS/ISO | NAS/PRIVADO/Plantillas |
| OSINT | Open source intelligence feeds | NAS/PUBLICO/OSINT (auto-updated) |

## File structure

```
Wiki_CODANOR/
  Proyecto_Wiki_CODANOR.html   ← Full project documentation (open in browser)
  docker-compose.yml           ← Open WebUI container config
  .env.example                 ← Template for environment variables
  .gitignore                   ← Excludes vectordb/, .env, documents
  vectordb/                    ← ChromaDB data (created by Docker on first run)
  scripts/
    setup_nas_folders.sh       ← Creates folder structure on NAS
    ingest_nas.py              ← Reads NAS docs, feeds to Open WebUI
    fetch_osint.py             ← Downloads OSINT sources to NAS
```

## Gotchas

- **First run**: Docker will download ~2 GB for the Open WebUI image. Subsequent starts are instant.
- **Port 3000**: If occupied, change in docker-compose.yml (`"3001:8080"`).
- **NAS must be mounted**: Scripts expect `/Volumes/Wiki_Knowledge` to exist. If not mounted, mount first with `open smb://IP/Wiki_Knowledge`.
- **Ollama must be running**: Open WebUI connects to local Ollama. If Ollama is stopped, Open WebUI shows "connection error".
- **Embedding model**: `nomic-embed-text` must be pulled before first document ingestion. Without it, RAG won't work.
