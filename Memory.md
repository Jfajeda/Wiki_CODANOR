# Memory.md — Wiki_CODANOR
> Ultima actualizacion: 2026-04-27

## Estado actual

- **Fase**: Proyecto creado, pendiente de arranque
- **Ultimo cambio significativo**: Creacion del proyecto con documentacion, docker-compose y scripts (2026-04-27)

## Infraestructura

| Elemento | Estado | Detalle |
|----------|--------|---------|
| Git | **No** | Pendiente de inicializar |
| GitHub | **No** | Pendiente (sin datos sensibles, solo infra) |
| SonarCloud | N/A | No aplica (proyecto de infraestructura, no codigo) |
| AGENTS.md | Si | Documenta arquitectura y colecciones |
| Memory.md | Si | Este archivo |
| Docker | Pendiente | docker-compose.yml preparado, falta ejecutar |
| NAS montado | Pendiente | Falta crear carpetas y montar |
| Open WebUI | Pendiente | Falta arrancar con docker compose up |
| nomic-embed-text | Pendiente | Falta descargar: ollama pull nomic-embed-text |

## Historial de decisiones

| Fecha | Decision | Razon |
|-------|----------|-------|
| 2026-04-27 | Arquitectura NAS + Mac (no cloud para datos clientes) | RGPD: datos de clientes nunca salen del hardware propio |
| 2026-04-27 | Open WebUI como interfaz Wiki | RAG integrado, sin codigo, drag&drop de documentos |
| 2026-04-27 | Ollama nativo (no en Docker) | Ya instalado, mejor rendimiento en Apple Silicon |
| 2026-04-27 | 10 colecciones tematicas | Alinear con los 10 proyectos existentes |
| 2026-04-27 | Separacion PRIVADO/PUBLICO en NAS | Distinguir datos RGPD de normativas publicas |

## Pendiente

- [ ] Instalar Docker Desktop (si no esta)
- [ ] Ejecutar `ollama pull nomic-embed-text`
- [ ] Crear carpeta compartida Wiki_Knowledge en NAS Synology
- [ ] Montar NAS en macOS
- [ ] Ejecutar `docker compose up -d`
- [ ] Crear cuenta admin en Open WebUI (http://localhost:3000)
- [ ] Crear las 10 Knowledge Bases en Open WebUI
- [ ] Copiar documentos publicos al NAS (INCIBE, AEPD, Magerit)
- [ ] Ingestar primeros documentos en Open WebUI
- [ ] Probar consultas RAG
- [ ] Inicializar Git
- [ ] Crear repo en GitHub (solo infra, sin datos)

## Notas y descubrimientos

- El proyecto ANALISIS_LOGs_PreSIEM ya usa datos de Synology NAS, asi que la conectividad Mac-NAS ya esta probada.
- iCloud NO se usara (causa problemas con Git y OpenCode, ya documentado).
- Los vectores (ChromaDB) ocupan ~500 MB para miles de documentos. Espacio minimo en Mac.
- Open WebUI soporta PDF, DOCX, MD, TXT nativamente via drag&drop.

---

> **Revisado 2026-11-13** — sin cambios de código en esta sesión (trabajo centrado en `Plataforma_Seguimiento_Proyectos`).
