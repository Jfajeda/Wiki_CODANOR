#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiki CODANOR — Script de ingestion de documentos del NAS
=========================================================
Lee documentos del NAS montado y los sube a Open WebUI para indexacion RAG.

Uso:
    python3 scripts/ingest_nas.py                  # Ingesta completa
    python3 scripts/ingest_nas.py --collection ENS  # Solo una coleccion
    python3 scripts/ingest_nas.py --dry-run         # Solo listar archivos

Prerequisitos:
    - NAS montado en /Volumes/Wiki_Knowledge
    - Open WebUI corriendo en http://localhost:3000
    - pip install requests
"""

import os
import sys
import argparse
from pathlib import Path

# Configuracion
NAS_MOUNT = os.environ.get("NAS_MOUNT", "/Volumes/Wiki_Knowledge")
WEBUI_URL = os.environ.get("WEBUI_URL", "http://localhost:3000")
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md", ".html", ".csv"}

# Mapeo de carpetas NAS → colecciones Open WebUI
COLLECTIONS = {
    "ENS": "PUBLICO/ENS",
    "ISO27001": "PUBLICO/ISO27001",
    "LOPD-RGPD": "PUBLICO/LOPD-RGPD",
    "NIS2": "PUBLICO/NIS2",
    "Legislacion": "PUBLICO/Legislacion",
    "Logs-SIEM": "PUBLICO/Logs-SIEM",
    "OSINT": "PUBLICO/OSINT",
    "Actas": "PRIVADO/Actas_Clientes",
    "Plantillas": "PRIVADO/Plantillas_Rellenadas",
    "Licitaciones": "PRIVADO/Licitaciones",
}


def scan_documents(base_path, collection_path):
    """Escanea documentos en una carpeta del NAS."""
    full_path = Path(base_path) / collection_path
    if not full_path.exists():
        print(f"  [WARN] Carpeta no encontrada: {full_path}")
        return []

    docs = []
    for root, dirs, files in os.walk(full_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                docs.append(os.path.join(root, f))
    return docs


def upload_to_webui(filepath, collection_name):
    """Sube un documento a Open WebUI (placeholder — requiere API key)."""
    # NOTA: Open WebUI requiere autenticacion via API.
    # Este es un placeholder. La forma mas facil es usar
    # la interfaz web (drag&drop) para la primera carga.
    #
    # Para automatizacion futura, se puede usar la API REST:
    # POST /api/v1/files/
    # Headers: Authorization: Bearer <token>
    # Body: multipart/form-data con el archivo
    #
    # El token se obtiene en Open WebUI > Settings > Account > API Keys
    print(f"  [UPLOAD] {os.path.basename(filepath)} → {collection_name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Wiki CODANOR - Ingestion de documentos del NAS")
    parser.add_argument("--collection", "-c", help="Solo ingestar una coleccion especifica")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Solo listar archivos, no subir")
    args = parser.parse_args()

    # Verificar NAS montado
    if not os.path.isdir(NAS_MOUNT):
        print(f"ERROR: NAS no montado en {NAS_MOUNT}")
        print(f"Montar con: open smb://TU_IP_NAS/Wiki_Knowledge")
        sys.exit(1)

    print(f"NAS detectado: {NAS_MOUNT}")
    print(f"Open WebUI: {WEBUI_URL}")
    print("=" * 60)

    total_docs = 0
    collections_to_process = COLLECTIONS

    if args.collection:
        if args.collection not in COLLECTIONS:
            print(f"ERROR: Coleccion '{args.collection}' no existe.")
            print(f"Colecciones validas: {', '.join(COLLECTIONS.keys())}")
            sys.exit(1)
        collections_to_process = {args.collection: COLLECTIONS[args.collection]}

    for name, path in collections_to_process.items():
        print(f"\n[{name}] Escaneando {path}...")
        docs = scan_documents(NAS_MOUNT, path)
        print(f"  Encontrados: {len(docs)} documentos")

        if not args.dry_run:
            for doc in docs:
                upload_to_webui(doc, name)

        total_docs += len(docs)

    print("\n" + "=" * 60)
    print(f"Total: {total_docs} documentos en {len(collections_to_process)} colecciones")
    if args.dry_run:
        print("(Modo dry-run: no se ha subido nada)")
    print("\nNOTA: Para la primera carga, se recomienda usar la interfaz web")
    print(f"de Open WebUI ({WEBUI_URL}) con drag&drop desde el NAS montado.")


if __name__ == "__main__":
    main()
