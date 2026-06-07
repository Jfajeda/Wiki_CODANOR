#!/bin/bash
# =============================================================
# Wiki CODANOR — Crear estructura de carpetas en NAS Synology
# =============================================================
# Uso: bash scripts/setup_nas_folders.sh
# Prerequisito: NAS montado en /Volumes/Wiki_Knowledge
# =============================================================

NAS_MOUNT="/Volumes/Wiki_Knowledge"

# Verificar que el NAS esta montado
if [ ! -d "$NAS_MOUNT" ]; then
    echo "ERROR: El NAS no esta montado en $NAS_MOUNT"
    echo ""
    echo "Para montarlo:"
    echo "  1. Finder > Ir > Conectar al servidor"
    echo "  2. smb://TU_IP_NAS/Wiki_Knowledge"
    echo "  3. O desde Terminal: open smb://TU_IP_NAS/Wiki_Knowledge"
    exit 1
fi

echo "NAS detectado en $NAS_MOUNT"
echo "Creando estructura de carpetas..."

# Carpetas PRIVADO (datos de clientes — RGPD)
mkdir -p "$NAS_MOUNT/PRIVADO/Actas_Clientes"
mkdir -p "$NAS_MOUNT/PRIVADO/Plantillas_Rellenadas"
mkdir -p "$NAS_MOUNT/PRIVADO/Informes_Clientes"
mkdir -p "$NAS_MOUNT/PRIVADO/Licitaciones"

# Carpetas PUBLICO (normativas y guias — sin RGPD)
mkdir -p "$NAS_MOUNT/PUBLICO/ENS"
mkdir -p "$NAS_MOUNT/PUBLICO/ISO27001"
mkdir -p "$NAS_MOUNT/PUBLICO/LOPD-RGPD"
mkdir -p "$NAS_MOUNT/PUBLICO/NIS2"
mkdir -p "$NAS_MOUNT/PUBLICO/Legislacion"
mkdir -p "$NAS_MOUNT/PUBLICO/Logs-SIEM"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/INCIBE"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/CCN-CERT"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/AEPD"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/ENISA"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/BOE"
mkdir -p "$NAS_MOUNT/PUBLICO/OSINT/NIST"

echo ""
echo "Estructura creada correctamente:"
echo ""
echo "  $NAS_MOUNT/"
echo "  ├── PRIVADO/          (datos clientes — NUNCA subir a nube)"
echo "  │   ├── Actas_Clientes/"
echo "  │   ├── Plantillas_Rellenadas/"
echo "  │   ├── Informes_Clientes/"
echo "  │   └── Licitaciones/"
echo "  └── PUBLICO/          (normativas publicas — OK para backup en nube)"
echo "      ├── ENS/"
echo "      ├── ISO27001/"
echo "      ├── LOPD-RGPD/"
echo "      ├── NIS2/"
echo "      ├── Legislacion/"
echo "      ├── Logs-SIEM/"
echo "      └── OSINT/"
echo "          ├── INCIBE/"
echo "          ├── CCN-CERT/"
echo "          ├── AEPD/"
echo "          ├── ENISA/"
echo "          ├── BOE/"
echo "          └── NIST/"
echo ""
echo "Siguiente paso: copiar documentos existentes a las carpetas correspondientes."
