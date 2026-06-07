#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wiki CODANOR — Descarga de fuentes OSINT publicas
==================================================
Descarga automaticamente documentos de fuentes abiertas de ciberseguridad
y normativas. Los guarda en el NAS para posterior ingestion en la Wiki.

Uso:
    python3 scripts/fetch_osint.py              # Todas las fuentes
    python3 scripts/fetch_osint.py --source incibe  # Solo INCIBE
    python3 scripts/fetch_osint.py --list       # Listar fuentes disponibles

Prerequisitos:
    - NAS montado en /Volumes/Wiki_Knowledge
    - pip install requests beautifulsoup4
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configuracion
NAS_MOUNT = os.environ.get("NAS_MOUNT", "/Volumes/Wiki_Knowledge")
OSINT_DIR = os.path.join(NAS_MOUNT, "PUBLICO", "OSINT")

# Fuentes OSINT catalogadas
OSINT_SOURCES = {
    "incibe": {
        "nombre": "INCIBE-CERT",
        "url_base": "https://www.incibe.es",
        "feeds": [
            "https://www.incibe.es/incibe-cert/alerta-temprana/avisos",
            "https://www.incibe.es/incibe-cert/guias-y-estudios",
        ],
        "carpeta": "INCIBE",
        "descripcion": "Alertas, guias y avisos de seguridad del INCIBE",
    },
    "ccn": {
        "nombre": "CCN-CERT",
        "url_base": "https://www.ccn-cert.cni.es",
        "feeds": [
            "https://www.ccn-cert.cni.es/es/series-ccn-stic.html",
            "https://www.ccn-cert.cni.es/es/comunicacion-eventos/comunicados-ccn-cert.html",
        ],
        "carpeta": "CCN-CERT",
        "descripcion": "Guias CCN-STIC (ENS), alertas y comunicados",
    },
    "aepd": {
        "nombre": "AEPD",
        "url_base": "https://www.aepd.es",
        "feeds": [
            "https://www.aepd.es/guias-y-herramientas/guias",
            "https://www.aepd.es/guias-y-herramientas/herramientas",
        ],
        "carpeta": "AEPD",
        "descripcion": "Guias RGPD, herramientas EIPD, resoluciones",
    },
    "enisa": {
        "nombre": "ENISA",
        "url_base": "https://www.enisa.europa.eu",
        "feeds": [
            "https://www.enisa.europa.eu/publications",
        ],
        "carpeta": "ENISA",
        "descripcion": "Normativa EU, threat landscape, buenas practicas",
    },
    "boe": {
        "nombre": "BOE",
        "url_base": "https://www.boe.es",
        "feeds": [
            "https://www.boe.es/diario_boe/",
        ],
        "carpeta": "BOE",
        "descripcion": "Legislacion espanola (filtrando seguridad/datos)",
    },
    "nist": {
        "nombre": "NIST",
        "url_base": "https://www.nist.gov",
        "feeds": [
            "https://www.nist.gov/cybersecurity",
            "https://csrc.nist.gov/publications",
        ],
        "carpeta": "NIST",
        "descripcion": "Frameworks y guias de ciberseguridad NIST",
    },
}


def check_nas():
    """Verifica que el NAS esta montado."""
    if not os.path.isdir(NAS_MOUNT):
        print(f"ERROR: NAS no montado en {NAS_MOUNT}")
        print(f"Montar con: open smb://TU_IP_NAS/Wiki_Knowledge")
        sys.exit(1)


def list_sources():
    """Lista todas las fuentes OSINT configuradas."""
    print("\nFuentes OSINT configuradas:")
    print("=" * 60)
    for key, source in OSINT_SOURCES.items():
        carpeta = os.path.join(OSINT_DIR, source["carpeta"])
        num_files = 0
        if os.path.isdir(carpeta):
            num_files = sum(1 for f in os.listdir(carpeta)
                          if os.path.isfile(os.path.join(carpeta, f)))
        print(f"\n  [{key}] {source['nombre']}")
        print(f"    URL: {source['url_base']}")
        print(f"    Descripcion: {source['descripcion']}")
        print(f"    Carpeta NAS: OSINT/{source['carpeta']}/")
        print(f"    Documentos actuales: {num_files}")


def fetch_source(key):
    """Descarga documentos de una fuente OSINT."""
    if key not in OSINT_SOURCES:
        print(f"ERROR: Fuente '{key}' no existe.")
        return

    source = OSINT_SOURCES[key]
    carpeta = os.path.join(OSINT_DIR, source["carpeta"])
    os.makedirs(carpeta, exist_ok=True)

    print(f"\n[{source['nombre']}] Consultando {source['url_base']}...")

    # NOTA: La descarga real requiere implementar scrapers especificos
    # para cada fuente. Este script es un esqueleto que muestra la
    # estructura. La implementacion completa de cada scraper se hara
    # en una fase posterior.
    #
    # Para la primera carga, se recomienda descargar manualmente
    # los PDFs/guias desde las URLs listadas y guardarlos en la
    # carpeta correspondiente del NAS.

    print(f"  Carpeta destino: {carpeta}")
    print(f"  Feeds configurados:")
    for feed in source["feeds"]:
        print(f"    - {feed}")

    print(f"\n  [INFO] Descarga automatica pendiente de implementar.")
    print(f"  Por ahora, descarga manualmente desde las URLs listadas")
    print(f"  y guarda los PDFs en: {carpeta}")

    # Guardar log de ultima consulta
    log_file = os.path.join(carpeta, ".last_fetch")
    with open(log_file, "w") as f:
        f.write(f"Ultima consulta: {datetime.now().isoformat()}\n")
        f.write(f"Fuente: {source['nombre']}\n")
        f.write(f"URLs:\n")
        for feed in source["feeds"]:
            f.write(f"  {feed}\n")


def main():
    parser = argparse.ArgumentParser(description="Wiki CODANOR - Descarga de fuentes OSINT")
    parser.add_argument("--source", "-s", help="Solo descargar una fuente especifica")
    parser.add_argument("--list", "-l", action="store_true", help="Listar fuentes disponibles")
    args = parser.parse_args()

    check_nas()

    if args.list:
        list_sources()
        return

    print(f"Wiki CODANOR — Descarga OSINT")
    print(f"NAS: {NAS_MOUNT}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    if args.source:
        fetch_source(args.source)
    else:
        for key in OSINT_SOURCES:
            fetch_source(key)

    print("\n" + "=" * 60)
    print("Completado. Siguiente paso: ingestar documentos en Open WebUI")
    print("  python3 scripts/ingest_nas.py")


if __name__ == "__main__":
    main()
